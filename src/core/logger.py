import logging
import logging.handlers
from typing import Optional
class MyLogger:
    def __init__(self):
        self.logger=self.getlogger()

    def getlogger(self,name: Optional[str] = "my_logger",filepath: Optional[str] ='VRCLS.log'):
        # 创建 logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)  # 设置日志级别
        # 日志文件路径
        log_file = filepath
        # 单个日志文件最大大小
        max_bytes = 1024 * 1024  # 1MB
        # 最多保留的日志文件数
        backup_count = 20
        # 创建 file handler 并设置日志级别
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count,encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        
        # 创建 console handler 并设置日志级别
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # 定义 handler 的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # 给 logger 添加 handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

def logger_process(queue, copyqueue, params, socketQueue):
    from .logger import MyLogger
    import sqlite3
    import datetime
    import traceback

    logger = MyLogger().logger

    # 初始化数据库连接
    conn = sqlite3.connect('log_statistics.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # 创建统计表（如果不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_stats
                     (date TEXT PRIMARY KEY, count INTEGER DEFAULT 0)''')
    conn.commit()
    # 创建统计表（如果不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_fail_stats
                     (date TEXT PRIMARY KEY, count INTEGER DEFAULT 0)''')
    conn.commit()
    # 定义需要统计的关键词列表
    keyweod_list = ["返回值过滤-","服务器翻译成功："]
    localizedSpeech=None
    localizedCapture=None
    TTSToggle=None
    
    infoType={
        "麦克风识别结果：":'mic',
        "桌面音频识别结果：":'cap',
        '文字发送识别结果：':'mic',
        "桌面音频请求过于频繁,可以尝试更换其他翻译引擎,触发规则":'cap',
        "麦克风请求过于频繁,可以尝试更换其他翻译引擎,触发规则":'mic',
        "文字发送请求过于频繁,可以尝试更换其他翻译引擎,触发规则":'mic',
        '桌面音频请求过于频繁,触发规则':'cap',
        "麦克风请求过于频繁,触发规则":'mic',
        '桌面音频本地识别服务器翻译数据接收异常:':'cap',
        '麦克风本地识别服务器翻译数据接收异常:':'mic',
        '文字发送翻译数据接收异常:':'mic',
        '桌面音频服务器数据接收异常:':'cap',
        '麦克风服务器数据接收异常:':'mic',
        'TTS请求过于频繁,触发规则':'mic',
        "TTS数据接收异常:":'mic',
        
        
    }
    try:
        while True:
            text = queue.get()
            if localizedSpeech != params.get("localizedSpeech"):
                localizedSpeech=params.get("localizedSpeech")
                if not localizedSpeech: keyweod_list.append("服务器识别总用时：")
                else:
                    try:keyweod_list.remove("服务器识别总用时：")
                    except:pass
            if localizedCapture != params.get("localizedCapture"):
                localizedCapture=params.get("localizedCapture")
                if not localizedCapture: keyweod_list.append("桌面音频识别结果：")
                else:
                    try:keyweod_list.remove("桌面音频识别结果：")
                    except:pass
            if TTSToggle != params.get("TTSToggle"):
                TTSToggle=params.get("TTSToggle")
                if TTSToggle!=0: keyweod_list.append("TTS文本生成: ")
                else:
                    try:keyweod_list.remove("TTS文本生成: ")
                    except:pass
            # 原有的复制逻辑
            for txt in infoType.keys():
                if txt in text['text']:
                    tmp_text=text['text'].split(txt, 1)[1].strip()
                    if params['running']:
                        socketQueue.put({'type':infoType[txt],'text':tmp_text[:len(tmp_text)-4] if '识别结果' in txt else text['text']})
            
            today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
            # 新增的统计逻辑
            if any(keyword in text['text'] for keyword in keyweod_list):
                
                try:
                    # 使用UPSERT语法更新统计
                    cursor.execute('''INSERT INTO daily_stats (date, count) 
                                    VALUES (?, 1)
                                    ON CONFLICT(date) 
                                    DO UPDATE SET count = count + 1''', (today,))
                    conn.commit()
                except Exception as e:
                    logger.error(f"数据库更新失败: {str(e)}")
                    conn.rollback()
            if any(keyword in text['text'] for keyword in ["请求过于频繁,触发规则","数据接收异常:"]):
                
                try:
                    # 使用UPSERT语法更新统计
                    cursor.execute('''INSERT INTO daily_fail_stats (date, count) 
                                    VALUES (?, 1)
                                    ON CONFLICT(date) 
                                    DO UPDATE SET count = count + 1''', (today,))
                    conn.commit()
                except Exception as e:
                    logger.error(f"数据库更新失败: {str(e)}")
                    conn.rollback()

            # 原有的日志记录逻辑
            log_level = text['level']
            log_content = text['text']
            {
                "debug": logger.debug,
                "info": logger.info,
                "warning": logger.warning,
                "error": logger.error
            }.get(log_level, logger.error)(log_content)
            if log_level!="debug" and params['running']:socketQueue.put({
                        'type':'log',
                        'text': text['text'],
                        'level': text['level'],
                        'timestamp': datetime.datetime.now().isoformat()
                    })
    except Exception:
        logger.error(f'日志进程报错：{traceback.format_exc()}')