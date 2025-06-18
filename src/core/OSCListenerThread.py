def micStatusListenerThread(logger,params):
    import pythoncom
    import win32com
    import time
    from .OSCListener import OSCListener
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    wmi=win32com.client.GetObject('winmgmts:')
    record=False
    while params["running"]:
        query = "SELECT * FROM Win32_Process WHERE Name = 'VRChat.exe'"
        processes = wmi.ExecQuery(query)
        if not processes or len(processes)==0 :
            time.sleep(1)
            continue
        else:
            break
    try:
        oscListener=OSCListener()
    except Exception as e:
        logger.put({"text":"未成功检测到vrchat",'level':'warning'})
    while params["running"]:
        mute=oscListener.getMuteSelf()
        if mute != record and mute in [True,False]:
            if mute:time.sleep(1.5)
            mute=oscListener.getMuteSelf()
            params["vrcMuteSelf"]=mute
            record=mute
            logger.put({"text":f"VRC麦克风状态:{'关闭'if mute else'打开'}",'level':'info'})
        time.sleep(0.1) 
          
