
def change_run_local(params,logger,mode):
    key="voiceKeyRun"if mode=="mic" else "gameVoiceKeyRun"
    params[key]=not params[key]
    logger.put({"text":f"{'麦克风' if mode=='mic' else '桌面音频'}状态：{'打开' if params[key] else '关闭'}","level":"info"})

def create_recognizer(logger,source):
    import sherpa_onnx
    import os,sys
    from pathlib import Path
    import unicodedata
    
    def contains_chinese_chars(path):
        for char in str(path):
            if unicodedata.name(char).startswith('CJK'):  # 检查是否为CJK字符，包括中文
                return True
        return False
    
        # 2. 动态路径注入（核心防护）
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))  # 适配 src/core 的层级
    if contains_chinese_chars(base_dir):
        logger.put({"text": f"路径存在中文，请修改VRCLS安装位置。当前路径：{base_dir}", "level": "error"})
        return None
    if source in ["zh","en","zt"] :
        #中英
        onnx_bin = os.path.join(base_dir,"sherpa-onnx-models", "sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20")
    elif source in ["zh","zt","ja","jp",'vi','th',"id",'ar',"ru","en"] :
        #中日
        onnx_bin = os.path.join(base_dir,"sherpa-onnx-models", "sherpa-onnx-streaming-zipformer-ar_en_id_ja_ru_th_vi_zh-2025-02-10")
    else:return None
    # 新增路径检查
    if not os.path.exists(onnx_bin):
        logger.put({"text": f"模型路径不存在：{onnx_bin},\n开始自动下载模型", "level": "error"})
        from ..core.update import module_download
        if not module_download('https://cloudflarestorage.boyqiu001.top/VRCLS本地识别模型包.7z',Path(base_dir), logger):
            logger.put({"text": f"模型自动下载失败,可以尝试重启程序再次安装，\n也可以去qq群1011986554或github文档页面下载并手动安装VRCLS本地识别模型包", "level": "error"})
            return None
    # Please replace the model files if needed.
    # See https://k2-fsa.github.io/sherpa/onnx/pretrained_models/index.html
    # for download links.
    recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens=os.path.join(onnx_bin,"tokens.txt"),
        encoder=os.path.join(onnx_bin,"encoder.onnx"),
        decoder=os.path.join(onnx_bin,"decoder.onnx"),
        joiner=os.path.join(onnx_bin,"joiner.onnx"),
        num_threads=1,
        sample_rate=16000,
        feature_dim=80,
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=300,  # it essentially disables this rule
        decoding_method="greedy_search",
        provider="cpu",
        hotwords_file="",
        hotwords_score=1.5,
        blank_penalty=0.0,
    )
    return recognizer
