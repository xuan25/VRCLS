import speech_recognition as sr
import requests
from multiprocessing import Process,Queue
import keyboard
import time
import pyttsx3



def once(audio:sr.AudioData,sendClient,config,params,logger,filter,mode,steamvrQueue,customEmoji:dict):
    from ..handler.DefaultCommand import DefaultCommand
    from ..handler.ChatBox import ChatboxHandler
    from ..handler.Avatar import AvatarHandler
    from ..handler.VRCBitmapLedHandler import VRCBitmapLedHandler
    from ..handler.SelfRead import SelfReadHandler
    from hanziconv import HanziConv

    
    tragetTranslateLanguage=params["tragetTranslateLanguage"]
    sourceLanguage=params["sourceLanguage"]
    avatar=AvatarHandler(logger=logger,osc_client=sendClient,config=config)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,config=config)
    chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,config=config)
    bitMapLed=VRCBitmapLedHandler(logger=logger,osc_client=sendClient,config=config,params=params)
    selfRead=SelfReadHandler(logger=logger,osc_client=sendClient,steamvrQueue=steamvrQueue,config=config)
    baseurl=config.get('baseurl')
    try:

        logger.put({"text":f"{"麦克风" if mode=="mic" else "桌面"}音频输出完毕","level":"info"})
        st=time.time()
        if params["runmode"] == "control" or params["runmode"] == "text" or params["runmode"] == "bitMapLed":
            url=baseurl+"/whisper/multitranscription"
        elif params["runmode"] == "translation":
            if mode =="cap":
                tmp=sourceLanguage
                sourceLanguage=tragetTranslateLanguage
                tragetTranslateLanguage=tmp
            if config["translationServer"] == "libre":

                if tragetTranslateLanguage=="en" and sourceLanguage== "zh" :url=baseurl+"/func/translateToEnglish"
                elif sourceLanguage != "zh" :url=baseurl+"/func/multitranslateToOtherLanguage"
                else:url=baseurl+"/func/translateToOtherLanguage"
            else:
                url=baseurl+"/func/doubleTransciption"
        else: 
            logger.put({"text":"运行模式异常,运行默认控制模式","level":"debug"})
            params["runmode"] = "control"
            url = baseurl+"/whisper/multitranscription"
        logger.put({"text":f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}","level":"debug"})
        files = {'file': ('filename', audio.get_wav_data(), 'audio/wav')}
        
        data = {'targetLanguage': tragetTranslateLanguage, 'sourceLanguage': "zh" if sourceLanguage=="zt" else  sourceLanguage}
        response = requests.post(url, files=files, data=data, headers=params['headers'])
        # 检查响应状态码
        counter=0  
        if response.status_code != 200:
            if response.status_code == 430 and counter < 3:
                res=response.json()
                logger.put({"text":f"请求过于频繁,触发规则{res.get("limit")}","level":"warning"})
            else:    
                logger.put({"text":f"数据接收异常:{response.text}","level":"warning"})
            return
        # 解析JSON响应
        res = response.json()
        et=time.time()
        if res["text"] =="":
            logger.put({"text":"返回值过滤-服务端规则","level":"info"})
            return
        if res["text"] in filter:
            logger.put({"text":"返回值过滤-自定义规则","level":"info"})
            return
        if sourceLanguage== "zh":res["text"]=HanziConv.toSimplified(res["text"])
        elif sourceLanguage=="zt":res["text"]=HanziConv.toTraditional(res["text"])
        logger.put({"text":f"用时：{round(et-st,2)}s 识别结果: " + res["text"],"level":"info"})
        if defaultCommand.handle(res["text"],params=params):return
        if mode=="cap":selfRead.handle(res,"桌面音频",params["steamReady"])
        else:
            if params["runmode"] == "text" or params["runmode"] == "translation": 
                for key in list(customEmoji.keys()):res['text']=res['text'].replace(key,customEmoji[key])
                if params["runmode"] == "translation" : 
                    for key in list(customEmoji.keys()):res['translatedText']=res['translatedText'].replace(key,customEmoji[key])
                if config.get("textInSteamVR"):selfRead.handle(res,"麦克风",params["steamReady"])
                chatbox.handle(res,runMode=params["runmode"])
            if params["runmode"] == "control":avatar.handle(res)
            if params["runmode"] == "bitMapLed":bitMapLed.handle(res,params=params)

    except requests.JSONDecodeError:
        logger.put({"text":"json解析异常,code:"+str(response.status_code)+" info:"+response.text,"level":"warning"})
        return
    except Exception as e:
        logger.put({"text":"once未知异常"+str(e),"level":"error"})
        return
def change_run(params,logger,mode):
    key="voiceKeyRun"if mode=="mic" else "gameVoiceKeyRun"
    params[key]=not params[key]
    logger.put({"text":f"{"麦克风" if mode=="mic" else "桌面音频"}状态：{"打开" if params[key] else "关闭"}","level":"info"})

def clearVRCBitmapLed(client,config,params,logger):
    logger.put({"text":f"开始清空点阵屏","level":"info"})

    if "clear" not in params["VRCBitmapLed_taskList"]:params["VRCBitmapLed_taskList"].append("clear")
    else:return
    while params["VRCBitmapLed_taskList"][0]!="clear":
        if "clear" not in params["VRCBitmapLed_taskList"]:return
        time.sleep(0.1)
    num=(8 if config.get("VRCBitmapLed_row") is None else config.get("VRCBitmapLed_row") )*(16 if config.get("VRCBitmapLed_col") is None else config.get("VRCBitmapLed_col"))
    if num==128:
        for i in range(num):

            if params["VRCBitmapLed_taskList"][0]!="clear":return
            client.send_message("/avatar/parameters/BitmapLed/Pointer", i)
            client.send_message(f"/avatar/parameters/BitmapLed/Data", 0)
            client.send_message(f"/avatar/parameters/BitmapLed/DataX16", 0)
            params["VRCBitmapLed_Line_old"]=params["VRCBitmapLed_Line_old"][:i+1]+" "+params["VRCBitmapLed_Line_old"][i+2:]
            time.sleep(0.2)
    elif num==256:
        client.send_message("/avatar/parameters/BitmapLed/Pointer", 255)
        client.send_message(f"/avatar/parameters/BitmapLed/Data", 4)
        client.send_message(f"/avatar/parameters/BitmapLed/DataX16", 0)
    params["VRCBitmapLed_taskList"].pop(0)
    logger.put({"text":f"清空点阵屏完成","level":"info"})

def selfMic_listen(sendClient,config,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji):
    if config.get("micName")== "" or config.get("micName") is None or config.get("micName")== "default":
        logger.put({"text":"使用系统默认麦克风","level":"info"})
        micIndex=defautMicIndex
    else:
        try:
            micIndex=micList.index(config.get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前麦克风：{micList[micIndex]}","level":"info"})
    r = sr.Recognizer()
    m = sr.Microphone(device_index=micIndex)
    params["voiceKeyRun"]=True 
    voiceMode=config.get("voiceMode")
    dynamicVoice=config.get("dynamicThreshold")
    r.dynamic_energy_threshold=False if dynamicVoice is None or dynamicVoice == False else True
    customthreshold=config.get("customThreshold")
    voiceHotKey=config.get("voiceHotKey")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["voiceKeyRun"]=False 
        keyboard.add_hotkey(hotkey=voiceHotKey, callback=change_run,args=(params,logger,"mic"))
        logger.put({"text":f"当前麦克风状态：{"打开" if params["voiceKeyRun"] else "关闭"}","level":"info"})
    
    if customthreshold is None or not isinstance(customthreshold, (int, float)) or dynamicVoice:
        logger.put({"text":"开始音量测试","level":"info"})
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        logger.put({"text":"结束音量测试","level":"info"})
    else:
        r.energy_threshold=32768.0*customthreshold

    logger.put({"text":"sound process started complete||音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("麦克风音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    count=0
    with m as s:
        while params["running"]:
            if not params["voiceKeyRun"]:continue
            try:  # listen for 1 second, then check again if the stop function has been called
                audio = r.listen(s, 10,30)
                count=0
            except sr.WaitTimeoutError:  # listening timed out, just try again
                if params["runmode"] == "bitMapLed":
                    if count>=2:
                        pt = Process(target=clearVRCBitmapLed,daemon=True, args=(sendClient,config,params,logger))
                        pt.start()
                    else:count+=1
            else:
                if params["running"] and params["voiceKeyRun"]:
                    p = Process(target=once,daemon=True, args=(audio,sendClient,config,params,logger,filter,"mic",steamvrQueue,customEmoji))
                    p.start()

    logger.put({"text":"sound process exited complete||麦克风音频进程退出完毕","level":"info"})
    params["micStopped"]=True


def gameMic_listen_VoiceMeeter(sendClient,config,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji):
    if config.get("gameMicName")== "" or config.get("gameMicName") is None :
        logger.put({"text":"请指定游戏麦克风，游戏麦克风线程退出","level":"warning"})
        return
    else:
        try:
            micIndex=micList.index(config.get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定游戏麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前游戏麦克风：{micList[micIndex]}","level":"info"})
    r = sr.Recognizer()
    m = sr.Microphone(device_index=micIndex)
    params["gameVoiceKeyRun"]=True 
    voiceMode=config.get("voiceMode")
    dynamicVoice=config.get("dynamicThreshold")
    r.dynamic_energy_threshold=False if dynamicVoice is None or dynamicVoice == False else True
    customthreshold=config.get("gameCustomThreshold")
    voiceHotKey=config.get("gameVoiceHotKey")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["gameVoiceKeyRun"]=False 
        keyboard.add_hotkey(hotkey=voiceHotKey, callback=change_run,args=(params,logger,"cap"))
        logger.put({"text":f"当前游戏麦克风状态：{"打开" if params["gameVoiceKeyRun"] else "关闭"}","level":"info"})
    
    if customthreshold is None or not isinstance(customthreshold, (int, float)) or dynamicVoice:
        logger.put({"text":"开始音量测试","level":"info"})
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        logger.put({"text":"结束音量测试","level":"info"})
    else:
        r.energy_threshold=32768.0*customthreshold

    logger.put({"text":"sound process started complete||游戏音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("游戏音频进程启动完毕")
    except:pass
    count=0
    with m as s:
        while params["running"]:
            if not params["gameVoiceKeyRun"]:continue
            try:  # listen for 1 second, then check again if the stop function has been called
                audio = r.listen(s, 10,30)
                count=0
            except sr.WaitTimeoutError:  # listening timed out, just try again
                if params["runmode"] == "bitMapLed":
                    if count>=2:
                        pt = Process(target=clearVRCBitmapLed,daemon=True, args=(sendClient,config,params,logger,"vm"))
                        pt.start()
                    else:count+=1
            else:
                if params["running"] and params["gameVoiceKeyRun"]:
                    p = Process(target=once,daemon=True, args=(audio,sendClient,config,params,logger,filter,"cap",steamvrQueue,customEmoji))
                    p.start()

    logger.put({"text":"sound process exited complete||游戏音频进程退出完毕","level":"info"})
    params["gameStopped"] = True

def gameMic_listen_capture(sendClient,config,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji):
    from .recordLocal import voice_activation_stream
    if config.get("gameMicName")== "" or config.get("gameMicName") is None or config.get("gameMicName")== "default":
        logger.put({"text":"使用系统默认桌面音频","level":"info"})
        micIndex=None
    else:
        device_index=False
        for i in micList:
            if config.get("gameMicName")==i.get("name"):
                device_index=True
                micIndex=i.get('index')
                logger.put({"text":f"当前桌面音频：{config.get("gameMicName")}","level":"info"})
                break
        
            
        if not device_index:
            logger.put({"text":"无法找到指定桌面音频，使用系统默认桌面音频","level":"info"})
            micIndex=None
    params["gameVoiceKeyRun"]=True 
    voiceMode=config.get("gameVoiceMode")
    customthreshold=config.get("gameCustomThreshold")
    voiceHotKey=config.get("gameVoiceHotKey")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["gameVoiceKeyRun"]=False 
        keyboard.add_hotkey(hotkey=voiceHotKey, callback=change_run,args=(params,logger,"cap"))
        logger.put({"text":f"当前桌面音频捕获状态状态：{"打开" if params["gameVoiceKeyRun"] else "关闭"}","level":"info"})

    energy_threshold=32768.0*customthreshold

    logger.put({"text":"sound process started complete||桌面音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("桌面音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    count=0
    while params["running"]:
        if not params["gameVoiceKeyRun"]:continue
        try:  # listen for 1 second, then check again if the stop function has been called
            audio = voice_activation_stream(
                logger=logger,
                micIndex=micIndex,
                params=params,
                silence_threshold=int(energy_threshold)
            )
            count=0
        except sr.WaitTimeoutError:  # listening timed out, just try again
            if params["runmode"] == "bitMapLed":
                if count>=2:
                    pt = Process(target=clearVRCBitmapLed,daemon=True, args=(sendClient,config,params,logger))
                    pt.start()
                else:count+=1
        else:
            if params["running"] and params["gameVoiceKeyRun"]:
                p = Process(target=once,daemon=True, args=(audio,sendClient,config,params,logger,filter,"cap",steamvrQueue,customEmoji))
                p.start()

    logger.put({"text":"sound process exited complete||桌面音频进程退出完毕","level":"info"})
    params["gameStopped"] = True

def logger_process(queue, copyqueue, params):
    from .logger import MyLogger
    import sqlite3
    import datetime

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
    keyweod_list = ["返回值过滤-"]
    localizedSpeech=None
    localizedCapture=None
    while True:
        text = queue.get()
        if localizedSpeech != params.get("localizedSpeech"):
            localizedSpeech=params.get("localizedSpeech")
            if not localizedSpeech: keyweod_list.append("输出文字: ")
            else:
                try:keyweod_list.remove("输出文字: ")
                except:pass
        if localizedCapture != params.get("localizedCapture"):
            localizedCapture=params.get("localizedCapture")
            if not localizedCapture: keyweod_list.append("桌面音频识别结果：")
            else:
                try:keyweod_list.remove("桌面音频识别结果：")
                except:pass
        # 原有的复制逻辑
        if params.get('opencopybox'):
            for txt in ["输出文字: ", "桌面音频识别结果："]:
                if txt in text['text']:
                    tmp_text=text['text'].split(txt, 1)[1].strip()
                    copyqueue.put(tmp_text[:len(tmp_text)-4])

        # 新增的统计逻辑
        if any(keyword in text['text'] for keyword in keyweod_list):
            today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
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

# def steamvr_process(logger,queue:Queue,params,hand=0,size=0.15):
#     import openvr
#     from..module.steamvr import VRTextOverlay
#     textOverlay=VRTextOverlay()
#     try:
#         if not textOverlay.initialize(logger,params,hand):return
#         textOverlay._create_text_texture()
#         textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle,size)
#         textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
#         logger.put({"text":f"掌心显示启动完毕","level":"info"})
#         try:pyttsx3.speak("SteamVR掌心显示启动完毕")
#         except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
#         while params['running']:
#             if queue.empty():
#                 time.sleep(0.5)
#                 continue
#             text=queue.get() 
#             logger.put({"text":f"开始执行一次掌心输出","level":"debug"})
#             textOverlay.update_text(text)
#             time.sleep(1)
#     # except Exception as e:
#     #     logger.put({"text":f"发生错误: {str(e)}","level":"error"})
#     finally:  # 确保始终执行清理
#         if textOverlay.overlay_handle:
#             textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
#             textOverlay.overlay.destroyOverlay(textOverlay.overlay_handle)
#         openvr.shutdown()
#         time.sleep(1)

def steamvr_process(logger, queue: Queue, params,config):
    import openvr
    from ..module.steamvr import VRTextOverlay
    textOverlay = VRTextOverlay()
    MAX_RETRIES = 10  # 最大重试次数
    retry_count = 0
    is_two_hand=config.get("SteamVRHad")==2
    def safe_shutdown():
        try:
            if textOverlay.overlay_handle:
                textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
                textOverlay.overlay.destroyOverlay(textOverlay.overlay_handle)
            openvr.shutdown()
            logger.put({"text":"VR资源已安全释放","level":"info"})
        except Exception as e:
            logger.put({"text":f"关闭资源时出错:{str(e)}","level":"error"})

    try:
        # 带重试的初始化
        while retry_count < MAX_RETRIES and params['running']:
            try:
                if not textOverlay.initialize(logger, params, config):
                    raise RuntimeError("SteamVR初始化失败")
                # logger.put({"text":"SteamVR初始化成功","level":"info"})
                last_success = time.time()
                check_interval = 10  # 手柄状态检查间隔
                error_count = 0
                MAX_ERRORS = 5  # 最大连续错误次数
                textOverlay._create_text_texture()
                textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle,config.get("SteamVRSize")*(1.5 if config.get("Separate_Self_Game_Mic")!=0 else 1.0))
                textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
                if is_two_hand:
                    textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle_1,config.get("SteamVRSize")*(1.5 if config.get("Separate_Self_Game_Mic")!=0 else 1.0))
                    textOverlay.overlay.showOverlay(textOverlay.overlay_handle_1)
                logger.put({"text":f"掌心显示启动完毕","level":"info"})
                # 主循环
                while params['running']:
                    try:
                        # 定期设备检查
                        if time.time() - last_success > check_interval:
                            
                            if config.get("SteamVRHad") ==2:
                                current_status = textOverlay.set_overlay_to_hand(0) and textOverlay.set_overlay_to_hand(1,True)
                            else:
                                current_status = textOverlay.set_overlay_to_hand(config.get("SteamVRHad"))
                                

                            if not current_status:
                                logger.put({"text":"控制器连接状态异常，尝试恢复...","level":"warning"})
                                textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
                                if is_two_hand:textOverlay.overlay.hideOverlay(textOverlay.overlay_handle_1)
                                time.sleep(1)
                                textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
                                if config.get("SteamVRHad") ==2:
                                    textOverlay.overlay.showOverlay(textOverlay.overlay_handle_1)
                                    status_tmp = textOverlay.set_overlay_to_hand(0) and textOverlay.set_overlay_to_hand(1,True)
                                else:
                                    status_tmp = textOverlay.set_overlay_to_hand(config.get("SteamVRHad"))
                             
                                if status_tmp:
                                    last_success = time.time()
                                    logger.put({"text":"控制器连接恢复成功","level":"info"})
                                else: continue
                            else:
                                last_success = time.time()
                            
                        error=0
                        # 处理消息队列
                        if not queue.empty():
                            text = queue.get()
                            logger.put({"text":f"开始处理新的文本更新","level":"debug"})
                            
                            
                            # 带重试的更新操作
                            for _ in range(3):  # 最多重试3次
                                try:
                                    textOverlay.update_text(text)
                                    error=200
                                    break
                                except openvr.openvr.error_code.OverlayError_RequestFailed:
                                    logger.put({"text":f"OpenVR错误: {str(type(oe))}，尝试恢复初始化,{error}","level":"error"})
                                    safe_shutdown()
                                    time.sleep(5)
                                    if not textOverlay.initialize(logger, params, config):
                                        raise RuntimeError("SteamVR初始化失败")
                                    time.sleep(1)
                                    textOverlay._create_text_texture()  # 重新创建纹理
                                    time.sleep(1)
                                except openvr.error_code.OverlayError as oe:
                                    error+=1
                                    logger.put({"text":f"OpenVR错误: {str(type(oe))}，尝试恢复...,{error}","level":"error"})
                                    textOverlay._create_text_texture()  # 重新创建纹理
                                    time.sleep(1)
                                    
                            
                            # 强制更新Overlay属性
                            textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle, config.get("SteamVRSize")*(1.0 if config.get("Separate_Self_Game_Mic")==0 or config.get("SteamVRHad") ==2 else 1.5))
                            textOverlay.overlay.setOverlayAlpha(textOverlay.overlay_handle, 1.0)
                            if config.get("SteamVRHad") ==2:
                                # 强制更新Overlay属性
                                textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle_1, config.get("SteamVRSize")*(1.0 if config.get("Separate_Self_Game_Mic")==0 or config.get("SteamVRHad") ==2 else 1.5))
                                textOverlay.overlay.setOverlayAlpha(textOverlay.overlay_handle_1, 1.0)
                        time.sleep(0.1)
                        if error ==200:error_count = 0  # 重置错误计数器

                    except Exception as inner_e:
                        error_count += 1
                        logger.put({"text":f"[运行时错误] {str(type(inner_e))} ({error_count}/{MAX_ERRORS})","level":"error"})
                        if error_count >= MAX_ERRORS:
                            logger.put({"text":"达到最大错误次数，尝试重新初始化...","level":"critical"})
                            safe_shutdown()
                            time.sleep(5)
                            break  # 退出内层循环进行重新初始化

                # 正常退出循环
                if not params['running']:
                    break

            except Exception as init_e:
                retry_count += 1
                logger.put({"text":f"初始化失败 ({retry_count}/{MAX_RETRIES}): {str(type(init_e))}","level":"error"})
                safe_shutdown()
                time.sleep(5)  # 指数退避
                
        if retry_count >= MAX_RETRIES:
            logger.put({"text":"达到最大重试次数，SteamVR功能终止","level":"error"})

    except Exception as outer_e:
        logger.put({"text":f"[未捕获的异常] {str(type(outer_e))}|| {str(outer_e)}","level":"error"})
    finally:
        safe_shutdown()
        # 确保释放所有VR资源
        for _ in range(3):
            try:
                openvr.shutdown()
            except:
                pass
            time.sleep(1)

def copyBox_process(queue:Queue):
    import tkinter as tk
    from ..module.copybox import ScrollableListApp
    # 启动GUI
    root = tk.Tk()
    app = ScrollableListApp(root, queue)
    root.geometry("500x400")
    
    # 绑定关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()