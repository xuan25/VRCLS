from typing import Optional
from .base_handler import BaseHandler
import winsound
import time
import pyttsx3
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
        logger.put({"text":f"{source}识别结果：{message}","level":"info"})
        if self.steamvrOpen and steamready:
            self.steamvrQueue.put(f"{source}识别结果：\n{message}")

