from typing import Optional
from .base_handler import BaseHandler
import winsound
import time
import pyttsx3
class AvatarHandler(BaseHandler):
    def __init__(self,logger, osc_client,config):
        super().__init__(osc_client)
        self.config=config
        self.logger=logger
    """聊天框处理器"""
        
    def handle(self, message: str):
        self.controlFunction(message)
    def controlFunction(self,res):
        config=self.config
        logger=self.logger
        text=res['text']
        global running
        if config["activateText"] == "":
            logger.put({"text":"无头命令:"+text,"level":"info"})
            for script in config.get("scripts"):
                if any( command in text  for command in script.get("text")):
                    logger.put({"text":"执行命令:"+script["action"],"level":"info"})
                    for vrcaction in script["vrcActions"]:
                        type=vrcaction.get("vrcValueType")
                        if type=="float":value=float(vrcaction.get("vrcValue"))
                        elif type=="int":value=int(vrcaction.get("vrcValue"))
                        elif type=="bool":value=bool(vrcaction.get("vrcValue"))
                        else:
                            logger.put({"text":"未知参数类型，使用bool模式","level":"warning"})
                            value=bool(vrcaction.get("vrcValue"))
                        self.osc_client.send_message(vrcaction.get("vrcPath"),value)
                        time.sleep( float(vrcaction.get("sleeptime")) if vrcaction.get("sleeptime") is not None and vrcaction.get("sleeptime") != ""  else 0.1)
                    pyttsx3.speak(f"触发命令 {script["action"]}")
        elif config["activateText"] in text:
            commandlist=text.split(config["activateText"])
            command=commandlist[-1]
            if (config["stopText"] in command) or config["stopText"] == "":
                if config["stopText"] != "":command=command.split(config["stopText"])[0]
                logger.put({"text":"有头命令:"+command,"level":"info"})
                for script in config.get("scripts"):
                    if command in script.get("text"):
                        logger.put({"text":"执行命令:"+script.get("action"),"level":"info"})
                        for vrcaction in script["vrcActions"]:
                            type=vrcaction.get("vrcValueType")
                            if type=="float":value=float(vrcaction.get("vrcValue"))
                            elif type=="int":value=int(vrcaction.get("vrcValue"))
                            elif type=="bool":value=bool(vrcaction.get("vrcValue"))
                            else:
                                logger.put({"text":"未知参数类型，使用bool模式","level":"warning"})
                                value=bool(vrcaction.get("vrcValue"))
                            self.osc_client.send_message(vrcaction.get("vrcPath"),value)
                            time.sleep( float(vrcaction.get("sleeptime")) if vrcaction.get("sleeptime") is not None else 0.1)
                        pyttsx3.speak(f"触发命令 {script["action"]}")