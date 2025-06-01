def once(audioQueue,sendClient,params,logger,filter,mode,steamvrQueue,customEmoji:dict,outputList,ttsVoice):
    import requests
    import time
    import translators
    import html
    import traceback
    from ..handler.DefaultCommand import DefaultCommand
    from ..handler.ChatBox import ChatboxHandler
    from ..handler.Avatar import AvatarHandler
    from ..handler.VRCBitmapLedHandler import VRCBitmapLedHandler
    from ..handler.SelfRead import SelfReadHandler
    from ..handler.tts import TTSHandler
    from hanziconv import HanziConv
    from ..module.translate import other_trasnlator
    import struct
    from io import BytesIO

    avatar=AvatarHandler(logger=logger,osc_client=sendClient,params=params)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,params=params)
    if mode=="mic":chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,params=params)
    bitMapLed=VRCBitmapLedHandler(logger=logger,osc_client=sendClient,params=params)
    selfRead=SelfReadHandler(logger=logger,osc_client=sendClient,steamvrQueue=steamvrQueue,params=params)
    tts=TTSHandler(logger=logger,params=params,mode=mode,header=params['headers'],outputList=outputList,ttsVoice=ttsVoice)
    baseurl=params["config"].get('baseurl')
    translator=params["config"].get('translateService')

    while params["running"]:
        try:
            tragetTranslateLanguage2=params["config"].get("targetTranslationLanguage2")
            tragetTranslateLanguage3=params["config"].get("targetTranslationLanguage3")
            tragetTranslateLanguage=params["tragetTranslateLanguage"]
            sourceLanguage=params["sourceLanguage"]
            
            audio=audioQueue.get()

            st=time.time()
            
            changed_rate=16000
            raw_pcm_data = audio.get_raw_data(convert_rate=changed_rate)
            sample_width = audio.sample_width
            
            data_size = len(raw_pcm_data)
            duration = data_size / (changed_rate * 1 * sample_width)
            logger.put({"text":f"{"麦克风" if mode=="mic" else "桌面"}音频输出完毕, opus音频长度：{round(duration,2)} s","level":"info"})
            
            opus_bytes=pcm_to_packaged_opus_stream_opuslib(raw_pcm_data,1,sample_width,changed_rate)
            files = {'file': ('filename', opus_bytes , 'audio/opus')}
            # else:
            #     wav_bytes =audio.get_wav_data()
            #     # 解析 WAV 头部信息
            #     with BytesIO(wav_bytes) as wav_file:
            #         # 读取前 44 字节的 WAV 头部
            #         header = wav_file.read(44)
                    
            #         # 提取关键参数（偏移量参考标准 WAV 格式）
            #         channels = struct.unpack('<H', header[22:24])[0]  # 声道数
            #         sample_rate = struct.unpack('<I', header[24:28])[0]  # 采样率
            #         data_size = struct.unpack('<I', header[40:44])[0]  # 音频数据总字节数

            #     # 计算时长（单位：秒）
            #     duration = data_size / (sample_rate * channels * 2)  # 2 表示 16-bit（2字节）采样
            #     logger.put({"text":f"{"麦克风" if mode=="mic" else "桌面"}音频输出完毕, wav音频长度：{round(duration,2)} s","level":"info"})
            #     files = {'file': ('filename', wav_bytes , 'audio/wav')}
            if params["runmode"] == "control" or params["runmode"] == "text" or params["runmode"] == "bitMapLed":
                url=baseurl+"/whisper/multitranscription"
            elif params["runmode"] == "translation":
                if mode =="cap":
                    tmp=sourceLanguage
                    sourceLanguage=tragetTranslateLanguage
                    tragetTranslateLanguage=tmp
                if params["config"]["translationServer"] == "libre":
                    url=baseurl+"/func/multitranslateToOtherLanguage" if params["config"].get("translateService")=="developer" else baseurl+"/whisper/multitranscription"
                elif params["config"]["translationServer"] == "vllm":
                    url=baseurl+"/func/vllmTest"
                else:
                    url=baseurl+"/func/doubleTransciption"
            else: 
                logger.put({"text":"运行模式异常,运行默认控制模式","level":"debug"})
                params["runmode"] = "control"
                url = baseurl+"/whisper/multitranscription"
            logger.put({"text":f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}","level":"debug"})
            
            
            data = {'targetLanguage': tragetTranslateLanguage,
                    'targetLanguage2': tragetTranslateLanguage2,
                    'targetLanguage3': tragetTranslateLanguage3,
                    'sourceLanguage': "zh" if sourceLanguage=="zt" else  sourceLanguage}
            response = requests.post(url, files=files, data=data, headers=params['headers'])
            # 检查响应状态码
            if response.status_code != 200:
                if response.status_code == 430:
                    res=response.json()
                    logger.put({"text":f"{'桌面音频'if mode=='cap'else'麦克风'}请求过于频繁,触发规则{res.get("limit")}","level":"warning"})
                else:    
                    logger.put({"text":f"{'桌面音频'if mode=='cap'else'麦克风'}服务器数据接收异常:{response.text}","level":"warning"})
                continue
            # 解析JSON响应
            res = response.json()
            logger.put({"text":f"返回数据信息：{res}","level":"debug"})
            if res["text"] =="":
                logger.put({"text":"返回值过滤-服务端规则","level":"info"})
                continue
            if res["text"] in filter:
                logger.put({"text":"返回值过滤-自定义规则","level":"info"})
                continue
            
            if sourceLanguage== "zh":res["text"]=HanziConv.toSimplified(res["text"])
            elif sourceLanguage=="zt":res["text"]=HanziConv.toTraditional(res["text"])
            et0=time.time()
            if params["runmode"] == "translation" and params["config"].get("translateService")!="developer":
                res['translatedText2']=''
                res['translatedText3']=''
                try:
                    logger.put({"text":f"restext:{res["text"]}","level":"debug"})
                    res['translatedText']=html.unescape(translators.translate_text(res["text"],translator=translator,from_language=sourceLanguage,to_language=tragetTranslateLanguage))
                except Exception as e:
                    if all(i in str(e) for i in["from_language[","] and to_language[","] should not be same"]):
                        logger.put({"text":f"翻译语言检测同语言：{e}","level":"debug"})
                        res['translatedText']=res["text"]
                    else:
                        logger.put({"text":f"翻译异常,请尝试更换翻译引擎：{e};","level":"error"})
                        logger.put({"text":f"翻译异常：{traceback.format_exc()}","level":"debug"})
                        res['translatedText']=''

            if params["runmode"] == "translation" and mode=="mic" and params["config"].get("translateService")!="developer":
                # 第二语言
                if  tragetTranslateLanguage2!="none":
                    res['translatedText2']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage2,res)
                # 第三语言
                if tragetTranslateLanguage3!="none":
                    res['translatedText3']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage3,res)
                        
            et=time.time()
            if params["config"].get("translateService")!="developer":
                logger.put({"text":f"识别用时：{round(et0-st,2)}s，翻译用时：{round(et-et0,2)}s 识别结果: " + res["text"],"level":"info"})
            else:
                logger.put({"text":f"服务器识别+翻译用时：{round(et-st,2)}s 识别结果: " + res["text"],"level":"info"})
            if mode=="cap":selfRead.handle(res,"桌面音频",params["steamReady"])
            else:
                if defaultCommand.handle(res["text"],params=params):continue
                if params["runmode"] == "text" or params["runmode"] == "translation": 
                    selfRead.handle(res,"麦克风",params["steamReady"])
                    for key in list(customEmoji.keys()):res['text']=res['text'].replace(key,customEmoji[key])
                    if params["runmode"] == "translation" : 
                        for key in list(customEmoji.keys()):res['translatedText']=res['translatedText'].replace(key,customEmoji[key])
                    if not params["config"].get("oscShutdown"):chatbox.handle(res,runMode=params["runmode"])
                    if params["config"].get("TTSToggle")==3:
                        tts.tts_audio(res['translatedText'],language=tragetTranslateLanguage)
                    if params["config"].get("TTSToggle")==1 and mode == 'mic' and params["runmode"] == "translation" :
                        tts.tts_audio(res['translatedText'],language=tragetTranslateLanguage)
                    if params["config"].get("TTSToggle")==2 and mode == 'mic'and params["runmode"] == "text" :
                        tts.tts_audio(res['text'],language=sourceLanguage)
                if params["runmode"] == "control":avatar.handle(res)
                if params["runmode"] == "bitMapLed":bitMapLed.handle(res,params=params)
            et=time.time()

            logger.put({"text":f"服务器识别总用时：{round(et-st,2)}s, 音频长度：{duration} s","level":"debug"})

        except requests.JSONDecodeError:
            logger.put({"text":"json解析异常,code:"+str(response.status_code)+" info:"+response.text,"level":"warning"})
            continue
        except Exception as e:
            logger.put({"text":"once未知异常"+str(e),"level":"error"})
            continue
