from flask import Flask, request, render_template, url_for,jsonify,send_from_directory
import waitress
from src.core.startup import StartUp
from src.core.avatar import avatar
from multiprocessing import Process,Manager,freeze_support,Queue
from src.core.process import logger_process,selfMic_listen,gameMic_listen_capture,gameMic_listen_VoiceMeeter

import time
import json,os
import webbrowser

queue=Queue(-1)
processList=[]
app = Flask(__name__,static_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key' 

def rebootJob():
    global queue,params,listener_thread,listener_thread,startUp,sendClient,baseurl,headers,manager
    queue.put({"text":"/reboot","level":"debug"})
    queue.put({"text":"sound process start to complete wait for 20s|| 程序开始重启 请等待20秒 ","level":"info"})
    params["running"] = False
    time.sleep(20)
    params["VRCBitmapLed_taskList"]=manager.list()
    startUp.getMics()
    listener_thread = Process(target=selfMic_listen,args=(baseurl,sendClient,startUp.config,headers,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter))
    listener_thread.start()
    if startUp.config.get("Separate_Self_Game_Mic")==1:
        listener_thread1 = Process(target=gameMic_listen_capture,args=(baseurl,sendClient,startUp.config,headers,params,queue,startUp.loopbackIndexList,startUp.defautMicIndex,startUp.filter))
        listener_thread1.start()
    elif startUp.config.get("Separate_Self_Game_Mic")==2:
        listener_thread1 = Process(target=gameMic_listen_VoiceMeeter,args=(baseurl,sendClient,startUp.config,headers,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter))
        listener_thread1.start()
    
    params["running"] = True
    params["tragetTranslateLanguage"]=startUp.config.get("targetTranslationLanguage")
    params["sourceLanguage"]=startUp.config.get("sourceLanguage")
    queue.put({"text":"sound process restart complete|| 程序完成重启","level":"info"})
@app.route('/api/saveConfig', methods=['post'])
def saveConfig():
    global queue,params,listener_thread,startUp,sendClient,baseurl,headers
    data=request.get_json()
    queue.put({"text":"/saveandreboot","level":"debug"})
    try:
        with open('client.json', 'r',encoding='utf8') as file, open('client-back.json', 'w', encoding="utf8") as f:
            f.write(file.read())
        startUp.config=data["config"]
        with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(startUp.config,ensure_ascii=False, indent=4))
    except Exception as e:
        queue.put({"text":f"config saved 配置保存异常:{e}","level":"warning"})
        return jsonify({"text":f"config saved 配置保存异常:{e}","level":"warning"}),401
    queue.put({"text":"config saved 配置保存完毕","level":"info"})
    return startUp.config

@app.route('/')
def ui():
    return render_template("index.html")

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)
# 处理表单提交
@app.route('/api/getConfig', methods=['get'])
def getConfig():
    global startUp,queue
    queue.put({"text":"/getConfig","level":"debug"})
    return jsonify(startUp.config),200


@app.route('/api/reboot', methods=['get'])
def reboot():
    rebootJob()
    return jsonify({'message':'sound process restart complete|| 程序完成重启'}),200
 

# 处理表单提交
@app.route('/api/saveandreboot', methods=['post'])
def update_config():
    data=request.get_json(silent=True)
    if data is None: return jsonify({'text':'no data'}),400
    config=saveConfig()
    rebootJob() 
    return jsonify(config),200
@app.route('/api/getAvatarParameters', methods=['get'])
def getAvatarParameters():
    try:
        avatarInfo=avatar()
    except Exception as e:
        queue.put({"text":"未成功检测到vrchat",'level':'warning'})
    avatarID=avatarInfo.getAvatarID()
    avatar_json_path,userID=find_avatar_json(avatarID)
    with open(avatar_json_path,'rb') as file:
        content = file.read()
        # 检查并去除 BOM（如果存在）
        # UTF-8 BOM 是 b'\xef\xbb\xbf'
        if content.startswith(b'\xef\xbb\xbf'):content = content[3:]  # 去除 BOM
        json_str = content.decode('utf-8')
        data = json.loads(json_str)
        
    res=[]
    for item in data['parameters']:
        if item.get("input"):

            res.append({
                'name':item["name"],
                "path":item["input"]["address"],
                'type':item["input"]["type"]
            })
    return jsonify({"avatarInfo":{'avatarID':data["id"],'avatarName':data["name"],"filePath":avatar_json_path},'dataTable':res}),200

