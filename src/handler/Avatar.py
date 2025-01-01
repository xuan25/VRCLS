from typing import Optional
from .base_handler import BaseHandler
import winsound
import time
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
            logger.info("无头命令:"+text)
            if text == config["exitText"]:
                running = False
                exit(0)
            for script in config.get("scripts"):
                if any( command in text  for command in script.get("text")):
                    logger.info("执行命令:"+script["action"])
                    for vrcaction in script["vrcActions"]:
                        self.osc_client.sendOSCMesssage(vrcaction.get("vrcPath"),float(vrcaction.get("vrcValue")))
                        time.sleep( float(vrcaction.get("sleeptime")) if vrcaction.get("sleeptime") is not None and vrcaction.get("sleeptime") != ""  else 0.1)
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
        elif config["activateText"] in text:
            commandlist=text.split(config["activateText"])
            command=commandlist[-1]
            if (config["stopText"] in command) or config["stopText"] == "":
                if config["stopText"] != "":command=command.split(config["stopText"])[0]
                logger.info("有头命令:"+command)
                if command == config["exitText"]:
                    running = False
                    exit(0)
                for script in config.get("scripts"):
                    if command in script.get("text"):
                        logger.info("执行命令:"+script.get("action"))
                        for vrcaction in script.get("vrcActions"):
                            self.osc_client.sendOSCMesssage(vrcaction.get("vrcPath"),float(vrcaction.get("vrcValue")))
                            time.sleep( float(vrcaction.get("sleeptime")) if vrcaction.get("sleeptime") is not None else 0.1)
                        winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)