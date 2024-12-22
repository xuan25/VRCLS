import speech_recognition as sr
from pythonosc import udp_client
import json
import time
from selflogger import getlogger
logger =getlogger("client",'client.log')
import requests
import winsound
# 设置一个标志变量来控制循环
defaultConfig={
    "userInfo":{"username":"","password":""},
    "baseurl":"https://whisper.boyqiu001.cn:7070",
    "port":9000,
    "ip":"127.0.0.1",
    "defaultMode":"control",
    "exitText":"关闭语音助手",
    "activateText":"",
    "stopText":"",
    "sourceLanguage":"zh",
    "targetTranslationLanguage":"en",
    "defaultScripts":[
        {
            "action":"changToTrans",
            "text":["切换到翻译模式","到翻译模式"],
        },
        {
            "action":"changToControl",
            "text":["切换到控制模式","到控制模式"],
        },
        {
            "action":"changToEnglish",
            "text":["切换到英语翻译"]
        },
        {
            "action":"changTojapanese",
            "text":["切换到日语翻译"]
        },
        {
            "action":"changToRussian",
            "text":["切换到俄语翻译"]
        },
        {
            "action":"changToKorean",
            "text":["切换到韩语翻译"]
        }
    ],
    "scripts":[
        {
            "action":"toggle Mic",
            "text":["切换麦克风","切換麥克風"],
            "vrcActions":[
                {
                    "vrcPath":"/input/Voice",
                    "vrcValue":0
                },
                {
                    "vrcPath":"/input/Voice",
                    "vrcValue":1
                },
                {
                    "vrcPath":"/input/Voice",
                    "vrcValue":0
                }
            ]

        },
        {
            "action":"blackCloth",
            "text":["黑色衣服"],            
            "vrcActions":[
                {
            "vrcPath":"/avatar/parameters/Change_material",
            "vrcValue":0
                }
            ]
        },
        {
            "action":"whiteCloth",
            "text":["白色衣服"],
            "vrcActions":[
                {
            "vrcPath":"/avatar/parameters/Change_material",
            "vrcValue":0.5
                }
            ]

        },
        {
            "action":"openBaseballBat",
            "text":["打开棒球棒"],
            "vrcActions":[
                {
                    "vrcPath":"/avatar/parameters/IsBaseballBat",
                    "vrcValue":1
                }
            ]
        },
        {
            "action":"closeBaseballBat",
            "text":["关闭棒球棒"],
            "vrcActions":[
                {
                    "vrcPath":"/avatar/parameters/IsBaseballBat",
                    "vrcValue":0
                }
            ]

        },
        {
            "action":"openTailCloud",
            "text":["打开尾巴云朵"],
            "vrcActions":[{
            "vrcPath":"/avatar/parameters/TailCloud",
            "vrcValue":1
                }
            ]
        },
        {
            "action":"closeTailCloud",
            "text":["关闭尾巴云朵"],
            "vrcActions":[{
            "vrcPath":"/avatar/parameters/TailCloud",
            "vrcValue":0
                }
            ]

        }
    
    ]
}

running = True
try:
    try:
        with open('client.json', 'r',encoding='utf-8') as file:
            config:dict = json.load(file)
            configDiff=list(set(defaultConfig.keys())-set(config.keys()))
        if configDiff != []:
            logger.info("配置文件更新,增加条目："+str(configDiff))
            for newConfig in configDiff:
                config[newConfig]=defaultConfig[newConfig]
            with open('client.json', 'w', encoding="utf8") as file:
                file.write(json.dumps(config,ensure_ascii=False, indent=4))
        configDefaultScripts=[script["action"] for script in config["defaultScripts"]]
        defaultScriptsDiff=[script for script in defaultConfig["defaultScripts"] if script["action"] not in configDefaultScripts]
        if defaultScriptsDiff != []:
            logger.info("配置文件更新,增加默认指令条目："+str(defaultScriptsDiff))
            for newConfig in defaultScriptsDiff:
                config["defaultScripts"].append(newConfig)
            with open('client.json', 'w', encoding="utf8") as file:
                file.write(json.dumps(config,ensure_ascii=False, indent=4))
    except requests.exceptions.JSONDecodeError as e:
        logger.warning("配置文件异常,详情："+str(e.strerror))
        time.sleep(10)
        exit(0)