def change_run(params,logger,mode):
    key="voiceKeyRun"if mode=="mic" else "gameVoiceKeyRun"
    params[key]=not params[key]
    logger.put({"text":f"{"麦克风" if mode=="mic" else "桌面音频"}状态：{"打开" if params[key] else "关闭"}","level":"info"})

def clearVRCBitmapLed(client,params,logger):
    import time
    logger.put({"text":f"开始清空点阵屏","level":"info"})

    if "clear" not in params["VRCBitmapLed_taskList"]:params["VRCBitmapLed_taskList"].append("clear")
    else:return
    while params["VRCBitmapLed_taskList"][0]!="clear":
        if "clear" not in params["VRCBitmapLed_taskList"]:return
        time.sleep(0.1)
    num=(8 if params["config"].get("VRCBitmapLed_row") is None else params["config"].get("VRCBitmapLed_row") )*(16 if params["config"].get("VRCBitmapLed_col") is None else params["config"].get("VRCBitmapLed_col"))
    if num==128:
        for i in range(num):

            if params["VRCBitmapLed_taskList"][0]!="clear":return
            client.send_message("/avatar/parameters/BitmapLed/Pointer", i)
            client.send_message(f"/avatar/parameters/BitmapLed/Data", 0)
            client.send_message(f"/avatar/parameters/BitmapLed/DataX16", 0)
            params["VRCBitmapLed_Line_old"]=params["VRCBitmapLed_Line_old"][:i+1]+" "+params["VRCBitmapLed_Line_old"][i+2:]
            time.sleep(0.2)
    elif num==256:
        client.send_message("/avatar/parameters/BitmapLed/Pointer", 255)
        client.send_message(f"/avatar/parameters/BitmapLed/Data", 4)
        client.send_message(f"/avatar/parameters/BitmapLed/DataX16", 0)
    params["VRCBitmapLed_taskList"].pop(0)
    logger.put({"text":f"清空点阵屏完成","level":"info"})

