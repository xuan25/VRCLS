from .serverActionProcess import once
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
        from .keypress import VKeyHandler
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
                ifcontinue=params["vrcMuteSelf"] if voiceMode == 3 else not params["voiceKeyRun"]
                if ifcontinue:continue
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
                        
                    if params["running"] and  (not ifcontinue or voiceMode==2 ) and not (voiceMode==3 and params["vrcMuteSelf"]):audioQueue.put(audio)
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
                ifcontinue=params["vrcMuteSelf"] if voiceMode == 3 else not params["gameVoiceKeyRun"]
                if ifcontinue:continue
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
                    if params["running"] and  (not ifcontinue or voiceMode==2 ) and not (voiceMode==3 and params["vrcMuteSelf"]):audioQueue.put(audio)
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
            ifcontinue=params["vrcMuteSelf"] if voiceMode == 3 else not params["gameVoiceKeyRun"]
            if ifcontinue:continue
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
                    if params["running"] and (params["gameVoiceKeyRun"] or voiceMode==2 ) and not (voiceMode==3 and params["vrcMuteSelf"]):audioQueue.put(audio)
    finally:
        p.terminate()
        while p.is_alive():time.sleep(0.5)
        else: p.close()
        if voiceMode!=0:
            try:keyThread.stop()
            except:pass
        logger.put({"text":"sound process exited complete||桌面音频进程退出完毕","level":"info"})
        params["gameStopped"] = True


# 弃用
# def copyBox_process(queue):
#     import tkinter as tk
#     from ..module.copybox import ScrollableListApp
#     # 启动GUI
#     root = tk.Tk()
#     app = ScrollableListApp(root, queue)
#     root.geometry("500x400")
    
#     # 绑定关闭事件
#     root.protocol("WM_DELETE_WINDOW", app.on_close)
#     root.mainloop()

