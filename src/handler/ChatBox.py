import time
from .base_handler import BaseHandler
from .Color import Colors
import traceback
def sendClientMessage(params,oscClient,logger):
    oldserverdata=''
    oldclientdata=''
    oldclientsendTime=oldserversendTime=time.time()
    while params['running']:
        serverdata=params.get('serverdata','')
        clientdata=params.get('clientdata','')
        
        if serverdata!='' or clientdata!='':
            if serverdata!='' and oldserverdata!=serverdata:
                oldserverdata=serverdata
                oldserversendTime=time.time()
            if clientdata!='' and oldclientdata!=clientdata:
                oldclientdata=clientdata
                oldclientsendTime=time.time() 
            template=params['config']['chatboxOscMixTemplate']
            now=time.time()
            replacements={
                'serverdata':oldserverdata if now-oldserversendTime<30 and serverdata=='' else serverdata,
                'clientdata':oldclientdata if now-oldclientsendTime<30 and clientdata=='' else clientdata}
            output= template.format(**replacements)
            logger.put({"text":f"复合定时输出:{output}","level":"debug"})
            while True:
                try:
                    oscClient.send_message("/chatbox/input",[ output, True, False])
                    params['serverdata']=''
                    params['clientdata']=''
                    break
                except OSError:
                    logger.put({"text":f"文本框osc发送异常:{traceback.format_exc()}","level":"debug"})
                    time.sleep(1)
        else:time.sleep(0.2)
            
class ChatboxHandler(BaseHandler):
    def __init__(self,logger, osc_client,params):
        import threading
        super().__init__(osc_client)
        self.logger=logger
        self.params=params
        self.timer_thread = threading.Thread(target=sendClientMessage,args=(params,self.osc_client,logger),daemon=True)
        self.timer_thread.start()
    """聊天框处理器"""
    

        
    def handle(self, message: str,runMode:str):
        if runMode == "text": self.sendTextFunction(message)
        if runMode == "translation":self.translateFunction(message)
    def translateFunction(self,res:str):
        text=res['text']
        transtext=res.get('translatedText')
        self.logger.put({"text":f"{Colors.CYAN}输出文字: {transtext}({text}){Colors.END}","level":"info"})
        output=self.replace_multiple_placeholders(self.params['config']['VRCChatboxformat_new'],res)
        self.params['clientdata']=output
        # while True:
        #     try:
        #         self.osc_client.send_message("/chatbox/input",[ output, True, False])
        #         break
        #     except OSError:
        #         time.sleep(0.1)
        #         continue

    def sendTextFunction(self,res:str):
        text=res['text']
        self.logger.put({"text":f"{Colors.CYAN}输出文字: {text}{Colors.END}","level":"info"})
        tempalte=self.params['config']['VRCChatboxformat_text']
        output=self.replace_multiple_placeholders(tempalte,res)
        self.params['clientdata']=output
        # while True:
        #     try:
        #         self.osc_client.send_message("/chatbox/input",[ output, True, False])   
        #         break
        #     except OSError:
        #         time.sleep(0.1)
        #         continue
    
    def replace_multiple_placeholders(self,template: str, replacements: dict) -> str:
        """通过字典替换多个占位符"""
        return template.format(**replacements)