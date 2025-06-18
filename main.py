from flask import Flask, request, render_template, url_for,jsonify,send_from_directory
from src.core.startup import StartUp
from src.core.update import main_update
from src.core.OSCListener import OSCListener
from src.core.OSCListenerThread import micStatusListenerThread
from multiprocessing import Process,Manager,freeze_support,Queue
from src.core.serverListener import selfMic_listen,gameMic_listen_capture,gameMic_listen_VoiceMeeter
from src.core.logger import logger_process
from src.core.steamvrProcess import steamvr_process
from src.module.sherpaOnnx import sherpa_onnx_run,sherpa_onnx_run_local,sherpa_onnx_run_mic
from src.module.oscserver import startServer
import time
import json,os,traceback,sys
import webbrowser
import ctypes
from ctypes import wintypes
import sqlite3
from datetime import datetime, timedelta
import requests
import threading as td
from engineio.async_drivers import threading
from flask_socketio import SocketIO, emit
import win32api
import win32com.client
import subprocess
import ctypes
import os
def is_admin():
    """检查当前脚本是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    

def kill_other_vrcls():

    current_pid = win32api.GetCurrentProcessId()
    print(f"当前脚本进程 PID: {current_pid}")

    wmi = None
    service = None
    
    try:
        wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        service = wmi.ConnectServer(".", "root\\cimv2")
    except Exception as e:
        print(f"错误：连接 WMI 服务失败: {e}")
        return

    processes_to_check = []
    try:
        # 获取所有vrcls.exe进程信息
        query = f"SELECT ProcessId, Name FROM Win32_Process WHERE Name='VRCLS.exe'"
        found_processes = service.ExecQuery(query)

        if not found_processes: # WMI ExecQuery 返回的是一个集合，可以直接判断
             print("信息：没有找到名为 'VRCLS.exe' 的正在运行的进程。")
             return
        
        for proc_info in found_processes:
            processes_to_check.append(proc_info) # proc_info 是一个 SWbemObject

    except Exception as e:
        print(f"错误：查询 'VRCLS.exe' 进程列表时出错: {str(e)}")
        if wmi: del wmi
        if service: del service
        return

    if not processes_to_check:
        print("信息：没有找到名为 'VRCLS.exe' 的正在运行的进程。")
        if wmi: del wmi
        if service: del service
        return
        
    other_vrcls_pids = []
    is_current_vrcls = False
    for proc_obj in processes_to_check:
        if proc_obj.ProcessId == current_pid:
            print(f"信息：当前脚本 (PID: {current_pid}, 名称: {proc_obj.Name}) 是 VRCLS.exe，将被保留。")
            is_current_vrcls = True
        else:
            other_vrcls_pids.append(proc_obj.ProcessId)

    if not other_vrcls_pids:
        if is_current_vrcls:
            print("信息：没有其他 'VRCLS.exe' 进程需要终止，仅当前脚本实例运行。")
        else:
            print("信息：没有其他 'VRCLS.exe' 进程需要终止。(当前脚本非VRCLS.exe)")
        if wmi: del wmi
        if service: del service
        return

    print(f"准备终止以下 'VRCLS.exe' 进程 PID: {other_vrcls_pids}")
    
    killed_count = 0
    failed_count = 0

    for pid_to_kill in other_vrcls_pids:
        print(f"尝试终止进程 PID: {pid_to_kill}...")
        
        # 方案1: 使用 WMI Terminate (原始方法)
        terminated_by_wmi = False
        # 需要重新获取 WMI 对象才能调用 Terminate 方法，或者在上面循环时就尝试
        # 为了简化，我们直接用 taskkill，如果需要 WMI Terminate，可以这样：
        # for proc_obj in processes_to_check:
        #     if proc_obj.ProcessId == pid_to_kill: # 确保是我们要杀的那个
        #         try:
        #             result_code = proc_obj.Terminate() # Terminate 返回 0 表示成功
        #             if result_code == 0:
        #                 print(f"  WMI 成功终止进程: {pid_to_kill}")
        #                 killed_count += 1
        #                 terminated_by_wmi = True
        #             else:
        #                 print(f"  WMI 终止进程 {pid_to_kill} 失败，返回码: {result_code}. 尝试使用 taskkill...")
        #         except Exception as e_wmi:
        #             print(f"  WMI 终止进程 {pid_to_kill} 异常: {str(e_wmi)}. 尝试使用 taskkill...")
        #         break # 找到了就跳出内部循环

        # if terminated_by_wmi:
        #     continue

        # 方案2: 使用 taskkill (更强制)
        try:
            # CREATE_NO_WINDOW 防止 taskkill 命令执行时弹出命令行窗口
            # text=True (或 universal_newlines=True) 使 stdout/stderr 为字符串
            # check=False 让我们手动检查 returncode
            result = subprocess.run(
                ["taskkill", "/F", "/PID", str(pid_to_kill)],
                capture_output=True,
                text=True,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW 
            )
            
            if result.returncode == 0:
                print(f"  成功: 进程 {pid_to_kill} 已通过 taskkill 终止。")
                killed_count += 1
            else:
                # taskkill 常见错误码:
                # 128: 进程未找到 (可能在你尝试终止它之前就已经退出了)
                # 1:   拒绝访问 (权限问题) 或其他操作失败
                error_message = f"  失败: 无法通过 taskkill 终止进程 {pid_to_kill}。"
                if result.stderr:
                    error_message += f" 原因: {result.stderr.strip()}"
                elif result.stdout: # 有时错误信息在 stdout
                     error_message += f" 输出: {result.stdout.strip()}"
                else:
                    error_message += f" taskkill 返回码: {result.returncode}"
                print(error_message)
                failed_count += 1
                
        except FileNotFoundError:
            print(f"  错误: 'taskkill' 命令未找到。请确保它在系统 PATH 中。")
            failed_count += 1 # 计为失败
        except Exception as e_taskkill:
            print(f"  错误: 使用 taskkill 终止进程 {pid_to_kill} 时发生意外: {str(e_taskkill)}")
            failed_count += 1

    print(f"\n总结：")
    print(f"  成功终止 {killed_count} 个进程。")
    if failed_count > 0:
        print(f"  未能终止 {failed_count} 个进程。请检查上面的错误信息和脚本权限。")
    
    # 显式释放COM对象
    if service:
        del service
    if wmi:
        del wmi
class stopSignal(Exception):

    pass
def enable_vt_mode():
    if sys.platform != 'win32':
        return  # 仅Windows需要处理

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    STD_OUTPUT_HANDLE = -11

    # 获取标准输出句柄
    hConsole = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hConsole == -1 or hConsole is None:
        return  # 非控制台环境（如重定向到文件）

    # 获取当前控制台模式
    mode = wintypes.DWORD()
    if not kernel32.GetConsoleMode(hConsole, ctypes.byref(mode)):
        return  # 获取模式失败

    # 检查是否已启用虚拟终端
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x4
    if (mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING) == 0:
        # 设置新模式（原模式 + 虚拟终端标志）
        kernel32.SetConsoleMode(hConsole, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    ENABLE_QUICK_EDIT = 0x0040

    # 获取标准输入句柄
    h_input = kernel32.GetStdHandle(-10)  # -10对应STD_INPUT_HANDLE
    if h_input == -1:
        print("获取句柄失败")
        exit(1)

    # 获取当前控制台模式
    prev_mode = wintypes.DWORD()
    if not kernel32.GetConsoleMode(h_input, ctypes.byref(prev_mode)):
        print("获取模式失败")
        exit(1)

    # 禁用快速编辑模式
    new_mode = prev_mode.value & ~ENABLE_QUICK_EDIT
    if not kernel32.SetConsoleMode(h_input, new_mode):
        print("设置模式失败")
        exit(1)
    
def toggle_console(show: bool):
    if sys.platform == 'win32':
        console_handler = ctypes.windll.kernel32.GetConsoleWindow()
        if console_handler != 0:
            ctypes.windll.user32.ShowWindow(console_handler, 1 if show else 0)

import winreg

def check_webview2_registry():
    reg_paths = [
        r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}",  # 64位系统
        r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"             # 32位系统
    ]
    try:
        for path in reg_paths:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            version, _ = winreg.QueryValueEx(key, "pv")
            if version > "0.0.0.0":
                return True
    except FileNotFoundError:
        pass
    return False

import platform

def get_system_arch():
    arch = platform.machine().lower()
    return "x64" if "64" in arch else "x86"

def download_webview2_runtime(arch):
    base_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
    download_url = f"{base_url}&arch={arch}"
    return download_url
processList=[]
app = Flask(__name__,static_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key' 
socketio = SocketIO(app, cors_allowed_origins="*",async_mode='threading')

def rebootJob():
    global queue,params,listener_thread,listener_thread,startUp,sendClient,manager,steamvrQueue
    queue.put({"text":"/reboot","level":"debug"})
    queue.put({"text":"sound process start to complete|| 程序开始重启 ","level":"info"})
    params["running"] = False
    while not params["micStopped"] and ( startUp.config.get("Separate_Self_Game_Mic") == 0 or not params["gameStopped"]):time.sleep(1)
    params['headers']=startUp.run()
    params["runmode"]= startUp.config["defaultMode"]
    time.sleep(3)
    params["VRCBitmapLed_taskList"]=manager.list()
    if startUp.config.get("textInSteamVR"):
        steamvrThread=Process(target=steamvr_process,daemon=True,args=(queue,steamvrQueue,params))
        steamvrThread.start()
    if startUp.config.get("localizedSpeech"):
        listener_thread = Process(target=sherpa_onnx_run,args=(sendClient,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
    else:
        listener_thread = Process(target=selfMic_listen,args=(sendClient,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
    listener_thread.start()
    if startUp.config.get("Separate_Self_Game_Mic")==1:
        listener_thread1 = Process(target=sherpa_onnx_run_local if startUp.config.get("localizedCapture") else gameMic_listen_capture,args=(sendClient,params,queue,startUp.loopbackIndexList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
        listener_thread1.start()
    elif startUp.config.get("Separate_Self_Game_Mic")==2:
        listener_thread1 = Process(target=sherpa_onnx_run_mic if startUp.config.get("localizedCapture") else gameMic_listen_VoiceMeeter,args=(sendClient,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
        listener_thread1.start()
    if startUp.config.get('enableOscServer'):
        oscServerTread=td.Thread(target=startServer,args=(params,queue),daemon=True)
        oscServerTread.start()



    
    params["running"] = True
    params["micStopped"] = False
    params["gameStopped"] = False
    params['serverdata']=''
    params['clientdata']=''
    params["tragetTranslateLanguage"]=startUp.config.get("targetTranslationLanguage")
    params["sourceLanguage"]=startUp.config.get("sourceLanguage")
    params["localizedCapture"]=startUp.config['localizedCapture']
    params["localizedSpeech"]=startUp.config['localizedSpeech']
    queue.put({"text":"sound process restart complete|| 程序完成重启","level":"info"})
@app.route('/api/saveConfig', methods=['post'])
def saveConfig():
    global queue,params,listener_thread,startUp,sendClient,window
    data=request.get_json()
    queue.put({"text":"/saveandreboot","level":"debug"})
    try:
        with open(startUp.path_dict['client.json'], 'r',encoding='utf8') as file, open(startUp.path_dict['client-back.json'], 'w', encoding="utf8") as f:
            f.write(file.read())
        with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(data["config"],ensure_ascii=False, indent=4))
        # if startUp.config.get("darkmode") != data["config"].get("darkmode"):
        #     set_window_frame_color_windows(window.hwnd,data["config"].get("darkmode"))
        if startUp.config.get("Separate_Self_Game_Mic") != data["config"].get("Separate_Self_Game_Mic"):
            queue.put({"text":f"请关闭整个程序后再重启程序","level":"info"})
            return jsonify({"text":"请关闭整个程序后再重启程序"}),220
        if startUp.config.get("CopyBox") != data["config"].get("CopyBox"):
            queue.put({"text":f"请关闭整个程序后再重启程序","level":"info"})
            return jsonify({"text":"请关闭整个程序后再重启程序"}),220
        if startUp.config.get("localizedSpeech") != data["config"].get("localizedSpeech"):
            queue.put({"text":f"请关闭整个程序后再重启程序","level":"info"})
            return jsonify({"text":"请关闭整个程序后再重启程序"}),220
        if startUp.config.get("localizedCapture") != data["config"].get("localizedCapture"):
            queue.put({"text":f"请关闭整个程序后再重启程序","level":"info"})
            return jsonify({"text":"请关闭整个程序后再重启程序"}),220
        if startUp.config.get("textInSteamVR") != data["config"].get("textInSteamVR"):
            queue.put({"text":f"请关闭整个程序后再重启程序","level":"info"})
            return jsonify({"text":"请关闭整个程序后再重启程序"}),220
        startUp.config=data["config"]
        params["config"]=data["config"]
    except Exception as e:
        queue.put({"text":f"config saved 配置保存异常:{e}","level":"warning"})
        return jsonify({"text":f"config saved 配置保存异常:{e}","level":"warning"}),401
    queue.put({"text":"config saved 配置保存完毕","level":"info"})
    return jsonify("保存成功"),200

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
@app.route('/api/closewindow', methods=['get'])
def closewindow():
    global window
    window.destroy()
    return 'ok',200

@app.route('/api/maximize', methods=['get'])
def fullscreen():
    global window
    window.maximize()
    return 'ok',200
@app.route('/api/minimize', methods=['get'])
def minimize():
    global window
    window.minimize()
    return 'ok',200

@app.route('/api/windowrestore', methods=['get'])
def windowrestore():
    global window
    window.restore()
    return 'ok',200

@app.route('/api/reboot', methods=['get'])
def reboot():
    rebootJob()
    return jsonify({'message':'sound process restart complete|| 程序完成重启'}),200
 
@app.route('/api/verion', methods=['get'])
def verion():
    return jsonify({'text':VERSION_NUM}),200
# 处理表单提交
@app.route('/api/saveandreboot', methods=['post'])
def update_config():
    data=request.get_json(silent=True)
    if data is None: return jsonify({'text':'no data'}),400
    config=saveConfig()
    rebootJob() 
    return jsonify(config),200
@app.route('/api/sendTextandTranslate', methods=['post'])
def sendTextandTranslate():
    import html
    import translators
    from hanziconv import HanziConv
    from src.module.translate import other_trasnlator
    from src.handler.SelfRead import SelfReadHandler
    def replace_multiple_placeholders(template: str, replacements: dict) -> str:
        """通过字典替换多个占位符"""
        return template.format(**replacements)
    global params,queue,steamvrQueue,sendClient
    res=request.get_json(silent=True)
    logger=queue
    selfRead=SelfReadHandler(logger=logger,osc_client=sendClient,steamvrQueue=steamvrQueue,params=params)
    baseurl=params["config"].get('baseurl')
    translator=params["config"].get('translateService')
    tragetTranslateLanguage2=params["config"].get("targetTranslationLanguage2")
    tragetTranslateLanguage3=params["config"].get("targetTranslationLanguage3")
    tragetTranslateLanguage=params["tragetTranslateLanguage"]
    sourceLanguage=params["sourceLanguage"]
    if params["config"].get("translateService")!="developer":
        res['translatedText2']=''
        res['translatedText3']=''
        try:
            res['translatedText']=html.unescape(translators.translate_text(res["text"],translator=translator,from_language="zh" if sourceLanguage=="zt" else  sourceLanguage,to_language=tragetTranslateLanguage))
        except Exception as e:
            if all(i in str(e) for i in["from_language[","] and to_language[","] should not be same"]):
                logger.put({"text":f"翻译语言检测同语言：{e}","level":"debug"})
                res['translatedText']=res["text"]
            else:
                logger.put({"text":f"翻译异常,请尝试更换翻译引擎：{str(e)}","level":"error"})
                logger.put({"text":f"翻译异常：{traceback.format_exc()}","level":"debug"})
                res['translatedText']=''
                return '翻译异常',401
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
                logger.put({"text":f"文字发送请翻译过于频繁,可以尝试更换其他翻译引擎,触发规则{res.get("limit")}","level":"warning"})
            else:    
                logger.put({"text":f"文字发送翻译数据接收异常:{response.text}","level":"warning"})
            return '翻译异常',401
        # 解析JSON响应
        res = response.json()
        logger.put({"text":f"服务器翻译成功：","level":"debug"})

    if  params["runmode"] == "translation" and params["config"].get("translateService")!="developer":        
        # 第二语言
        if  tragetTranslateLanguage2!="none":
                res['translatedText2']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage2,res)
        # 第三语言
        if  tragetTranslateLanguage3!="none":
                res['translatedText3']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage3,res)
                
        
    if sourceLanguage== "zh":res["text"]=HanziConv.toSimplified(res["text"])
    elif sourceLanguage=="zt":res["text"]=HanziConv.toTraditional(res["text"])
    selfRead.handle(res,"文字发送",params["steamReady"])
    output=replace_multiple_placeholders(params['config']['VRCChatboxformat_new'],res)
    params['clientdata']=output
    return 'ok',200
@app.route('/api/getAvatarParameters', methods=['get'])
def getAvatarParameters():
    try:
        avatarInfo=OSCListener()
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
    return jsonify([item for item in startUp.micList if item != '']),200

@app.route('/api/getUpdate', methods=['get'])
def getUpdate():
    global queue,params
    queue.put({"text":"/getUpdate","level":"debug"})
    if params["updateInfo"].get('version','None')!='None':return jsonify({"info":params["updateInfo"],"changelog":params['updateChangeLog']}),200
    return jsonify({}),400
    
@app.route('/api/getOutputs', methods=['get'])
def getOutputs():
    global queue,startUp
    queue.put({"text":"/getOutputs","level":"debug"})
    return jsonify([item for item in startUp.outPutList if item != '']),200
@app.route('/api/getcapture', methods=['get'])
def getCapture():
    global queue,startUp
    queue.put({"text":"/getcapture","level":"debug"})

    Separate_Self_Game_Mic = int(request.args.get('Separate_Self_Game_Mic', 0))

    if Separate_Self_Game_Mic==2:return jsonify(startUp.micList),200
    elif Separate_Self_Game_Mic==1:return jsonify(startUp.loopbackList),200
    else :return jsonify([]),200

    
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
        

def get_db_connection():
    conn = sqlite3.connect('log_statistics.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/stats', methods=['GET'])
def get_stats():
    mode=request.args.get('mode')
    dayNum=request.args.get('dayNum')
    database='daily_stats' if mode=='true' else 'daily_fail_stats'
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 计算最近7天日期范围
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=int(dayNum))).strftime("%Y-%m-%d")
        
        # 查询最近7天数据（包含没有记录的日期）
        cursor.execute(f'''
            WITH dates(date) AS (
                VALUES (date(?))
                UNION ALL
                SELECT date(date, '+1 day')
                FROM dates
                WHERE date < date(?)
            )
            SELECT dates.date, COALESCE({database}.count, 0) AS count
            FROM dates
            LEFT JOIN {database} ON dates.date = {database}.date
            ORDER BY dates.date DESC
            LIMIT ?
        ''', (start_date, end_date,dayNum))
        
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/upgrade', methods=['get'])
def upgrade():
    toggle_console(True)
    from pathlib import Path
    global queue,params,logger_thread,startUp,listener_thread1,steamvrThread,stop_for_except
    queue.put({"text":"/api/upgrade","level":"debug"})
    if main_update(params["updateInfo"]['packgeURL'], Path(os.path.dirname(sys._MEIPASS))):
        stop_for_except=False
        raise stopSignal
    else:
        queue.put({"text":"请刷新配置网页重新开始更新任务","level":"warning"})
        return jsonify({"message":'请刷新配置网页重新开始更新任务'}),401
    
# ---------- 在主进程中启动WS发送线程 ----------
def ws_log_sender():
    global socketio,socketQueue
    while True:
        try:
            msg = socketQueue.get()
            if msg.get('shutdown'):
                break
            if msg.get('type')=='log':
                socketio.emit('log', {
                    'text': msg['text'],
                    'level': msg['level'],
                    'timestamp': msg.get('timestamp')
                })
            else:
                socketio.emit(msg.get('type'), {
                    'text': msg['text'],
                })
        except OSError as e:
            print(f"ws管道已结束:{str(e)}")
            return
        except Exception as e:
            print(f"WS发送异常: {traceback.format_exc()}")

@socketio.on('connect')
def handle_connect():
    emit('log', {'text': 'Connected to log server','level':'0','timestamp':''})
    
def run_server(app,host,port):
    global socketio
    socketio.run(app=app,debug=False, host=host, port=port,allow_unsafe_werkzeug=True)
    print('server exit')   
if __name__ == '__main__':
    freeze_support()
    if not is_admin():
        print("警告: 程序未以管理员权限运行。可能会出现问题。")
        print("请尝试右键单击脚本，选择“以管理员身份运行”。或者勾选程序属性-兼容性-以管理员身份启动此程序\n")
        input('可以直接关闭当前脚本或按任意键继续。。。。。。')
        # 可以选择在这里直接退出，或者继续尝试但提示可能失败
        # return
    
    
    
    if not check_webview2_registry():
        arch = get_system_arch()
        url_webview = download_webview2_runtime(arch)
        print(f'未检测到vebview环境\n请通过以下网页链接安装webview环境：{url_webview}')
        while not check_webview2_registry():time.sleep(5)
    
    print('''
          检测到vebview环境
          本窗口将自动关闭，程序启动......

          ''')
    show_console = '--show-console' in sys.argv
    # kill_other_vrcls()
    if show_console:enable_vt_mode()# 在程序启动时立即调用
    try:

        VERSION_NUM='v0.5.9'
        listener_thread=None
        startUp=None
        manager = Manager()
        params=manager.dict()
        queue=manager.Queue(-1)
        copyQueue=manager.Queue(-1)
        socketQueue=manager.Queue(-1)
        params["opencopybox"] = False
        params["running"] = True
        params["micStopped"] = False
        params["gameStopped"] = False
        params['serverdata']=''
        params['clientdata']=''
        stop_for_except=True


        logger_thread = td.Thread(target=logger_process,daemon=True,args=(queue,copyQueue,params,socketQueue))
        logger_thread.start()
        ws_thread = td.Thread(target=ws_log_sender, daemon=True)
        ws_thread.start()
        startUp=StartUp(queue,params)
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
                                                   

               当前版本: '''+str(VERSION_NUM)+r'''
                   
        '''+f'webUI: http://{startUp.config['api-ip']}:{startUp.config['api-port']}'+r''' 
                                                
        》》》》                  《《《《            
        》》》》请保持本窗口持续开启《《《《          
        》》》》                  《《《《                                 
    
        欢迎使用由VoiceLinkVR开发的VRCLS 
        本程序的开发者为boyqiu-001(boyqiu玻璃球)
        欢迎大家加入qq群1011986554获取最新资讯

        默认使用开发者云服务器免费测试账户,
        器限制每日800次请求.每分钟8次请求,
        可通过爱发电支持服务器运维提升日请求上限,
        并解锁请求速率限制,发电方式请加qq群查看群公告

        可以使用本地模型，无限制,延迟较低,但准确度较差
        本地识别模型会自动下载，也可群内手动下载

        如需获取更多服务器资源或技术支持请加qq群

------------------------------------------------------------------------
                    ''','level':'info'}
                    )
        params['headers']=startUp.run()
        params["config"]=startUp.config
        time.sleep(3)
        sendClient= startUp.setOSCClient(queue)
        params["VRCBitmapLed_taskList"]= manager.list()
        tmp=" "*(8 if startUp.config.get("VRCBitmapLed_row") is None else int(startUp.config.get("VRCBitmapLed_row")) )*(16 if int(startUp.config.get("VRCBitmapLed_col")) is None else int(startUp.config.get("VRCBitmapLed_col")))
        params["VRCBitmapLed_Line_old"]= tmp
        params["tragetTranslateLanguage"]=startUp.tragetTranslateLanguage
        params["sourceLanguage"]=startUp.sourceLanguage
        params["localizedCapture"]=startUp.config['localizedCapture']
        params["localizedSpeech"]=startUp.config['localizedSpeech']
        params["TTSToggle"]=startUp.config['TTSToggle']
        params["updateInfo"]={'version':'None'}
        params["vrcMuteSelf"]=False
        if getattr(sys, 'frozen', False):
            queue.put({'text':"update check||开始版本更新检查",'level':'warning'})
            response = requests.get(startUp.config['baseurl']+"/latestVersionInfo")
            try:
                res=response.json()
                if response.status_code==200:
                    res=response.json()
                    if VERSION_NUM!= res['version']:
                        queue.put({'text':"need to update||需要更新",'level':'info'})
                        params["updateInfo"]=res
                        response = requests.get('https://cloudflarestorage.boyqiu001.top/VRCLS_changeLog.md')
                        params['updateChangeLog']=response.text
                    else:
                            queue.put({'text':"no need to update||当前处于最新版，无需更新",'level':'info'})
                else:
                    queue.put({'text':"update check failed||版本更新检查异常",'level':'warning'})
                    queue.put({'text':response.text,'level':'debug'})
            except requests.exceptions.JSONDecodeError:
                queue.put({'text':"update check failed||版本更新检查异常",'level':'warning'})
                queue.put({'text':traceback.format_exc(),'level':'debug'})
            except Exception:
                queue.put({'text':"update check failed||版本更新检查异常",'level':'warning'})
                queue.put({'text':traceback.format_exc(),'level':'debug'})
                    
            
        queue.put({'text':"vrc udpClient ok||发送准备就绪",'level':'info'})
        params["runmode"]= startUp.config["defaultMode"]
        params["steamReady"]=False

        steamvrQueue=Queue(-1)
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        # this is called from the background thread
        if startUp.config.get("textInSteamVR"):
            steamvrThread=td.Thread(target=steamvr_process,daemon=True,args=(queue,steamvrQueue,params))
            steamvrThread.start()
        if startUp.config.get("localizedSpeech"):
            listener_thread = Process(target=sherpa_onnx_run,args=(sendClient,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
        else:
            listener_thread = Process(target=selfMic_listen,args=(sendClient,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
        listener_thread.start()
        if startUp.config.get("Separate_Self_Game_Mic")==1:
            listener_thread1 = Process(target=sherpa_onnx_run_local if startUp.config.get("localizedCapture") else gameMic_listen_capture,args=(sendClient,params,queue,startUp.loopbackIndexList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
            listener_thread1.start()
        elif startUp.config.get("Separate_Self_Game_Mic")==2:
            listener_thread1 = Process(target=sherpa_onnx_run_mic if startUp.config.get("localizedCapture") else gameMic_listen_VoiceMeeter,args=(sendClient,params,queue,startUp.micList,startUp.defautMicIndex,startUp.filter,steamvrQueue,startUp.customEmoji,startUp.outPutList,startUp.ttsVoice))
            listener_thread1.start()
        if startUp.config.get('enableOscServer'):
            oscServerTread=td.Thread(target=startServer,args=(params,queue),daemon=True)
            oscServerTread.start()
        if startUp.config.get('voiceMode')==3 or startUp.config.get('gameVoiceMode')==3:
            queue.put({'text':"micStatusListenerThread start",'level':'info'})
            vrcListenThread=td.Thread(target=micStatusListenerThread,args=(queue,params),daemon=True)
            vrcListenThread.start()
            
        
        queue.put({'text':"api ok||api就绪",'level':'info'})
        # open_web(startUp.config['api-ip'],startUp.config['api-port'])
        server_thread=td.Thread(target=run_server, daemon=True,args=(app,startUp.config['api-ip'],startUp.config['api-port']))
        server_thread.start()
        import webview
    
        window = webview.create_window(
            'VRCLS控制面板', 
            f'http://{startUp.config['api-ip']}:{startUp.config['api-port']}',
            width=1200,
            height=900,frameless=True, easy_drag=False,resizable=True
        )
        toggle_console(show_console)
        webview.start()
        
        
    except Exception as e:
        queue.put({'text':traceback.format_exc(),'level':'error'})
        time.sleep(3)
    finally:
        params["running"]=False
        socketio.stop()
        
        
        # logger_thread.terminate()
        
        if listener_thread:
            try:
                listener_thread.terminate()
            except:
                traceback.print_exc()
        if startUp:
            if startUp.config.get("Separate_Self_Game_Mic")!=0: 
                try:
                    listener_thread1.terminate()
                except:traceback.print_exc()
            # if startUp.config.get("textInSteamVR"):
            #     try:steamvrThread.terminate()
            #     except:traceback.print_exc()
        
        if stop_for_except:
            print("press any key to exit||任意键退出...")
        else:
            print("窗口即将自动关闭，将在30s内自动重启")
        # 设置退出事件来通知所有子线程
