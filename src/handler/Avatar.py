from typing import Optional
from .base_handler import BaseHandler
import time
import pyttsx3
class AvatarHandler(BaseHandler):
    def __init__(self,logger, osc_client,params):
        super().__init__(osc_client)
        self.params=params
        self.logger=logger
    """聊天框处理器"""
        
    def handle(self, message: str):
        self.controlFunction(message)
    def controlFunction(self,res):
        logger=self.logger
        text=res['text']
        global running
        if self.params["config"]["activateText"] == "":
            logger.put({"text":"无头命令:"+text,"level":"info"})
            for script in self.params["config"].get("scripts"):
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
                    try:pyttsx3.speak(f"触发命令 {script['action']}")
                    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
        elif self.params["config"]["activateText"] in text:
            commandlist=text.split(self.params["config"]["activateText"])
            command=commandlist[-1]
            if (self.params["config"]["stopText"] in command) or self.params["config"]["stopText"] == "":
                if self.params["config"]["stopText"] != "":command=command.split(self.params["config"]["stopText"])[0]
                logger.put({"text":"有头命令:"+command,"level":"info"})
                for script in self.params["config"].get("scripts"):
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
                        try:pyttsx3.speak(f"触发命令 {script['action']}")
                        except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})