except FileNotFoundError:
    with open('client.json', 'w', encoding="utf8") as f:
        f.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
    with open('client.json', 'w', encoding="utf8") as f:
        defaultConfig["userInfo"]["username"] = input("请输入用户名: ")
        defaultConfig["userInfo"]["password"] = input("请输入密码: ")
        f.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
        config=defaultConfig

while True:
    time.sleep(0.1)
    if config["userInfo"]["username"] == "" or config["userInfo"]["password"] == "" or config["userInfo"]["username"] is None or config["userInfo"]["password"] is None:
        logger.warning("userinfo empty , please enter again||无用户信息请重新输入")
        config["userInfo"]["username"] = input("请输入用户名: ")
        config["userInfo"]["password"] = input("请输入密码: ")
        continue
    baseurl=config["baseurl"]
    response = requests.post(baseurl+"/login",json=config["userInfo"])
    if response.status_code != 200: 
        logger.debug(response.text)
        logger.warning("password or account error , please enter again||账户或密码错误,请重新输入")
        config["userInfo"]["username"] = input("请输入用户名: ")
        config["userInfo"]["password"] = input("请输入密码: ")
        continue
    with open('client.json', 'w', encoding="utf8") as f:
        f.write(json.dumps(config,ensure_ascii=False, indent=4))
    break


res=response.json()
headers={'Authorization': 'Bearer '+res["access_token"]}
r = sr.Recognizer()
m = sr.Microphone()
sendClient = udp_client.SimpleUDPClient(config["ip"],config["port"])
logger.info("vrc udpClient ok||发送准备就绪")
runmode= config["defaultMode"]
tragetTranslateLanguage="en" if config["targetTranslationLanguage"] is None or  config["targetTranslationLanguage"] == "" else config["targetTranslationLanguage"]
whisperSupportedLanguageList=["af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es"
                              ,"et","eu","fa","fi","fo","fr","gl","gu","ha","haw","he","hi","hr","ht","hu","hy","id","is","it",
                              "ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms",
                              "mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq",
                              "sr", "su", "sv","sw","ta", "te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","yue","zh"]
sourceLanguage="zh" if config["sourceLanguage"] =="" else config["sourceLanguage"]
if sourceLanguage not in whisperSupportedLanguageList:
    logger.warning('please check your sourceLanguage in config,please choose one in following list\n 请检查sourceLanguage配置是否正确 请从下方语言列表中选择一个(中文是 zh)\n list:'+str(whisperSupportedLanguageList))
    input("press any key to exit||按下任意键退出...")

# this is called from the background thread
def callback(recognizer, audio):
    global running 
    global runmode
    global tragetTranslateLanguage
    global sourceLanguage
    try:

        logger.debug("音频输出完毕")
        if runmode == "control":
            url=baseurl+"/whisper/transcriptions"
        elif runmode == "trasnlation":
            if tragetTranslateLanguage=="en":url=baseurl+"/func/translateToEnglish"
            else:url=baseurl+"/func/translateToOtherLanguage"
        else: 
            logger.error("运行模式异常,运行默认控制模式")
            runmode = "control"
            url = baseurl+"/whisper/transcriptions"
        logger.debug(f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}")
        response = requests.post(url,files={"file":audio.get_wav_data()},data={"targetLanguage":tragetTranslateLanguage},headers=headers)
        if response.status_code != 200: 
            logger.warning(f"数据接收异常:{response.text}")
            return
        res = response.json()
    except sr.UnknownValueError:
        logger.info("无法理解这个语音")
        return
    except sr.RequestError as e:
        logger.warning("识别服务无法达到; 检查您的互联网连接或者是服务本身是否下线")
        return
    except sr.WaitTimeoutError:
        logger.info("说话超时")
    except requests.exceptions.JSONDecodeError:
        logger.warning("json解析异常,code:"+str(response.status_code)+" info:"+response.text)
        return
    except Exception as e:
        logger.warning("未知异常："+str(e))
        return
    logger.debug("你说的是: " + res["text"])
    if res["text"] =="":
        logger.debug("返回值过滤")
        return
    if isdefaultCommand(res["text"]):return
    if runmode == "control":controlFunction(res)
    if runmode == "trasnlation":translateFunction(res)