def sherpa_onnx_run_local(sendClient,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji,outputList,ttsVoice):
    import pyaudiowpatch
    import numpy as np
    from multiprocessing import Process,Queue
    import time
    import pyttsx3

    from pythonosc import udp_client
    if params["config"].get("gameMicName")== "" or params["config"].get("gameMicName") is None or params["config"].get("gameMicName")== "default":
        logger.put({"text":"使用系统默认桌面音频","level":"info"})
        micIndex=None
    else:
        device_index=False
        for i in micList:
            if params["config"].get("gameMicName")==i.get("name"):
                device_index=True
                micIndex=i.get('index')
                logger.put({"text":f"当前桌面音频：{params['config'].get('gameMicName')}","level":"info"})
                break
        
        
        if not device_index:
            logger.put({"text":"无法找到指定桌面音频，使用系统默认桌面音频","level":"info"})
            micIndex=None
    params["gameVoiceKeyRun"]=True 
    voiceMode=params["config"].get("gameVoiceMode")
    voiceHotKey=params["config"].get("gameVoiceHotKey_new")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        from pynput import keyboard
        from functools import partial
        params["gameVoiceKeyRun"]=False 
        keyThread=keyboard.GlobalHotKeys({voiceHotKey:partial(change_run_local,params,logger,"cap")})
        keyThread.start()
        logger.put({"text":f"当前桌面音频捕获状态状态：{'打开' if params['gameVoiceKeyRun'] else '关闭'}","level":"info"})
    elif voiceMode == 2 and voiceHotKey is not None:#按住说话
        from ..core.keypress import VKeyHandler
        params["gameVoiceKeyRun"]=False 
        keyThread = VKeyHandler(params,"gameVoiceKeyRun")
        keyThread.start()
        logger.put({"text":f"按住说话已开启，请按住v键说话","level":"info"})


    
    pa = pyaudiowpatch.PyAudio()
    # 获取输入设备信息  
    device_info = pa.get_default_wasapi_loopback() if micIndex is None else pa.get_device_info_by_index(micIndex)
   

    recognizer = create_recognizer(logger,params["config"].get("targetTranslationLanguage"))
    if recognizer is None:
        logger.put({"text":"本地模型当前只支持，中文、英文、俄文、越南文、日文、泰文、印尼文和阿拉伯文","level":"warning"})
        return
    sample_rate = int(device_info["defaultSampleRate"])
    samples_per_read = int(0.1 * sample_rate)  # 0.1秒 = 4800个样本

    stream = recognizer.create_stream()

    # 创建PyAudio音频流
    audio_stream = pa.open(
        rate=sample_rate,
        channels=1,
        format=pyaudiowpatch.paFloat32,
        input=True,
        input_device_index=device_info["index"],
        frames_per_buffer=samples_per_read,
    )

    last_result = ""
    logger.put({"text":"sound process started complete||本地桌面音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("本地桌面音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    messageQueue=Queue(-1)
    p = Process(target=sherpa_once,daemon=True, args=(messageQueue,sendClient,params,logger,filter,"cap",steamvrQueue,customEmoji,outputList,ttsVoice))
    p.start()
    client=udp_client.SimpleUDPClient(params["config"].get("osc-ip"), int(params["config"].get("osc-port")))
    lastSendTime=time.time()
    try:
        while params["running"]:
            ifcontinue=params["vrcMuteSelf"] if voiceMode == 3 else not params["gameVoiceKeyRun"] or params["gameStopped"]
            if ifcontinue:
                if not audio_stream.is_stopped():audio_stream.stop_stream()
            else:
                if not audio_stream.is_stopped():audio_stream.start_stream()
            # 读取音频数据
            data = audio_stream.read(samples_per_read)
            samples = np.frombuffer(data, dtype=np.float32)
            
            stream.accept_waveform(sample_rate, samples)
            while recognizer.is_ready(stream):
                recognizer.decode_stream(stream)

            is_endpoint = recognizer.is_endpoint(stream)
            result = recognizer.get_result(stream)

            if result and (last_result != result):
                last_result = result
                nowtime=time.time()
                dalaytime=float(params["config"].get("realtimeOutputDelay"))
                if dalaytime>0 and nowtime-lastSendTime>dalaytime:
                    lastSendTime=nowtime
                    client.send_message("/chatbox/input",[ f'{result}', True, False]) 
            
            if is_endpoint:
                if result:
                   messageQueue.put(result)
                recognizer.reset(stream)
                
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        pa.close()
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||本地桌面音频进程退出完毕","level":"info"})
        params["gameStopped"] = True
def sherpa_onnx_run(sendClient,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji,outputList,ttsVoice):
    import pyaudiowpatch
    import numpy as np
    from multiprocessing import Process,Queue
    import time
    import pyttsx3
    from pynput import keyboard
    from functools import partial
    from pythonosc import udp_client
    if params["config"].get("micName")== "" or params["config"].get("micName") is None or params["config"].get("micName")== "default":
        logger.put({"text":"使用系统默认麦克风","level":"info"})
        micIndex=defautMicIndex
    else:
        try:
            micIndex=micList.index(params["config"].get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定游戏麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前游戏麦克风：{micList[micIndex]}","level":"info"})
    params["voiceKeyRun"]=True 
    voiceMode=params["config"].get("voiceMode")
    voiceHotKey=params["config"].get("voiceHotKey_new")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["voiceKeyRun"]=False 
        keyThread=keyboard.GlobalHotKeys({voiceHotKey:partial(change_run_local,params,logger,"mic")})
        keyThread.start()
        logger.put({"text":f"当前麦克风状态：{'打开' if params['voiceKeyRun'] else '关闭'}","level":"info"})
    elif voiceMode == 2 and voiceHotKey is not None:#按住说话
        from ..core.keypress import VKeyHandler
        params["voiceKeyRun"]=False 
        keyThread = VKeyHandler(params,"voiceKeyRun")
        keyThread.start()
        logger.put({"text":f"按住说话已开启，请按住v键说话","level":"info"})
    
    pa = pyaudiowpatch.PyAudio()
    
    # 获取输入设备信息
    input_device = pa.get_device_info_by_index(micIndex)
    

    recognizer = create_recognizer(logger,params["config"].get("sourceLanguage"))
    if recognizer is None:
        logger.put({"text":"本地模型当前只支持，中文、英文、俄文、越南文、日文、泰文、印尼文和阿拉伯文","level":"warning"})
        return

    sample_rate = int(input_device["defaultSampleRate"])
    samples_per_read = int(0.1 * sample_rate)  # 0.1秒 = 4800个样本

    stream = recognizer.create_stream()

    # 创建PyAudio音频流
    audio_stream = pa.open(
        rate=sample_rate,
        channels=1,
        format=pyaudiowpatch.paFloat32,
        input=True,
        input_device_index=micIndex,
        frames_per_buffer=samples_per_read,
    )
    logger.put({"text":"sound process started complete||本地音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("本地音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    last_result = ""
    messageQueue=Queue(-1)
    p = Process(target=sherpa_once,daemon=True, args=(messageQueue,sendClient,params,logger,filter,"mic",steamvrQueue,customEmoji,outputList,ttsVoice))
    p.start()
    client=udp_client.SimpleUDPClient(params["config"].get("osc-ip"), int(params["config"].get("osc-port")))
    lastSendTime=time.time()


    
    try:
        while params["running"]:
            ifcontinue=params["vrcMuteSelf"] if voiceMode == 3 else not params["voiceKeyRun"] or params["micStopped"]
            if ifcontinue:
                if not audio_stream.is_stopped():audio_stream.stop_stream()
                continue
            else:
                if audio_stream.is_stopped():audio_stream.start_stream()
            # 读取音频数据
            data = audio_stream.read(samples_per_read)
            samples = np.frombuffer(data, dtype=np.float32)
            
            stream.accept_waveform(sample_rate, samples)
            while recognizer.is_ready(stream):
                recognizer.decode_stream(stream)
            is_endpoint=recognizer.is_endpoint(stream)
            result = recognizer.get_result(stream)
            
            if result and (last_result != result):
                last_result = result
                nowtime=time.time()
                dalaytime=float(params["config"].get("realtimeOutputDelay"))
                if dalaytime>0 and nowtime-lastSendTime>dalaytime:
                    lastSendTime=nowtime
                    client.send_message("/chatbox/input",[ f'{result}', True, False]) 

            if is_endpoint:
                if result:
                    messageQueue.put(result)
                recognizer.reset(stream)

                
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||麦克风音频进程退出完毕","level":"info"})
        params["micStopped"]=True
        
def sherpa_onnx_run_mic(sendClient,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji,outputList,ttsVoice):
    import pyaudiowpatch
    import numpy as np
    from multiprocessing import Process,Queue
    import time
    import pyttsx3
    from pynput import keyboard
    from functools import partial
    from pythonosc import udp_client
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
    params["gameVoiceKeyRun"]=True 
    voiceMode=params["config"].get("gameVoiceMode")
    voiceHotKey=params["config"].get("gameVoiceHotKey_new")
    if voiceMode == 0 :#常开模式
        pass
    elif voiceMode == 1 and voiceHotKey is not None:#按键切换模式
        params["gameVoiceKeyRun"]=False 
        keyThread=keyboard.GlobalHotKeys({voiceHotKey:partial(change_run_local,params,logger,"cap")})
        keyThread.start()
        logger.put({"text":f"当前桌面音频捕获状态状态：{'打开' if params['gameVoiceKeyRun'] else '关闭'}","level":"info"})
    elif voiceMode == 2 and voiceHotKey is not None:#按住说话
        from ..core.keypress import VKeyHandler
        params["gameVoiceKeyRun"]=False 
        keyThread = VKeyHandler(params,"gameVoiceKeyRun")
        keyThread.start()
        logger.put({"text":f"按住说话已开启，请按住v键说话","level":"info"})

    pa = pyaudiowpatch.PyAudio()
    
    # 获取输入设备信息
    input_device = pa.get_device_info_by_index(micIndex)
    

    recognizer = create_recognizer(logger,params["config"].get("targetTranslationLanguage"))
    if recognizer is None:
        logger.put({"text":"本地模型当前只支持，中文、英文、俄文、越南文、日文、泰文、印尼文和阿拉伯文","level":"warning"})
        return

    sample_rate = int(input_device["defaultSampleRate"])
    samples_per_read = int(0.1 * sample_rate)  # 0.1秒 = 4800个样本

    stream = recognizer.create_stream()

    # 创建PyAudio音频流
    audio_stream = pa.open(
        rate=sample_rate,
        channels=1,
        format=pyaudiowpatch.paFloat32,
        input=True,
        input_device_index=micIndex,
        frames_per_buffer=samples_per_read,
    )
    logger.put({"text":"sound process started complete||本地桌面音频进程启动完毕","level":"info"})
    try:pyttsx3.speak("本地桌面音频进程启动完毕")
    except:logger.put({"text":"请去系统设置-时间和语言中的语音栏目安装中文语音包","level":"warning"})
    last_result = ""
    messageQueue=Queue(-1)
    p = Process(target=sherpa_once,daemon=True, args=(messageQueue,sendClient,params,logger,filter,"cap",steamvrQueue,customEmoji,outputList,ttsVoice))
    p.start()
    client=udp_client.SimpleUDPClient(params["config"].get("osc-ip"), int(params["config"].get("osc-port")))
    lastSendTime=time.time()
    try:
        while params["running"]:
            ifcontinue=params["vrcMuteSelf"] if voiceMode == 3 else not params["gameVoiceKeyRun"] or params["gameStopped"]
            if ifcontinue:continue
            # 读取音频数据
            data = audio_stream.read(samples_per_read)
            samples = np.frombuffer(data, dtype=np.float32)
            
            stream.accept_waveform(sample_rate, samples)
            while recognizer.is_ready(stream):
                recognizer.decode_stream(stream)

            is_endpoint = recognizer.is_endpoint(stream)
            result = recognizer.get_result(stream)

            if result and (last_result != result):
                last_result = result
                nowtime=time.time()
                dalaytime=float(params["config"].get("realtimeOutputDelay"))
                if dalaytime>0 and nowtime-lastSendTime>dalaytime:
                    lastSendTime=nowtime
                    client.send_message("/chatbox/input",[ f'{result}', True, False]) 

            if is_endpoint:
                if result:
                    messageQueue.put(result)
                recognizer.reset(stream)

                
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||游戏音频进程退出完毕","level":"info"})
        params["gameStopped"] = True
def sherpa_once(result,sendClient,params,logger,filter,mode,steamvrQueue,customEmoji:dict,outputList,ttsVoice):
    import translators
    import time
    import html
    import traceback
    
    from ..handler.DefaultCommand import DefaultCommand
    from ..handler.ChatBox import ChatboxHandler
    from ..handler.Avatar import AvatarHandler
    from ..handler.VRCBitmapLedHandler import VRCBitmapLedHandler
    from ..handler.SelfRead import SelfReadHandler
    from ..handler.tts import TTSHandler
    from hanziconv import HanziConv
    import requests
    from ..module.translate import developer_trasnlator,other_trasnlator
    

    avatar=AvatarHandler(logger=logger,osc_client=sendClient,params=params)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,params=params)
    chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,params=params)
    bitMapLed=VRCBitmapLedHandler(logger=logger,osc_client=sendClient,params=params)
    selfRead=SelfReadHandler(logger=logger,osc_client=sendClient,steamvrQueue=steamvrQueue,params=params)
    if params["config"].get("TTSToggle")!=0:tts=TTSHandler(logger=logger,params=params,mode=mode,header=params['headers'],outputList=outputList,ttsVoice=ttsVoice)
    
    baseurl=params["config"].get('baseurl')
    while params["running"]:
        try:
            tragetTranslateLanguage2=params["config"].get("targetTranslationLanguage2")
            tragetTranslateLanguage3=params["config"].get("targetTranslationLanguage3")
            tragetTranslateLanguage=params["tragetTranslateLanguage"]
            sourceLanguage=params["sourceLanguage"]
            translator=params["config"].get('translateService') if mode=="mic" else params["config"].get('translateServicecap')
            res={}
            res['text']=result.get()
            st=time.time()
            et0=time.time()
            if params["runmode"] == "translation":
                if mode =="cap":
                    tmp=sourceLanguage
                    sourceLanguage=tragetTranslateLanguage
                    tragetTranslateLanguage=tmp
                if params["config"].get("translateService")!="developer":
                    res['translatedText2']=''
                    res['translatedText3']=''
                    try:
                        if translator == "openai":
                            from src.module.translate import openai_translator
                            res['translatedText'] = openai_translator(logger, sourceLanguage, tragetTranslateLanguage, res, params)
                        else:
                            res['translatedText']=html.unescape(translators.translate_text(res["text"],translator=translator,from_language="zh" if sourceLanguage=="zt" else  sourceLanguage,to_language=tragetTranslateLanguage))
                    except Exception as e:
                        if all(i in str(e) for i in["from_language[","] and to_language[","] should not be same"]):
                            logger.put({"text":f"翻译语言检测同语言：{e}","level":"debug"})
                            res['translatedText']=res["text"]
                        else:
                            logger.put({"text":f"翻译异常,请尝试更换翻译引擎：{str(e)}","level":"error"})
                            logger.put({"text":f"翻译异常：{traceback.format_exc()}","level":"debug"})
                            res['translatedText']=''
                else:
                    url=baseurl+'/func/webtranslate'
                    data = {"text":res['text'],
                            "targetLanguage": tragetTranslateLanguage,
                            'targetLanguage2': tragetTranslateLanguage2,
                            'targetLanguage3': tragetTranslateLanguage3,
                            "sourceLanguage": "zh" if sourceLanguage=="zt" else  sourceLanguage}
                    logger.put({"text":f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}","level":"debug"})
                    response=requests.post(url, json=data, headers=params['headers'])
                    
                                # 检查响应状态码
                    if response.status_code != 200:
                        if response.status_code == 430:
                            res=response.json()
                            logger.put({"text":f"{'桌面音频'if mode=='cap'else'麦克风'}请求过于频繁,可以尝试更换其他翻译引擎,触发规则{res.get('limit')}","level":"warning"})
                        else:    
                            logger.put({"text":f"本地识别服务器翻译数据接收异常:{response.text}","level":"warning"})
                        continue
                    # 解析JSON响应
                    res = response.json()
                    logger.put({"text":f"服务器翻译成功：","level":"debug"})

            if  params["runmode"] == "translation" and  mode=='mic' and params["config"].get("translateService")!="developer":        
                # 第二语言
                if  tragetTranslateLanguage2!="none":
                        if translator == "openai":
                            from src.module.translate import openai_translator
                            res['translatedText2'] = openai_translator(logger, sourceLanguage, tragetTranslateLanguage2, res, params)
                        else:
                            res['translatedText2']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage2,res)
                # 第三语言
                if  tragetTranslateLanguage3!="none":
                        if translator == "openai":
                            from src.module.translate import openai_translator
                            res['translatedText3'] = openai_translator(logger, sourceLanguage, tragetTranslateLanguage3, res, params)
                        else:
                            res['translatedText3']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage3,res)
                        
                
            if sourceLanguage== "zh":res["text"]=HanziConv.toSimplified(res["text"])
            elif sourceLanguage=="zt":res["text"]=HanziConv.toTraditional(res["text"])
            et=time.time()
            logger.put({"text":f"本地桌面音频识别结果: " + res["text"],"level":"debug"})
            logger.put({"text":f"识别用时：{round(et0-st,2)}s，翻译用时：{round(et-et0,2)}s 识别结果: " + res["text"],"level":"info"})
            
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
                        tts.tts_audio(res['translatedText'],language=tragetTranslateLanguage if mode=="mic" else sourceLanguage)
                    if params["config"].get("TTSToggle")==1 and mode == 'mic' and params["runmode"] == "translation" :
                        tts.tts_audio(res['translatedText'],language=tragetTranslateLanguage)
                    if params["config"].get("TTSToggle")==2 and mode == 'mic'and params["runmode"] == "text" :
                        tts.tts_audio(res['text'],language=sourceLanguage)
                    
                if params["runmode"] == "control":avatar.handle(res)
                if params["runmode"] == "bitMapLed":bitMapLed.handle(res,params=params)
            et=time.time()
            logger.put({"text":f"总用时：{round(et-st,2)}s","level":"debug"})
        except Exception as e:
            import traceback
            logger.put({"text":"sherpa_once未知异常"+traceback.format_exc(),"level":"error"})
            continue
whisper_to_baidu = {
    'af': 'afr',       # 阿非利堪斯语
    'am': 'amh',       # 阿姆哈拉语
    'ar': 'ara',       # 阿拉伯语
    'as': 'asm',       # 阿萨姆语
    'az': 'aze',       # 阿塞拜疆语
    'ba': 'bak',       # 巴什基尔语
    'be': 'bel',       # 白俄罗斯语
    'bg': 'bul',       # 保加利亚语
    'bn': 'ben',       # 孟加拉语
    'bo': None,       # 藏语（百度 API 中没有对应的代码）
    'br': 'bre',       # 布列塔尼语
    'bs': 'bos',       # 波斯尼亚语
    'ca': 'cat',       # 加泰罗尼亚语
    'cs': 'cs',        # 捷克语
    'cy': 'gle',       # 威尔士语
    'da': 'dan',       # 丹麦语
    'de': 'de',        # 德语
    'el': 'el',        # 希腊语
    'en': 'en',        # 英语
    'es': 'spa',       # 西班牙语
    'et': 'est',       # 爱沙尼亚语
    'eu': 'baq',       # 巴斯克语
    'fa': 'per',       # 波斯语
    'fi': 'fin',       # 芬兰语
    'fo': 'fao',       # 法罗语
    'fr': 'fra',       # 法语
    'gl': 'glg',       # 加利西亚语
    'gu': 'guj',       # 古吉拉特语
    'ha': 'hau',       # 豪萨语
    'haw': 'haw',      # 夏威夷语
    'he': 'heb',       # 希伯来语
    'hi': 'hi',        # 印地语
    'hr': 'hrv',       # 克罗地亚语
    'ht': 'hat',       # 海地克里奥尔语
    'hu': 'hu',        # 匈牙利语
    'hy': 'arm',       # 亚美尼亚语
    'id': 'id',        # 印尼语
    'is': 'ice',       # 冰岛语
    'it': 'it',        # 意大利语
    'ja': 'jp',        # 日语
    'jw': 'jav',       # 爪哇语
    'ka': 'geo',       # 格鲁吉亚语
    'kk': None,       # 哈萨克语（百度 API 中没有对应的代码）
    'km': 'hkm',       # 高棉语
    'kn': 'kan',       # 卡纳达语
    'ko': 'kor',       # 韩语
    'la': 'lat',       # 拉丁语
    'lb': 'ltz',       # 卢森堡语
    'ln': 'lin',       # 林加拉语
    'lo': 'lao',       # 老挝语
    'lt': 'lit',       # 立陶宛语
    'lv': 'lav',       # 拉脱维亚语
    'mg': 'mg',        # 马达加斯加语
    'mi': None,       # 毛利语（百度 API 中没有对应的代码）
    'mk': 'mac',       # 马其顿语
    'ml': 'mal',       # 马拉雅拉姆语
    'mn': None,       # 蒙古语（百度 API 中没有对应的代码）
    'mr': 'mar',       # 马拉地语
    'ms': 'may',       # 马来语
    'mt': 'mlt',       # 马耳他语
    'my': 'bur',       # 缅甸语
    'ne': 'nep',       # 尼泊尔语
    'nl': 'nl',        # 荷兰语
    'nn': 'nno',       # 新挪威语
    'no': 'nor',       # 挪威语
    'oc': 'oci',       # 奥克语
    'pa': 'pan',       # 旁遮普语
    'pl': 'pl',        # 波兰语
    'ps': 'pus',       # 普什图语
    'pt': 'pt',        # 葡萄牙语
    'ro': 'rom',       # 罗马尼亚语
    'ru': 'ru',        # 俄语
    'sa': 'san',       # 梵语
    'sd': 'snd',       # 信德语
    'si': 'sin',       # 僧伽罗语
    'sk': 'sk',        # 斯洛伐克语
    'sl': 'slo',       # 斯洛文尼亚语
    'sn': 'sna',       # 修纳语
    'so': 'som',       # 索马里语
    'sq': 'alb',       # 阿尔巴尼亚语
    'sr': 'srp',       # 塞尔维亚语
    'su': 'sun',       # 巽他语
    'sv': 'swe',       # 瑞典语
    'sw': 'swa',       # 斯瓦希里语
    'ta': 'tam',       # 泰米尔语
    'te': 'tel',       # 泰卢固语
    'tg': 'tgk',       # 塔吉克语
    'th': 'th',        # 泰语
    'tk': 'tuk',       # 土库曼语
    'tl': 'tgl',       # 他加禄语
    'tr': 'tr',        # 土耳其语
    'tt': 'tat',       # 鞑靼语
    'uk': 'ukr',       # 乌克兰语
    'ur': 'urd',       # 乌尔都语
    'uz': None,       # 乌兹别克语（百度 API 中没有对应的代码）
    'vi': 'vie',       # 越南语
    'yi': 'yid',       # 意第绪语
    'yo': 'yor',       # 约鲁巴语
    'yue': 'yue',     # 粤语
    'zh': 'zh',        # 简体中文
    'zt': 'cht'        # 繁体中文
}
libretranslate_to_baidu = {
    'ar': 'ara',       # 阿拉伯语
    'az': 'aze',       # 阿塞拜疆语
    'bg': 'bul',       # 保加利亚语
    'bn': 'ben',       # 孟加拉语
    'ca': 'cat',       # 加泰罗尼亚语
    'cs': 'cs',        # 捷克语
    'da': 'dan',       # 丹麦语
    'de': 'de',        # 德语
    'el': 'el',        # 希腊语
    'en': 'en',        # 英语
    'eo': None,       # 世界语（百度 API 中没有对应的代码）
    'es': 'spa',       # 西班牙语
    'et': 'est',       # 爱沙尼亚语
    'eu': 'baq',       # 巴斯克语
    'fa': 'per',       # 波斯语
    'fi': 'fin',       # 芬兰语
    'fr': 'fra',       # 法语
    'ga': 'gle',       # 爱尔兰语
    'gl': 'glg',       # 加利西亚语
    'he': 'heb',       # 希伯来语
    'hi': 'hi',        # 印地语
    'hu': 'hu',        # 匈牙利语
    'id': 'id',        # 印尼语
    'it': 'it',        # 意大利语
    'ja': 'jp',        # 日语
    'ko': 'kor',       # 韩语
    'lt': 'lit',       # 立陶宛语
    'lv': 'lav',       # 拉脱维亚语
    'ms': 'may',       # 马来语
    'nb': 'nob',       # 挪威语（书面挪威语）
    'nl': 'nl',        # 荷兰语
    'pl': 'pl',        # 波兰语
    'pt': 'pt',        # 葡萄牙语
    'ro': 'rom',       # 罗马尼亚语
    'ru': 'ru',        # 俄语
    'sk': 'sk',        # 斯洛伐克语
    'sl': 'slo',       # 斯洛文尼亚语
    'sq': 'alb',       # 阿尔巴尼亚语
    'sr': 'srp',       # 塞尔维亚语
    'sv': 'swe',       # 瑞典语
    'th': 'th',        # 泰语
    'tl': 'tgl',       # 塔加洛语
    'tr': 'tr',        # 土耳其语
    'uk': 'ukr',       # 乌克兰语
    'ur': 'urd',       # 乌尔都语
    'vi': 'vie',       # 越南语
    'zh': 'zh',        # 中文
    'zt': 'cht'        # 繁体中文
}
if __name__ == "__main__":
    sherpa_onnx_run()
