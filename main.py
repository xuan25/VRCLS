from flask import Flask, request, redirect, url_for,jsonify
from configparser import ConfigParser
import waitress
from src.core.startup import StartUp
from multiprocessing import Process,Manager,freeze_support,Queue
from src.core.process import logger_process,threaded_listen
import time
queue=Queue(-1)
processList=[]
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 用于 Flask 的会话管理
# logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
# app.logger=MyLogger().getlogger(filepath="VRCLSweb.log")
# 配置文件路径
CONFIG_FILE_PATH = 'config.ini'
 
# 读取配置文件
def read_config():
    parser = ConfigParser()
    parser.read(CONFIG_FILE_PATH)
    return parser
 
# 写入配置文件
def write_config(parser):
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        parser.write(configfile)
 
# 处理表单提交
@app.route('/getConfig', methods=['get'])
def update_config():
    global queue,params,listener_thread
    
    params["running"] = False
    queue.put({"text":"123123","level":"info"})
    while listener_thread.is_alive():time.sleep(1)
    listener_thread = Process(target=threaded_listen,args=(baseurl,sendClient,startUp.config,headers,params,queue))
    listener_thread.start()
    queue.put({"text":"31231","level":"info"})
    return jsonify({"1":"2"}),200


# # 处理表单提交
# @app.route('/update', methods=['POST'])
# def update_config():
#     data = request.get_json()
#     config = data.get('config')
#     data.get('is_restart')
#     is_ = read_config()
#     return redirect(url_for('index'))
 
 
if __name__ == '__main__':
    freeze_support()

    logger_thread = Process(target=logger_process,daemon=True,args=(queue,))
    logger_thread.start()
    manager = Manager()
    params=manager.dict()

    queue.put({'text':'''
                          
    欢迎使用由VoiceLinkVR开发的VRCLS
    本程序的开发这为boyqiu-001(boyqiu玻璃球)
    欢迎大家加入qq群1011986554获取最新资讯
    目前您使用的时公测账户,限制每日2000次请求
    如需获取更多资源请加群
                ''','level':'info'}
                )

    params["running"] = True


    startUp=StartUp(queue)
    headers=startUp.run()
    sendClient= startUp.setOSCClient(queue)
    baseurl=startUp.config.get("baseurl")

    params["tragetTranslateLanguage"]=startUp.tragetTranslateLanguage
    params["sourceLanguage"]=startUp.sourceLanguage

    queue.put({'text':"vrc udpClient ok||发送准备就绪",'level':'info'})
    params["runmode"]= startUp.config["defaultMode"]

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    # this is called from the background thread


    listener_thread = Process(target=threaded_listen,args=(baseurl,sendClient,startUp.config,headers,params,queue))
    listener_thread.start()
    
    # time.sleep(10)

    # while True:time.sleep(1)
    # app.run(debug=True,)
    queue.put({'text':"api ok||api就绪",'level':'info'})
    waitress.serve(app=app, host='0.0.0.0', port=8980)
