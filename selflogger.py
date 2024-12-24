import logging
import logging.handlers

def getlogger(name:str|None='my_logger',filepath:str|None='output.log'):
    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置日志级别
    # 日志文件路径
    log_file = 'client.log'
    # 单个日志文件最大大小
    max_bytes = 1024 * 1024  # 1MB
    # 最多保留的日志文件数
    backup_count = 20
    # 创建 file handler 并设置日志级别
    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
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
