import time
from .base_handler import BaseHandler
from .Color import Colors
class ChatboxHandler(BaseHandler):
    def __init__(self,logger, osc_client,params):
        super().__init__(osc_client)
        self.logger=logger
        self.params=params
    """聊天框处理器"""
        
    def handle(self, message: str,runMode:str):
        if runMode == "text": self.sendTextFunction(message)
        if runMode == "translation":self.translateFunction(message)
    def translateFunction(self,res:str):
        text=res['text']
        transtext=res.get('translatedText')
        self.logger.put({"text":f"{Colors.CYAN}输出文字: {transtext}({text}){Colors.END}","level":"info"})
        output=self.replace_multiple_placeholders(self.params['config']['VRCChatboxformat_new'],res)
        while True:
            try:
                self.osc_client.send_message("/chatbox/input",[ output, True, False])
                break
            except OSError:
                time.sleep(0.1)
                continue

    def sendTextFunction(self,res:str):
        text=res['text']
        self.logger.put({"text":f"{Colors.CYAN}输出文字: {text}{Colors.END}","level":"info"})
        while True:
            try:
                self.osc_client.send_message("/chatbox/input",[ f'{text}', True, False])   
                break
            except OSError:
                time.sleep(0.1)
                continue
    
    def replace_multiple_placeholders(self,template: str, replacements: dict) -> str:
        """通过字典替换多个占位符"""
        return template.format(**replacements)