def isdefaultCommand(text):
    global runmode
    global tragetTranslateLanguage
    global sourceLanguage
    for dafaultcommand in config["defaultScripts"]:
        if any( command in text for command in dafaultcommand["text"]):
            if dafaultcommand["action"]=="changToTrans":
                if runmode =="trasnlation":
                    logger.info("No need to modify mode. Currently in translation mode ||无需修改模式 当前处于翻译模式")
                    return False
                logger.info("change to translation mode ||切换至翻译模式")
                runmode="trasnlation"
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                return True
            if dafaultcommand["action"]=="changToControl":
                if runmode =="control":
                    logger.info("No need to change mode. Currently in control mode ||无需修改模式 当前处于控制模式")
                    return False
                logger.info("change to control mode ||切换至控制模式")
                runmode="control"
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                return True
            if dafaultcommand["action"]=="changToEnglish":
                if tragetTranslateLanguage == "en":
                    logger.info("No need to change mode. Currently in english translation||无需修改模式 当前翻译输出语言为 英语")
                    return False
                logger.info("change translation to english ||将翻译切换为英语")
                tragetTranslateLanguage="en"
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                return True
            if dafaultcommand["action"]=="changTojapanese":
                if tragetTranslateLanguage =="ja":
                    logger.info("No need to change mode. Currently in english translation||无需修改模式 当前翻译输出语言为 日语")
                    return False
                logger.info("change translation to japanese ||将翻译切换为日语")
                tragetTranslateLanguage="ja"
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                return True
            if dafaultcommand["action"]=="changToRussian":
                if tragetTranslateLanguage =="ru":
                    logger.info("No need to change mode. Currently in russian translation||无需修改模式 当前翻译输出语言为 俄语")
                    return False
                logger.info("change translation to russian ||将翻译切换为俄语")
                tragetTranslateLanguage="ru"
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                return True
            if dafaultcommand["action"]=="changToKorean":
                if tragetTranslateLanguage =="ko":
                    logger.info("No need to change mode. Currently in Korean translation||无需修改模式 当前翻译输出语言为 韩语")
                    return False
                logger.info("change translation to Korean ||将翻译切换为韩语")
                tragetTranslateLanguage="ko"
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
                return True
    return False
def translateFunction(res):
    global running
    text=res['text']
    transtext=res['translatedText']
    logger.info(f"输出文字: {transtext}({text})")
    sendClient.send_message("/chatbox/input",[ f'{transtext}({text})', True, False])
    
def controlFunction(res):
    text=res['text']
    global running
    if config["activateText"] == "":
        logger.info("无头命令:"+text)
        if text == config["exitText"]:
            stop_listening(wait_for_stop=False)
            running = False
            exit(0)
        for script in config["scripts"]:
            if any( command in text  for command in script["text"]):
                logger.info("执行命令:"+script["action"])
                for vrcaction in script["vrcActions"]:
                    sendClient.send_message(vrcaction["vrcPath"],vrcaction["vrcValue"])
                    time.sleep(0.1)
                winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
    elif config["activateText"] in text:
        commandlist=text.split(config["activateText"])
        command=commandlist[-1]
        if (config["stopText"] in command) or config["stopText"] == "":
            if config["stopText"] != "":command=command.split(config["stopText"])[0]
            logger.info("有头命令:"+command)
            if command == config["exitText"]:
                stop_listening(wait_for_stop=False)
                running = False
                exit(0)
            for script in config["scripts"]:
                if command in script["text"]:
                    logger.info("执行命令:"+script["text"])
                    for vrcaction in script["vrcActions"]:
                        sendClient.send_message(vrcaction["vrcPath"],vrcaction["vrcValue"])
                        time.sleep(0.1)
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)


logger.info("开始音量测试")
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
logger.info("结束音量测试")
# start listening in the background (note that we don't have to do this inside a `with` statement)

stop_listening = r.listen_in_background(m, callback)
logger.info("program started complete||程序启动完毕")
winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
# `stop_listening` is now a function that, when called, stops background listening
while running:time.sleep(0.00001)
