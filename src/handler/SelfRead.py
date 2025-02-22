from typing import Optional
from .base_handler import BaseHandler
from .Color import Colors

class SelfReadHandler(BaseHandler):
    def __init__(self,logger, osc_client,steamvrQueue,config):
        super().__init__(osc_client)
        self.logger=logger
        self.steamvrQueue=steamvrQueue
        self.steamvrOpen=config.get("textInSteamVR")
    """聊天框处理器"""
        
    def handle(self, res,source:str,steamready):
        text=res['text']
        transtext=res.get('translatedText')
        if transtext:message=f"{transtext}({text})"
        else:message=text
        logger=self.logger
        logger.put({"text":f"{Colors.YELLOW if source=="麦克风" else Colors.GREEN}{source}识别结果：{message}{Colors.END}","level":"info"})
        if self.steamvrOpen and steamready:
            self.steamvrQueue.put(f"{source}识别结果：\n{message}")

