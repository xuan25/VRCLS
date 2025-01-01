from src.core.logger import MyLogger
from src.core.startup import StartUp
from src.handler.DefaultCommand import DefaultCommand
from src.handler.ChatBox import ChatboxHandler
from src.handler.Avatar import AvatarHandler
import speech_recognition as sr
import requests
from multiprocessing import Process,Manager
import threading
import winsound
import time


def once(audio:sr.AudioData,baseurl,sendClient,config,headers,params):
    logger=MyLogger().logger
    tragetTranslateLanguage=params["tragetTranslateLanguage"]
    sourceLanguage=params["sourceLanguage"]
    avatar=AvatarHandler(logger=logger,osc_client=sendClient,config=config)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,config=config)
    chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,config=config)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,config=config)
    try:

        logger.debug("音频输出完毕")
        if params["runmode"] == "control" or params["runmode"] == "text":
            url=baseurl+"/whisper/transcriptions"
        elif params["runmode"] == "translation":
            if tragetTranslateLanguage=="en":url=baseurl+"/func/translateToEnglish"
            elif sourceLanguage != "zh" :url=baseurl+"/func/multitranslateToOtherLanguage"
            else:url=baseurl+"/func/translateToOtherLanguage"
        else: 
            logger.error("运行模式异常,运行默认控制模式")
            params["runmode"] = "control"
            url = baseurl+"/whisper/transcriptions"
        logger.debug(f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}")
        files = {'file': ('filename', audio.get_wav_data(), 'audio/wav')}
        data = {'targetLanguage': tragetTranslateLanguage, 'sourceLanguage': sourceLanguage}
        response = requests.post(url, files=files, data=data, headers=headers)
        # 检查响应状态码
        if response.status_code != 200:
            logger.warning(f"数据接收异常:{response.text}")
            return
        # 解析JSON响应
        res = response.json()
        logger.debug("你说的是: " + res["text"])
        if res["text"] =="":
            logger.debug("返回值过滤")
            return
        if defaultCommand.handle(res["text"],params=params):return
        if params["runmode"] == "text" or params["runmode"] == "translation": chatbox.handle(res,runMode=params["runmode"])
        if params["runmode"] == "control":avatar.handle(res)
    except requests.JSONDecodeError:
        logger.warning("json解析异常,code:"+str(response.status_code)+" info:"+response.text)
        return
    except Exception as e:
        logger.warning(e)
        return
def threaded_listen(baseurl,sendClient,config,headers,params):
    logger=MyLogger().logger
    r = sr.Recognizer()
    m = sr.Microphone()
    logger.info("开始音量测试")
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    logger.info("结束音量测试")
    logger.info("program started complete||程序启动完毕")
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
    with m as s:
        while params["running"]:
            try:  # listen for 1 second, then check again if the stop function has been called
                audio = r.listen(s, 10)
            except sr.WaitTimeoutError:  # listening timed out, just try again
                pass
            else:
                if params["running"]:
                    p = Process(target=once,daemon=True, args=(audio,baseurl,sendClient,config,headers,params))
                    p.start()
if __name__ == '__main__':
    manager = Manager()
    params=manager.dict()

    logger=MyLogger().logger
    logger.info("欢迎使用由VoiceLinkVR开发的VRCLS\n本程序的开发这为boyqiu-001(boyqiu玻璃球)\n欢迎大家加入qq群1011986554获取最新资讯\n\n")

    params["running"] = True


    startUp=StartUp(logger)
    headers=startUp.run()
    sendClient= startUp.setOSCClient(logger)
    baseurl=startUp.config.get("baseurl")

    params["tragetTranslateLanguage"]=startUp.tragetTranslateLanguage
    params["sourceLanguage"]=startUp.sourceLanguage

    logger.info("vrc udpClient ok||发送准备就绪")
    params["runmode"]= startUp.config["defaultMode"]

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    # this is called from the background thread

    listener_thread = Process(target=threaded_listen,args=(baseurl,sendClient,startUp.config,headers,params))
    listener_thread.start()


    


    # stop_listening = r.listen_in_background(m, callback)


    # `stop_listening` is now a function that, when called, stops background listening
    try:
        while params["runmode"]:time.sleep(0.00001)
    except KeyboardInterrupt:
        listener_thread.kill()