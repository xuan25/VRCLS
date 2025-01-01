from .base_handler import BaseHandler
import winsound
class DefaultCommand(BaseHandler):
    def __init__(self,logger, osc_client,config):
        super().__init__(osc_client)
        self.defaultScripts=config["defaultScripts"]
        self.logger=logger
    def handle(self,text,params):
        params["runmode"]
        for dafaultcommand in self.defaultScripts:
            if any( command in text for command in dafaultcommand["text"]):
                if dafaultcommand["action"]=="sendText":
                    if params["runmode"] =="text":
                        self.logger.info("No need to modify mode. Currently in sendText mode ||无需修改模式 当前处于发送文字模式")
                        return False
                    self.logger.info("change to sendText mode ||切换至发送文字模式")
                    params["runmode"]="text"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
                if dafaultcommand["action"]=="changToTrans":
                    if params["runmode"] =="translation":
                        self.logger.info("No need to modify mode. Currently in translation mode ||无需修改模式 当前处于翻译模式")
                        return False
                    self.logger.info("change to translation mode ||切换至翻译模式")
                    params["runmode"]="translation"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
                if dafaultcommand["action"]=="changToControl":
                    if params["runmode"] =="control":
                        self.logger.info("No need to change mode. Currently in control mode ||无需修改模式 当前处于控制模式")
                        return False
                    self.logger.info("change to control mode ||切换至控制模式")
                    params["runmode"]="control"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
                if dafaultcommand["action"]=="changToEnglish":
                    if params["tragetTranslateLanguage"] == "en":
                        self.logger.info("No need to change mode. Currently in english translation||无需修改模式 当前翻译输出语言为 英语")
                        return False
                    self.logger.info("change translation to english ||将翻译切换为英语")
                    params["tragetTranslateLanguage"]="en"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
                if dafaultcommand["action"]=="changTojapanese":
                    if params["tragetTranslateLanguage"] =="ja":
                        self.logger.info("No need to change mode. Currently in english translation||无需修改模式 当前翻译输出语言为 日语")
                        return False
                    self.logger.info("change translation to japanese ||将翻译切换为日语")
                    params["tragetTranslateLanguage"]="ja"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
                if dafaultcommand["action"]=="changToRussian":
                    if params["tragetTranslateLanguage"] =="ru":
                        self.logger.info("No need to change mode. Currently in russian translation||无需修改模式 当前翻译输出语言为 俄语")
                        return False
                    self.logger.info("change translation to russian ||将翻译切换为俄语")
                    params["tragetTranslateLanguage"]="ru"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
                if dafaultcommand["action"]=="changToKorean":
                    if params["tragetTranslateLanguage"] =="ko":
                        self.logger.info("No need to change mode. Currently in Korean translation||无需修改模式 当前翻译输出语言为 韩语")
                        return False
                    self.logger.info("change translation to Korean ||将翻译切换为韩语")
                    params["tragetTranslateLanguage"]="ko"
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                    return True
        return False