@app.route('/api/getMics', methods=['get'])
def getMics():
    global queue,startUp
    queue.put({"text":"/getMics","level":"debug"})
    return jsonify(startUp.micList),200
@app.route('/api/getcapture', methods=['get'])
def getCapture():
    global queue,startUp
    queue.put({"text":"/getcapture","level":"debug"})

    Separate_Self_Game_Mic = int(request.args.get('Separate_Self_Game_Mic', 0))

    if Separate_Self_Game_Mic==2:return jsonify(startUp.micList),200
    elif Separate_Self_Game_Mic==1:return jsonify(startUp.loopbackList),200
    else :return jsonify([]),200


# 示例用法
# if __name__ == "__main__":
#     devices = list_loopback_devices()
#     print("可用环路设备列表：")
#     for d in devices:
#         print(f'索引 {d["index"]}: {d["name"]} (采样率 {d["defaultSampleRate"]}Hz)')
# def get_wasapi_device_index():

#     import pyaudiowpatch
#     p = pyaudiowpatch.PyAudio()
#     try:
#         wasapi_info = p.get_host_api_info_by_type(pyaudiowpatch.paWASAPI)
#         deviceList=[]
#         # 列出所有WASAPI设备
#         for i in range(p.get_device_count()):
#             dev = p.get_device_info_by_index(i)
#             if dev["hostApi"] == wasapi_info["index"] and dev["maxInputChannels"] > 0:
#                 deviceList.append(dev['name'])
#         return jsonify(deviceList),200
#     finally:
#         p.terminate()
    
def find_avatar_json( avatar_id):
    base_path=r'~\AppData\LocalLow\VRChat\VRChat\OSC'
    # 拼接基础路径
    root_path = os.path.expanduser(base_path)
    
    # 遍历所有 userId 目录
    for user_id in os.listdir(root_path):
        avatar_path = os.path.join(root_path, user_id, 'Avatars', f'{avatar_id}.json')
        
        # 检查文件是否存在
        if os.path.isfile(avatar_path):
            return avatar_path, user_id
    
    return None, None
 
# 示例函数
def open_web(host,port):
    global startUp,queue

    # 定义要打开的URL
    url = f"http://{host}:{port}"
    
    # 获取Edge浏览器的可执行文件路径
    # 不同的操作系统有不同的路径
    edge_path = None
    if os.name == 'nt':  # Windows系统
        edge_path = os.path.join(os.environ.get('ProgramFiles(x86)'), 'Microsoft', 'Edge', 'Application', 'msedge.exe')
    elif os.uname().sysname == 'Darwin':  # macOS系统（注意：macOS上默认可能没有安装Edge）
        # 通常需要用户手动指定Edge的路径，或者通过其他方式获取
        # 例如：edge_path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
        pass  # 这里不做处理，因为路径需要用户指定
    elif os.uname().sysname == 'Linux':  # Linux系统
        # Linux上Edge的路径也可能需要用户手动指定
        # 例如：edge_path = '/opt/microsoft/edge/microsoft-edge'
        pass  # 这里不做处理，因为路径需要用户指定

    # 如果找到了Edge的路径，则使用它打开网页
    try:
        if startUp.config.get("webBrowserPath") is not None and startUp.config.get("webBrowserPath") != "":
            webbrowser.get(using=startUp.config.get("webBrowserPath")).open(url)
        elif edge_path:
            # 创建一个新的Edge控制器
            edge = webbrowser.get(using=edge_path)
            # 使用Edge控制器打开网页
            edge.open(url)
        else:
            # 如果没有找到Edge的路径，则使用默认浏览器打开网页
            
            webbrowser.open(url)
    except Exception:
        queue.put({"text":"没有找到指定的路径,使用默认浏览器打开网页","level":"debug"})
        webbrowser.open(url)
 
