import logging

def getlogger(name:str|None='my_logger',filepath:str|None='output.log'):
    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置日志级别
    
    # 创建 file handler 并设置日志级别
    fh = logging.FileHandler(filepath,encoding='utf-8')
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
