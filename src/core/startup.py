import json
from .defaultConfig import defaultConfig
from .osc_client import OSCClient
import requests
import time
import pyaudio
class StartUp:
    def __init__(self,logger):
        self.logger=logger
        self.tragetTranslateLanguage="en"
        self.micList=[]
        self.defautMicIndex=0
        try:
            with open('client.json', 'r',encoding='utf-8') as file:
                self.config:dict = json.load(file)
        except FileNotFoundError:
            with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
                self.config=defaultConfig
        except requests.exceptions.JSONDecodeError as e:
            self.logger.put({'text':"配置文件异常,详情："+str(e.strerror),"level":"error"})
            time.sleep(10)
            exit(0)

    def setOSCClient(self,logger):
        self.oscClient=OSCClient(logger=logger,host=self.config.get("osc-ip"),port=self.config.get("osc-port"))
        return self.oscClient.client
    def run(self):
        self.getMics()
        self.configCheck()
        res= self.checkAccount()
        return res
    def configCheck(self):
        try:
            with open('client.json', 'r',encoding='utf-8') as file:
                self.config:dict = json.load(file)
                configDiff=list(set(defaultConfig.keys())-set(self.config.keys()))
            if configDiff != []:
                self.logger.put({'text':"配置文件更新,增加条目："+str(configDiff),"level":"info"})
                for newConfig in configDiff:
                    self.config[newConfig]=defaultConfig[newConfig]
                with open('client.json', 'w', encoding="utf8") as file:
                    file.write(json.dumps(self.config,ensure_ascii=False, indent=4))
            configDefaultScripts=[script["action"] for script in self.config["defaultScripts"]]
            defaultScriptsDiff=[script for script in defaultConfig["defaultScripts"] if script["action"] not in configDefaultScripts]
            if defaultScriptsDiff != []:
                self.logger.put({'text':"配置文件更新,增加默认指令条目："+str(defaultScriptsDiff),"level":"info"})
                for newConfig in defaultScriptsDiff:
                    self.config["defaultScripts"].append(newConfig)
                with open('client.json', 'w', encoding="utf8") as file:
                    file.write(json.dumps(self.config,ensure_ascii=False, indent=4))
        except requests.exceptions.JSONDecodeError as e:
            self.logger.put({'text':"配置文件异常,详情："+str(e.strerror),"level":"warning"})
            time.sleep(10)
            exit(0)
        self.tragetTranslateLanguage="en" if self.config["targetTranslationLanguage"] is None or  self.config["targetTranslationLanguage"] == "" else self.config["targetTranslationLanguage"]
        whisperSupportedLanguageList=["af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es"
                                    ,"et","eu","fa","fi","fo","fr","gl","gu","ha","haw","he","hi","hr","ht","hu","hy","id","is","it",
                                    "ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms",
                                    "mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq",
                                    "sr", "su", "sv","sw","ta", "te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","yue","zh","zt"]
        self.sourceLanguage="zh" if self.config["sourceLanguage"] =="" else self.config["sourceLanguage"]
        if  self.sourceLanguage not in whisperSupportedLanguageList:
            self.logger.put({'text':'please check your sourceLanguage in config,please choose one in following list\n 请检查sourceLanguage配置是否正确 请从下方语言列表中选择一个(中文是 zh)\n list:'+str(whisperSupportedLanguageList),"level":"warning"})
            input("press any key to exit||按下任意键退出...")
            exit(0)
    def checkAccount(self):


        while True:
            time.sleep(0.1)
            if self.config["userInfo"]["username"] == "" or self.config["userInfo"]["password"] == "" or self.config["userInfo"]["username"] is None or self.config["userInfo"]["password"] is None:
                self.logger.put({'text':"userinfo empty , please enter again||无用户信息请重新输入","level":"warning"})
                self.config["userInfo"]["username"] = input("请输入用户名: ")
                self.config["userInfo"]["password"] = input("请输入密码: ")
                continue
            baseurl=self.config["baseurl"]
            response = requests.post(baseurl+"/login",json=self.config["userInfo"])
            if response.status_code != 200: 
                self.logger.put({'text':response.text,"level":"debug"})
                self.logger.put({'text':"password or account error , please enter again||账户或密码错误,请重新输入","level":"warning"})
                self.config["userInfo"]["username"] = input("请输入用户名: ")
                self.config["userInfo"]["password"] = input("请输入密码: ")
                continue
            with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(self.config,ensure_ascii=False, indent=4))
            break

        res=response.json()
        return {'Authorization': 'Bearer '+res["access_token"]}
    def getMics(self):
        # 创建 PyAudio 实例
        p = pyaudio.PyAudio()
        host_api_count=p.get_host_api_count()
        
        # 获取设备数量
        device_count = p.get_device_count()
    
        hostapis=[]
        for j in range(host_api_count):
            hostapi=p.get_host_api_info_by_index(j)
            hostapis.append(hostapi["name"])
        for i in range(device_count):
            # 获取每个设备的详细信息
            dev_info = p.get_device_info_by_index(i)
            # 检查设备是否是输入设备（麦克风）
            if dev_info['maxInputChannels'] > 0 and hostapis[dev_info['hostApi']]=="MME":
                self.micList.append( f"{hostapis[dev_info['hostApi']]} - {dev_info['name']}")
        self.defautMicIndex=p.get_default_input_device_info()['index']
        # 关闭 PyAudio 实例
        p.terminate()