# TODO steamvr显示界面
# TODO 修正各个模式下两个播放线程的行为
if __name__ == '__main__':
    freeze_support()
    try:

        logger_thread = Process(target=logger_process,daemon=True,args=(queue,))
        logger_thread.start()
        manager = Manager()
        params=manager.dict()

        params["running"] = True
        startUp=StartUp(queue)
        queue.put({'text':r'''
------------------------------------------------------------------------
     __     __  _______    ______   __         ______  
    /  |   /  |/       \  /      \ /  |       /      \ 
    $$ |   $$ |$$$$$$$  |/$$$$$$  |$$ |      /$$$$$$  |
    $$ |   $$ |$$ |__$$ |$$ |  $$/ $$ |      $$ \__$$/ 
    $$  \ /$$/ $$    $$< $$ |      $$ |      $$      \ 
     $$  /$$/  $$$$$$$  |$$ |   __ $$ |       $$$$$$  |
      $$ $$/   $$ |  $$ |$$ \__/  |$$ |_____ /  \__$$ |
       $$$/    $$ |  $$ |$$    $$/ $$       |$$    $$/ 
        $/     $$/   $$/  $$$$$$/  $$$$$$$$/  $$$$$$/  
                                                   

                   
        '''+f'webUI: http://{startUp.config['api-ip']}:{startUp.config['api-port']}'+r''' 
                                                
        》》》》                  《《《《            
        》》》》请保持本窗口持续开启《《《《          
        》》》》                  《《《《                                 
    
        欢迎使用由VoiceLinkVR开发的VRCLS 
        本程序的开发这为boyqiu-001(boyqiu玻璃球)
        欢迎大家加入qq群1011986554获取最新资讯
        目前您使用的时公测账户,限制每日2000次请求
        如需获取更多资源请加群
------------------------------------------------------------------------
                    ''','level':'info'}
                    )
        headers=startUp.run()
        sendClient= startUp.setOSCClient(queue)
        baseurl=startUp.config.get("baseurl")
        params["VRCBitmapLed_taskList"]= manager.list()
        tmp=" "*(8 if startUp.config.get("VRCBitmapLed_row") is None else startUp.config.get("VRCBitmapLed_row") )*(16 if startUp.config.get("VRCBitmapLed_col") is None else startUp.config.get("VRCBitmapLed_col"))
        params["VRCBitmapLed_Line_old"]= tmp
        params["tragetTranslateLanguage"]=startUp.tragetTranslateLanguage
        params["sourceLanguage"]=startUp.sourceLanguage

        queue.put({'text':"vrc udpClient ok||发送准备就绪",'level':'info'})
        params["runmode"]= startUp.config["defaultMode"]
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        # this is called from the background thread

        listener_thread = Process(target=selfMic_listen,args=(baseurl,sendClient,startUp.config,headers,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter))
        listener_thread.start()
        if startUp.config.get("Separate_Self_Game_Mic")==1:
            listener_thread1 = Process(target=gameMic_listen_capture,args=(baseurl,sendClient,startUp.config,headers,params,queue,startUp.loopbackIndexList,startUp.defautMicIndex,startUp.filter))
            listener_thread1.start()
        elif startUp.config.get("Separate_Self_Game_Mic")==2:
            listener_thread1 = Process(target=gameMic_listen_VoiceMeeter,args=(baseurl,sendClient,startUp.config,headers,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter))
            listener_thread1.start()
            
        
        queue.put({'text':"api ok||api就绪",'level':'info'})
        open_web(startUp.config['api-ip'],startUp.config['api-port'])
        waitress.serve(app=app, host=startUp.config['api-ip'], port=startUp.config['api-port'])
    except Exception as e:
        print(f"Main thread encountered an error: {e}")
    finally:
        # 设置退出事件来通知所有子线程
        listener_thread.kill()
        if startUp.config.get("Separate_Self_Game_Mic")!=0: listener_thread1.kill()
    