def selfMic_listen(sendClient,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji,outputList,ttsVoice):
    import speech_recognition as sr
    from multiprocessing import Process,Queue
    from pynput import keyboard
    from functools import partial
    import time
    import pyttsx3
    if params["config"].get("micName")== "" or params["config"].get("micName") is None or params["config"].get("micName")== "default":
        logger.put({"text":"使用系统默认麦克风","level":"info"})
        micIndex=defautMicIndex
    else:
        try:
            micIndex=micList.index(params["config"].get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前麦克风：{micList[micIndex]}","level":"info"})
    r = sr.Recognizer()
    m = sr.Microphone(device_index=micIndex)
    params["voiceKeyRun"]=True 
    voiceMode=params["config"].get("voiceMode")
    dynamicVoice=params["config"].get("dynamicThreshold")
    r.dynamic_energy_threshold=False if dynamicVoice is None or dynamicVoice == False else True
    customthreshold=params["config"].get("customThreshold")
    voiceHotKey=params["config"].get("voiceHotKey_new")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["voiceKeyRun"]=False 
        keyThread=keyboard.GlobalHotKeys({voiceHotKey:partial(change_run,params,logger,"mic")})
        keyThread.start()
        logger.put({"text":f"当前麦克风状态：{"打开" if params["voiceKeyRun"] else "关闭"}","level":"info"})
    elif voiceMode == 2 and voiceHotKey is not None:#按住说话
        from ..core.keypress import VKeyHandler
        params["voiceKeyRun"]=False 
        keyThread = VKeyHandler(params,"voiceKeyRun")
        keyThread.start()
        logger.put({"text":f"按住说话已开启，请按住v键说话","level":"info"})
    
    if customthreshold is None or not isinstance(customthreshold, (int, float)) or dynamicVoice:
        logger.put({"text":"开始音量测试","level":"info"})
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        logger.put({"text":"结束音量测试","level":"info"})
    else:
        r.energy_threshold=32768.0*customthreshold

    logger.put({"text":"sound process started complete||音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("麦克风音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    count=0
    audioQueue=Queue(-1)
    p = Process(target=once,daemon=True, args=(audioQueue,sendClient,params,logger,filter,"mic",steamvrQueue,customEmoji,outputList,ttsVoice))
    p.start()
    try:
        with m as s:
            while params["running"]:
                if not params["voiceKeyRun"]:continue
                try:  # listen for 1 second, then check again if the stop function has been called
                    audio = r.listen(s, 10,10)
                    count=0
                except sr.WaitTimeoutError:  # listening timed out, just try again
                    if params["runmode"] == "bitMapLed":
                        if count>=2:
                            pt = Process(target=clearVRCBitmapLed,daemon=True, args=(sendClient,params,logger))
                            pt.start()
                        else:count+=1
                else:
                    # with open(f'{time.time()}-file.wav', 'wb') as file:
                    #     file.write(audio.get_raw_data())
                        
                    if params["running"] and  (params["voiceKeyRun"] or voiceMode==2 ):audioQueue.put(audio)
    finally:
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||麦克风音频进程退出完毕","level":"info"})
        params["micStopped"]=True

# TODO 检查调用错误
def gameMic_listen_VoiceMeeter(sendClient,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji,outputList,ttsVoice):
    import speech_recognition as sr
    from multiprocessing import Process,Queue
    from pynput import keyboard
    from functools import partial
    import time
    import pyttsx3

    if params["config"].get("gameMicName")== "" or params["config"].get("gameMicName") is None :
        logger.put({"text":"请指定游戏麦克风，游戏麦克风线程退出","level":"warning"})
        return
    else:
        try:
            micIndex=micList.index(params["config"].get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定游戏麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前游戏麦克风：{micList[micIndex]}","level":"info"})
    r = sr.Recognizer()
    m = sr.Microphone(device_index=micIndex)
    params["gameVoiceKeyRun"]=True 
    voiceMode=params["config"].get("voiceMode")
    dynamicVoice=params["config"].get("dynamicThreshold")
    r.dynamic_energy_threshold=False if dynamicVoice is None or dynamicVoice == False else True
    customthreshold=params["config"].get("gameCustomThreshold")
    voiceHotKey=params["config"].get("gameVoiceHotKey_new")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["gameVoiceKeyRun"]=False 
        keyThread=keyboard.GlobalHotKeys({voiceHotKey:partial(change_run,params,logger,"cap")})
        keyThread.start()
        logger.put({"text":f"当前游戏麦克风状态：{"打开" if params["gameVoiceKeyRun"] else "关闭"}","level":"info"})
    elif voiceMode == 2 and voiceHotKey is not None:#按住说话
        from .keypress import VKeyHandler
        params["gameVoiceKeyRun"]=False 
        keyThread = VKeyHandler(params,"gameVoiceKeyRun")
        keyThread.start()
        logger.put({"text":f"按住说话已开启，请按住v键说话","level":"info"})
    
    if customthreshold is None or not isinstance(customthreshold, (int, float)) or dynamicVoice:
        logger.put({"text":"开始音量测试","level":"info"})
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        logger.put({"text":"结束音量测试","level":"info"})
    else:
        r.energy_threshold=32768.0*customthreshold

    logger.put({"text":"sound process started complete||游戏音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("游戏音频进程启动完毕")
    except:pass
    count=0
    audioQueue=Queue(-1)
    p = Process(target=once,daemon=True, args=(audioQueue,sendClient,params,logger,filter,"cap",steamvrQueue,customEmoji,outputList,ttsVoice))
    p.start()
    try:
        with m as s:
            while params["running"]:
                if not params["gameVoiceKeyRun"]:continue
                try:  # listen for 1 second, then check again if the stop function has been called
                    audio = r.listen(s, 10,10)
                    count=0
                except sr.WaitTimeoutError:  # listening timed out, just try again
                    if params["runmode"] == "bitMapLed":
                        if count>=2:
                            pt = Process(target=clearVRCBitmapLed,daemon=True, args=(sendClient,params,logger,"vm"))
                            pt.start()
                        else:count+=1
                else:
                    if params["running"] and  (params["gameVoiceKeyRun"] or voiceMode==2 ):audioQueue.put(audio)
    finally:
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||游戏音频进程退出完毕","level":"info"})
        params["gameStopped"] = True

def gameMic_listen_capture(sendClient,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji,outputList,ttsVoice):
    import speech_recognition as sr
    from multiprocessing import Process,Queue
    from pynput import keyboard
    from functools import partial
    import time
    import pyttsx3

    from .recordLocal import voice_activation_stream
    if params["config"].get("gameMicName")== "" or params["config"].get("gameMicName") is None or params["config"].get("gameMicName")== "default":
        logger.put({"text":"使用系统默认桌面音频","level":"info"})
        micIndex=None
    else:
        device_index=False
        for i in micList:
            if params["config"].get("gameMicName")==i.get("name"):
                device_index=True
                micIndex=i.get('index')
                logger.put({"text":f"当前桌面音频：{params["config"].get("gameMicName")}","level":"info"})
                break
        
            
        if not device_index:
            logger.put({"text":"无法找到指定桌面音频，使用系统默认桌面音频","level":"info"})
            micIndex=None
    params["gameVoiceKeyRun"]=True 
    voiceMode=params["config"].get("gameVoiceMode")
    customthreshold=params["config"].get("gameCustomThreshold")
    voiceHotKey=params["config"].get("gameVoiceHotKey_new")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["gameVoiceKeyRun"]=False 
        keyThread=keyboard.GlobalHotKeys({voiceHotKey:partial(change_run,params,logger,"cap")})
        keyThread.start()
        logger.put({"text":f"当前桌面音频捕获状态状态：{"打开" if params["gameVoiceKeyRun"] else "关闭"}","level":"info"})
    elif voiceMode == 2 and voiceHotKey is not None:#按住说话
        from .keypress import VKeyHandler
        params["gameVoiceKeyRun"]=False 
        keyThread = VKeyHandler(params,"gameVoiceKeyRun")
        keyThread.start()
        logger.put({"text":f"按住说话已开启，请按住v键说话","level":"info"})
    energy_threshold=32768.0*customthreshold

    logger.put({"text":"sound process started complete||桌面音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("桌面音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    count=0
    audioQueue=Queue(-1)
    p = Process(target=once,daemon=True, args=(audioQueue,sendClient,params,logger,filter,"cap",steamvrQueue,customEmoji,outputList,ttsVoice))
    p.start()
    try:
        while params["running"]:
            if not params["gameVoiceKeyRun"]:continue
            try:  # listen for 1 second, then check again if the stop function has been called
                audio = voice_activation_stream(
                    logger=logger,
                    micIndex=micIndex,
                    params=params,
                    silence_threshold=int(energy_threshold),
                    maxAudioLen=10.0
                )
                count=0
            except sr.WaitTimeoutError:  # listening timed out, just try again
                if params["runmode"] == "bitMapLed":
                    if count>=2:
                        pt = Process(target=clearVRCBitmapLed,daemon=True, args=(sendClient,params,logger))
                        pt.start()
                    else:count+=1
            else:
                    if params["running"] and (params["gameVoiceKeyRun"] or voiceMode==2 ):audioQueue.put(audio)
    finally:
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||桌面音频进程退出完毕","level":"info"})
        params["gameStopped"] = True

def logger_process(queue, copyqueue, params, socketQueue):
    from .logger import MyLogger
    import sqlite3
    import datetime
    import traceback

    logger = MyLogger().logger

    # 初始化数据库连接
    conn = sqlite3.connect('log_statistics.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # 创建统计表（如果不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_stats
                     (date TEXT PRIMARY KEY, count INTEGER DEFAULT 0)''')
    conn.commit()
    # 创建统计表（如果不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_fail_stats
                     (date TEXT PRIMARY KEY, count INTEGER DEFAULT 0)''')
    conn.commit()
    # 定义需要统计的关键词列表
    keyweod_list = ["返回值过滤-","服务器翻译成功："]
    localizedSpeech=None
    localizedCapture=None
    TTSToggle=None
    
    infoType={
        "麦克风识别结果：":'mic',
        "桌面音频识别结果：":'cap',
        "桌面音频请求过于频繁,可以尝试更换其他翻译引擎,触发规则":'cap',
        "麦克风请求过于频繁,可以尝试更换其他翻译引擎,触发规则":'mic',
        '桌面音频请求过于频繁,触发规则':'cap',
        "麦克风请求过于频繁,触发规则":'mic',
        '桌面音频本地识别服务器翻译数据接收异常:':'cap',
        '麦克风本地识别服务器翻译数据接收异常:':'mic',
        '桌面音频服务器数据接收异常:':'cap',
        '麦克风服务器数据接收异常:':'mic',
        'TTS请求过于频繁,触发规则':'mic',
        "TTS数据接收异常:":'mic'
    }
    try:
        while True:
            text = queue.get()
            if localizedSpeech != params.get("localizedSpeech"):
                localizedSpeech=params.get("localizedSpeech")
                if not localizedSpeech: keyweod_list.append("服务器识别总用时：")
                else:
                    try:keyweod_list.remove("服务器识别总用时：")
                    except:pass
            if localizedCapture != params.get("localizedCapture"):
                localizedCapture=params.get("localizedCapture")
                if not localizedCapture: keyweod_list.append("桌面音频识别结果：")
                else:
                    try:keyweod_list.remove("桌面音频识别结果：")
                    except:pass
            if TTSToggle != params.get("TTSToggle"):
                TTSToggle=params.get("TTSToggle")
                if TTSToggle!=0: keyweod_list.append("TTS文本生成: ")
                else:
                    try:keyweod_list.remove("TTS文本生成: ")
                    except:pass
            # 原有的复制逻辑
            for txt in infoType.keys():
                if txt in text['text']:
                    tmp_text=text['text'].split(txt, 1)[1].strip()
                    if params['running']:
                        socketQueue.put({'type':infoType[txt],'text':tmp_text[:len(tmp_text)-4] if '识别结果' in txt else text['text']})
            
            today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
            # 新增的统计逻辑
            if any(keyword in text['text'] for keyword in keyweod_list):
                
                try:
                    # 使用UPSERT语法更新统计
                    cursor.execute('''INSERT INTO daily_stats (date, count) 
                                    VALUES (?, 1)
                                    ON CONFLICT(date) 
                                    DO UPDATE SET count = count + 1''', (today,))
                    conn.commit()
                except Exception as e:
                    logger.error(f"数据库更新失败: {str(e)}")
                    conn.rollback()
            if any(keyword in text['text'] for keyword in ["请求过于频繁,触发规则","数据接收异常:"]):
                
                try:
                    # 使用UPSERT语法更新统计
                    cursor.execute('''INSERT INTO daily_fail_stats (date, count) 
                                    VALUES (?, 1)
                                    ON CONFLICT(date) 
                                    DO UPDATE SET count = count + 1''', (today,))
                    conn.commit()
                except Exception as e:
                    logger.error(f"数据库更新失败: {str(e)}")
                    conn.rollback()

            # 原有的日志记录逻辑
            log_level = text['level']
            log_content = text['text']
            {
                "debug": logger.debug,
                "info": logger.info,
                "warning": logger.warning,
                "error": logger.error
            }.get(log_level, logger.error)(log_content)
            if log_level!="debug" and params['running']:socketQueue.put({
                        'type':'log',
                        'text': text['text'],
                        'level': text['level'],
                        'timestamp': datetime.datetime.now().isoformat()
                    })
    except Exception:
        logger.error(f'日志进程报错：{traceback.format_exc()}')

def steamvr_process(logger, queue, params):
    import time
    import openvr
    from ..module.steamvr import VRTextOverlay
    textOverlay = VRTextOverlay()
    MAX_RETRIES = 10  # 最大重试次数
    retry_count = 0
    is_two_hand=params["config"].get("SteamVRHad")==2
    def safe_shutdown():
        try:
            if textOverlay.overlay_handle:
                textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
                textOverlay.overlay.destroyOverlay(textOverlay.overlay_handle)
            # openvr.shutdown()
            logger.put({"text":"VR资源已安全释放","level":"info"})
        except Exception as e:
            logger.put({"text":f"关闭资源时出错:{str(e)}","level":"error"})

    try:
        # 带重试的初始化
        while retry_count < MAX_RETRIES and params['running']:
            try:
                if not textOverlay.initialize(logger, params):
                    raise RuntimeError("SteamVR初始化失败")
                # logger.put({"text":"SteamVR初始化成功","level":"info"})
                last_success = time.time()
                check_interval = 10  # 手柄状态检查间隔
                error_count = 0
                retry_count=0
                MAX_ERRORS = 5  # 最大连续错误次数
                textOverlay._create_text_texture()
                textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle,params["config"].get("SteamVRSize")*(1.5 if params["config"].get("Separate_Self_Game_Mic")!=0 else 1.0))
                textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
                if is_two_hand:
                    textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle_1,params["config"].get("SteamVRSize")*(1.5 if params["config"].get("Separate_Self_Game_Mic")!=0 else 1.0))
                    textOverlay.overlay.showOverlay(textOverlay.overlay_handle_1)
                logger.put({"text":f"掌心显示启动完毕","level":"info"})
                # 主循环
                while params['running']:
                    try:
                        # 定期设备检查
                        if time.time() - last_success > check_interval:
                            
                            if params["config"].get("SteamVRHad") ==2:
                                current_status = textOverlay.set_overlay_to_hand(0) and textOverlay.set_overlay_to_hand(1,True)
                            else:
                                current_status = textOverlay.set_overlay_to_hand(params["config"].get("SteamVRHad"))
                                

                            if not current_status:
                                logger.put({"text":"控制器连接状态异常，尝试恢复...","level":"debug"})
                                textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
                                if is_two_hand:textOverlay.overlay.hideOverlay(textOverlay.overlay_handle_1)
                                time.sleep(1)
                                textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
                                if params["config"].get("SteamVRHad") ==2:
                                    textOverlay.overlay.showOverlay(textOverlay.overlay_handle_1)
                                    status_tmp = textOverlay.set_overlay_to_hand(0) and textOverlay.set_overlay_to_hand(1,True)
                                else:
                                    status_tmp = textOverlay.set_overlay_to_hand(params["config"].get("SteamVRHad"))
                             
                                if status_tmp:
                                    last_success = time.time()
                                    logger.put({"text":"控制器连接恢复成功","level":"info"})
                                else: continue
                            else:
                                last_success = time.time()
                            
                        error=0
                        # 处理消息队列
                        if not queue.empty():
                            text = queue.get()
                            logger.put({"text":f"开始处理新的文本更新","level":"debug"})
                            
                            
                            # 带重试的更新操作
                            for _ in range(3):  # 最多重试3次
                                try:
                                    textOverlay.update_text(text)
                                    error=200
                                    break
                                except openvr.openvr.error_code.OverlayError_RequestFailed:
                                    logger.put({"text":f"[steamvr异常]OpenVR错误: {str(type(oe))}，尝试恢复初始化,{error}","level":"debug"})
                                    safe_shutdown()
                                    time.sleep(5)
                                    if not textOverlay.initialize(logger, params):
                                        raise RuntimeError("[steamvr异常]SteamVR初始化失败")
                                    time.sleep(1)
                                    textOverlay._create_text_texture()  # 重新创建纹理
                                    time.sleep(1)
                                except openvr.error_code.OverlayError as oe:
                                    error+=1
                                    logger.put({"text":f"[steamvr异常]OpenVR错误: {str(type(oe))}，尝试恢复...,{error}","level":"debug"})
                                    textOverlay._create_text_texture()  # 重新创建纹理
                                    time.sleep(1)
                                    
                            
                            # 强制更新Overlay属性
                            textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle, params["config"].get("SteamVRSize")*(1.0 if params["config"].get("Separate_Self_Game_Mic")==0 or params["config"].get("SteamVRHad") ==2 else 1.5))
                            textOverlay.overlay.setOverlayAlpha(textOverlay.overlay_handle, 1.0)
                            if params["config"].get("SteamVRHad") ==2:
                                # 强制更新Overlay属性
                                textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle_1, params["config"].get("SteamVRSize")*(1.0 if params["config"].get("Separate_Self_Game_Mic")==0 or params["config"].get("SteamVRHad") ==2 else 1.5))
                                textOverlay.overlay.setOverlayAlpha(textOverlay.overlay_handle_1, 1.0)
                        time.sleep(0.1)
                        if error ==200:error_count = 0  # 重置错误计数器

                    except Exception as inner_e:
                        error_count += 1
                        logger.put({"text":f"[steamvr异常][运行时错误] {str(type(inner_e))} ({error_count}/{MAX_ERRORS})","level":"debug"})
                        if error_count >= MAX_ERRORS:
                            logger.put({"text":"[steamvr异常]达到最大错误次数，尝试重新初始化...","level":"error"})
                            safe_shutdown()
                            time.sleep(5)
                            break  # 退出内层循环进行重新初始化

                # 正常退出循环
                if not params['running']:
                    break

            except Exception as init_e:
                retry_count += 1
                logger.put({"text":f"[steamvr异常]初始化失败 ({retry_count}/{MAX_RETRIES}): {str(type(init_e))}","level":"error"})
                safe_shutdown()
                time.sleep(5)  # 指数退避
                
        if retry_count >= MAX_RETRIES:
            logger.put({"text":"[steamvr异常]达到最大重试次数，SteamVR功能终止","level":"error"})

    except Exception as outer_e:
        logger.put({"text":f"[steamvr异常][未捕获的异常] {str(type(outer_e))}|| {str(outer_e)}","level":"error"})
    finally:
        safe_shutdown()
        # 确保释放所有VR资源
        # for _ in range(3):
        #     try:
        #         openvr.shutdown()
        #     except:
        #         pass
        #     time.sleep(1)

def copyBox_process(queue):
    import tkinter as tk
    from ..module.copybox import ScrollableListApp
    # 启动GUI
    root = tk.Tk()
    app = ScrollableListApp(root, queue)
    root.geometry("500x400")
    
    # 绑定关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

import opuslib,io,struct
def pcm_to_packaged_opus_stream_opuslib(
    pcm_bytes,
    channels: int,
    sample_width:int,
    sample_rate:int,
    frame_duration_ms: int = 20,
    opus_application: int = opuslib.APPLICATION_AUDIO
) -> bytes:
    """
    将 speech_recognition.AudioData 对象中的 PCM 数据编码为
    带长度前缀的 Opus 包的单一字节流，使用 opuslib。

    每个 Opus 包前会有一个4字节的大端序无符号整数表示该包的长度。

    参数:
        audio_data (speech_recognition.AudioData): 包含 PCM 数据的 AudioData 对象。
        channels (int): 音频的通道数 (1 表示单声道, 2 表示立体声)。
                        AudioData 对象不包含此信息，必须由调用者提供。
        frame_duration_ms (int): Opus 编码器的帧时长，单位毫秒 (例如 20, 40, 60)。
                                 有效值: 2.5, 5, 10, 20, 40, 60。
        opus_application (int): Opus 应用类型 (例如 opuslib.APPLICATION_AUDIO,
                                opuslib.APPLICATION_VOIP,
                                opuslib.APPLICATION_RESTRICTED_LOWDELAY)。

    返回:
        bytes: 包含多个[长度+Opus包]序列的单一字节流。
               如果编码失败或无数据，可能返回空字节串。
    """

    # --- 参数校验 ---
    if not pcm_bytes:
        print("警告: AudioData 不包含原始 PCM 数据。")
        return b''
    if channels not in [1, 2]:
        raise ValueError("通道数必须是 1 (单声道) 或 2 (立体声)。")
    if sample_width != 2:
        # Opus C API (以及 opuslib) 期望的是 16-bit PCM。
        # speech_recognition.AudioData 通常是 sample_width=2。
        raise ValueError(f"Opuslib 需要 16-bit PCM 数据 (sample_width=2)，但 AudioData 的 sample_width 是 {sample_width}。")
    if sample_rate not in [8000, 12000, 16000, 24000, 48000]:
        raise ValueError(f"不支持的采样率: {sample_rate} Hz。Opus 支持 8, 12, 16, 24, 48 kHz。")
    if frame_duration_ms not in [2.5, 5, 10, 20, 40, 60]:
        raise ValueError(f"不支持的帧时长: {frame_duration_ms} ms。")
    valid_applications = [
        opuslib.APPLICATION_VOIP,
        opuslib.APPLICATION_AUDIO,
        opuslib.APPLICATION_RESTRICTED_LOWDELAY
    ]
    if opus_application not in valid_applications:
        raise ValueError(f"不支持的 Opus 应用类型: {opus_application}")

    # --- 初始化 Opus 编码器 ---
    try:
        encoder = opuslib.Encoder(sample_rate, channels, opus_application)
    except opuslib.OpusError as e:
        raise RuntimeError(f"创建 opuslib.Encoder 失败: {e}")
    except Exception as e: # 捕获其他可能的初始化错误
        raise RuntimeError(f"创建 opuslib.Encoder 时发生未知错误: {e}")

    # --- 计算帧参数 ---
    # Opus 编码器期望的每帧每通道的样本数
    samples_per_channel_per_frame = int(sample_rate * frame_duration_ms / 1000)
    # Opus 编码器期望的每帧 PCM 数据的总字节数
    # (每样本字节数 sample_width 已经确认是 2)
    pcm_bytes_per_opus_frame = samples_per_channel_per_frame * channels * sample_width

    # --- 编码过程 ---
    packaged_opus_stream = io.BytesIO()
    offset = 0
    while offset < len(pcm_bytes):
        # 获取当前帧的 PCM 数据
        frame_pcm_segment = pcm_bytes[offset : offset + pcm_bytes_per_opus_frame]

        # 如果是最后一帧且数据不足，需要用静音数据填充到完整帧大小
        if len(frame_pcm_segment) < pcm_bytes_per_opus_frame:
            # 确保不是因为已经处理完所有数据而 frame_pcm_segment 为空
            if not frame_pcm_segment and offset >= len(pcm_bytes):
                break # 所有数据已处理完毕
            
            padding_needed = pcm_bytes_per_opus_frame - len(frame_pcm_segment)
            frame_pcm_segment += b'\x00' * padding_needed # 使用静音填充
        
        # 如果在填充后仍然为空（不太可能发生，除非原始数据为空或计算错误），则跳过
        if not frame_pcm_segment:
            break

        try:
            # 使用 opuslib 进行编码
            # encoder.encode() 的第二个参数是 samples_per_frame (即 samples_per_channel_per_frame)
            encoded_opus_packet = encoder.encode(frame_pcm_segment, samples_per_channel_per_frame)

            # 将 Opus 包的长度（4字节，大端序无符号整数）和包数据写入流
            packaged_opus_stream.write(struct.pack('>I', len(encoded_opus_packet)))
            packaged_opus_stream.write(encoded_opus_packet)

        except opuslib.OpusError as e:
            # 发生编码错误，可以选择记录并跳过此帧，或直接抛出异常
            print(f"警告: Opus 编码错误 (跳过帧): {e}. PCM 段长度: {len(frame_pcm_segment)}")
            # 若要更健壮，可以考虑如何处理这种情况，例如是否停止整个过程
        except Exception as e:
            print(f"警告: Opus 编码时发生未知错误 (跳过帧): {e}")

        offset += pcm_bytes_per_opus_frame
        # 如果最后一帧被填充，并且我们已经处理了所有原始数据，就结束
        if len(frame_pcm_segment) == pcm_bytes_per_opus_frame and offset >= len(pcm_bytes) and \
           pcm_bytes[offset-pcm_bytes_per_opus_frame:] == frame_pcm_segment[:len(pcm_bytes)- (offset-pcm_bytes_per_opus_frame)]:
             pass # 刚好处理完
        elif offset >= len(pcm_bytes) and len(frame_pcm_segment) < pcm_bytes_per_opus_frame: # 处理了最后一小段
            break


    return packaged_opus_stream.getvalue()