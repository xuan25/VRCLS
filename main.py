from src.core.logger import MyLogger
from src.core.startup import StartUp
from src.handler.DefaultCommand import DefaultCommand
from src.handler.ChatBox import ChatboxHandler
from src.handler.Avatar import AvatarHandler
import speech_recognition as sr
import requests
from multiprocessing import Process,Manager,freeze_support,Queue
import threading
import winsound
import time


def once(audio:sr.AudioData,baseurl,sendClient,config,headers,params,logger):
    tragetTranslateLanguage=params["tragetTranslateLanguage"]
    sourceLanguage=params["sourceLanguage"]
    avatar=AvatarHandler(logger=logger,osc_client=sendClient,config=config)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,config=config)
    chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,config=config)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,config=config)
    try:

        logger.put({"text":"音频输出完毕","level":"info"})
        if params["runmode"] == "control" or params["runmode"] == "text":
            url=baseurl+"/whisper/transcriptions"
        elif params["runmode"] == "translation":
            if tragetTranslateLanguage=="en":url=baseurl+"/func/translateToEnglish"
            elif sourceLanguage != "zh" :url=baseurl+"/func/multitranslateToOtherLanguage"
            else:url=baseurl+"/func/translateToOtherLanguage"
        else: 
            logger.put({"text":"运行模式异常,运行默认控制模式","level":"debug"})
            params["runmode"] = "control"
            url = baseurl+"/whisper/transcriptions"
        logger.put({"text":f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}","level":"debug"})
        files = {'file': ('filename', audio.get_wav_data(), 'audio/wav')}
        data = {'targetLanguage': tragetTranslateLanguage, 'sourceLanguage': sourceLanguage}
        response = requests.post(url, files=files, data=data, headers=headers)
        # 检查响应状态码
        if response.status_code != 200:
            logger.put({"text":f"数据接收异常:{response.text}","level":"warning"})
            return
        # 解析JSON响应
        res = response.json()
        logger.put({"text":"你说的是: " + res["text"],"level":"info"})
        if res["text"] =="":
            logger.put({"text":"返回值过滤","level":"debug"})
            return
        if defaultCommand.handle(res["text"],params=params):return
        if params["runmode"] == "text" or params["runmode"] == "translation": chatbox.handle(res,runMode=params["runmode"])
        if params["runmode"] == "control":avatar.handle(res)
    except requests.JSONDecodeError:
        logger.put({"text":"json解析异常,code:"+str(response.status_code)+" info:"+response.text,"level":"warning"})
        return
    except Exception as e:
        logger.put({"text":e,"level":"warning"})
        return
def threaded_listen(baseurl,sendClient,config,headers,params,logger):
    # logger=MyLogger().logger
    r = sr.Recognizer()
    m = sr.Microphone()
    logger.put({"text":"开始音量测试","level":"info"})
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    logger.put({"text":"结束音量测试","level":"info"})
    logger.put({"text":"program started complete||程序启动完毕","level":"info"})
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
    with m as s:
        while params["running"]:
            try:  # listen for 1 second, then check again if the stop function has been called
                audio = r.listen(s, 10)
            except sr.WaitTimeoutError:  # listening timed out, just try again
                pass
            else:
                if params["running"]:
                    p = Process(target=once,daemon=True, args=(audio,baseurl,sendClient,config,headers,params,logger))
                    p.start()

if __name__ == '__main__':
    queue=Queue(-1)
    freeze_support()
    manager = Manager()
    params=manager.dict()

    logger=MyLogger().logger
    logger.info('''
                          
    欢迎使用由VoiceLinkVR开发的VRCLS
    本程序的开发这为boyqiu-001(boyqiu玻璃球)
    欢迎大家加入qq群1011986554获取最新资讯
    目前您使用的时公测账户,限制每日2000次请求
    如需获取更多资源请加群
                '''
                )

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

    listener_thread = Process(target=threaded_listen,args=(baseurl,sendClient,startUp.config,headers,params,queue))
    listener_thread.start()


    


    # stop_listening = r.listen_in_background(m, callback)


    # `stop_listening` is now a function that, when called, stops background listening
    try:
        while params["runmode"]:
            text=queue.get()
            if text['level']=="debug":logger.debug(text['text'])
            elif text['level']=="info":logger.info(text['text'])
            elif text['level']=="warning":logger.warning(text['text'])
            elif text['level']=="error":logger.error(text['text'])
            else :logger.warning(text)
    except Exception:
        listener_thread.kill()