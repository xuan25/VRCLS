import json
import sys
from .defaultConfig import defaultConfig,defaultFilter
from .osc_client import OSCClient
import requests
import time
import pyaudio
import os
import shutil

from ..handler.tts import whisper_voice_mapping,libretranslate_voice_mapping
# import os,sys
# from pydub import AudioSegment
class StartUp:
    def __init__(self,logger,params):
        self.logger=logger
        self.params=params
        self.tragetTranslateLanguage="en"
        self.micList=[]
        self.outPutList=[]
        self.loopbackList=[]
        self.loopbackIndexList=[]
        self.defautMicIndex=0
        self.defautOutPutIndex=0

        if sys.platform == "win32":
            docs_dir = os.path.join(os.environ['USERPROFILE'], 'Documents','VRCLS')
        else:
            # Linux/MacOS try $XDG_CONFIG_HOME first
            xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
            if xdg_config_home:
                docs_dir = os.path.join(xdg_config_home, 'VRCLS')
            else:
                docs_dir = os.path.join(os.path.expanduser('~'), '.config', 'VRCLS')

        self.path_dict={
            'client.json':os.path.join(docs_dir,'client.json'),
            'filter.json':os.path.join(docs_dir,'filter.json'),
            'ttsConfig.json':os.path.join(docs_dir,'ttsConfig.json'),
            'customEmoji.json':os.path.join(docs_dir,'customEmoji.json'),
            'client-back.json':os.path.join(docs_dir,'client-back.json')
        }
        os.makedirs(docs_dir, exist_ok=True)
        for i in ['client.json','filter.json','ttsConfig.json','customEmoji.json']: 
            if os.path.exists(i) and not os.path.exists(self.path_dict[i]):
                shutil.move(i, self.path_dict[i])
                
                
        try:
            with open(self.path_dict["client.json"], 'r',encoding='utf-8') as file:
                self.config:dict = json.load(file)
        except FileNotFoundError:
            with open(self.path_dict["client.json"], 'w', encoding="utf8") as f:
                f.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
                self.config=defaultConfig
        except json.JSONDecodeError as e:
            self.logger.put({'text':"client.json配置文件解析异常,详情："+str(e),"level":"error"})
            self.logger.put({'text':"正在创建备份文件并重新生成配置文件","level":"warning"})
            # 备份损坏的配置文件
            backup_path = self.path_dict["client.json"] + ".backup"
            try:
                shutil.copy2(self.path_dict["client.json"], backup_path)
                self.logger.put({'text':f"已备份损坏的配置文件到: {backup_path}","level":"info"})
            except:
                pass
            # 重新生成默认配置文件
            with open(self.path_dict["client.json"], 'w', encoding="utf8") as f:
                f.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
                self.config=defaultConfig
        
        try:
            with open(self.path_dict['filter.json'], 'r',encoding='utf-8') as file:
                self.filter:list = json.load(file)
        except FileNotFoundError:
            with open(self.path_dict['filter.json'], 'w', encoding="utf8") as f:
                f.write(json.dumps(defaultFilter,ensure_ascii=False, indent=4))
                self.filter=defaultFilter
        except json.JSONDecodeError as e:
            self.logger.put({'text':"filter.json配置文件解析异常,详情："+str(e),"level":"error"})
            self.logger.put({'text':"正在创建备份文件并重新生成配置文件","level":"warning"})
            # 备份损坏的配置文件
            backup_path = self.path_dict['filter.json'] + ".backup"
            try:
                shutil.copy2(self.path_dict['filter.json'], backup_path)
                self.logger.put({'text':f"已备份损坏的配置文件到: {backup_path}","level":"info"})
            except:
                pass
            # 重新生成默认配置文件
            with open(self.path_dict['filter.json'], 'w', encoding="utf8") as f:
                f.write(json.dumps(defaultFilter,ensure_ascii=False, indent=4))
                self.filter=defaultFilter
        
        try:
            with open(self.path_dict['ttsConfig.json'], 'r',encoding='utf-8') as file:
                self.ttsVoice:list = json.load(file)
        except FileNotFoundError:
            with open(self.path_dict['ttsConfig.json'], 'w', encoding="utf8") as f:
                f.write(json.dumps({"libretranslate_voice_mapping":libretranslate_voice_mapping,"whisper_voice_mapping":whisper_voice_mapping},ensure_ascii=False, indent=4))
                self.ttsVoice={"libretranslate_voice_mapping":libretranslate_voice_mapping,"whisper_voice_mapping":whisper_voice_mapping}
        except json.JSONDecodeError as e:
            self.logger.put({'text':"ttsConfig.json配置文件解析异常,详情："+str(e),"level":"error"})
            self.logger.put({'text':"正在创建备份文件并重新生成配置文件","level":"warning"})
            # 备份损坏的配置文件
            backup_path = self.path_dict['ttsConfig.json'] + ".backup"
            try:
                shutil.copy2(self.path_dict['ttsConfig.json'], backup_path)
                self.logger.put({'text':f"已备份损坏的配置文件到: {backup_path}","level":"info"})
            except:
                pass
            # 重新生成默认配置文件
            with open(self.path_dict['ttsConfig.json'], 'w', encoding="utf8") as f:
                f.write(json.dumps({"libretranslate_voice_mapping":libretranslate_voice_mapping,"whisper_voice_mapping":whisper_voice_mapping},ensure_ascii=False, indent=4))
                self.ttsVoice={"libretranslate_voice_mapping":libretranslate_voice_mapping,"whisper_voice_mapping":whisper_voice_mapping}
        
        try:
            with open(self.path_dict['customEmoji.json'], 'r',encoding='utf-8') as file:
                self.customEmoji:list = json.load(file)
        except FileNotFoundError:
            with open(self.path_dict['customEmoji.json'], 'w', encoding="utf8") as f:
                defaultCustomEmoji={"测试惊讶":"・ࡇ・","测试心碎":"💔"}
                f.write(json.dumps(defaultCustomEmoji,ensure_ascii=False, indent=4))
                self.customEmoji=defaultCustomEmoji
        except json.JSONDecodeError as e:
            self.logger.put({'text':"customEmoji.json配置文件解析异常,详情："+str(e),"level":"error"})
            self.logger.put({'text':"正在创建备份文件并重新生成配置文件","level":"warning"})
            # 备份损坏的配置文件
            backup_path = self.path_dict['customEmoji.json'] + ".backup"
            try:
                shutil.copy2(self.path_dict['customEmoji.json'], backup_path)
                self.logger.put({'text':f"已备份损坏的配置文件到: {backup_path}","level":"info"})
            except:
                pass
            # 重新生成默认配置文件
            with open(self.path_dict['customEmoji.json'], 'w', encoding="utf8") as f:
                defaultCustomEmoji={"测试惊讶":"・ࡇ・","测试心碎":"💔"}
                f.write(json.dumps(defaultCustomEmoji,ensure_ascii=False, indent=4))
                self.customEmoji=defaultCustomEmoji
        
    def setOSCClient(self,logger):
        self.oscClient=OSCClient(logger=logger,host=self.config.get("osc-ip"),port=int(self.config.get("osc-port")))
        return self.oscClient.client
    def run(self):
        # self.set_ffmpeg_path()
        self.getMics()
        self.list_loopback_devices()
        self.configCheck()
        os.environ["translators_default_region"]=self.config.get('translateRegion')
        if self.config.get("CopyBox"):self.params["opencopybox"]=True
        # self.initffmpeg()
        if not self.config.get('localizedSpeech') or self.config.get("Separate_Self_Game_Mic") !=0 or self.config.get("TTSToggle") !=0 or self.config.get("translateService") =='developer':
           return self.checkAccount()
        else:
            try:
                response = requests.post(self.config["baseurl"]+"/login",json=self.config["userInfo"],timeout=20)
                if response.status_code==200:
                    res=response.json()
                    return {'Authorization': 'Bearer '+res["access_token"]}
            except Exception:
                pass
        return None
    def configCheck(self):
        try:
            with open(self.path_dict['client.json'], 'r',encoding='utf-8') as file:
                self.config:dict = json.load(file)
                configDiff=list(set(defaultConfig.keys())-set(self.config.keys()))
            if configDiff != []:
                self.logger.put({'text':"配置文件更新,增加条目："+str(configDiff),"level":"info"})
                for newConfig in configDiff:
                    self.config[newConfig]=defaultConfig[newConfig]
                with open(self.path_dict['client.json'], 'w', encoding="utf8") as file:
                    file.write(json.dumps(self.config,ensure_ascii=False, indent=4))
            configDefaultScripts=[script["action"] for script in self.config["defaultScripts"]]
            defaultScriptsDiff=[script for script in defaultConfig["defaultScripts"] if script["action"] not in configDefaultScripts]
            if defaultScriptsDiff != []:
                self.logger.put({'text':"配置文件更新,增加默认指令条目："+str(defaultScriptsDiff),"level":"info"})
                for newConfig in defaultScriptsDiff:
                    self.config["defaultScripts"].append(newConfig)
                with open(self.path_dict['client.json'], 'w', encoding="utf8") as file:
                    file.write(json.dumps(self.config,ensure_ascii=False, indent=4))
        except json.JSONDecodeError as e:
            self.logger.put({'text':"client.json配置文件解析异常,详情："+str(e),"level":"error"})
            self.logger.put({'text':"正在重新生成配置文件","level":"warning"})
            # 重新生成默认配置文件
            with open(self.path_dict['client.json'], 'w', encoding="utf8") as file:
                file.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
                self.config = defaultConfig
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
            sys.exit(0)
    def checkAccount(self):

        accont_wrong=False
        while True:
            time.sleep(0.1)
            if self.config["userInfo"]["username"] == "" or self.config["userInfo"]["password"] == "" or self.config["userInfo"]["username"] is None or self.config["userInfo"]["password"] is None:
                self.logger.put({'text':"userinfo empty , please enter again||无用户信息请重新输入","level":"warning"})
                self.config["userInfo"]["username"] = input("请输入用户名: ")
                self.config["userInfo"]["password"] = input("请输入密码: ")
                continue
            baseurl=self.config["baseurl"]
            response = requests.post(baseurl+"/login",json=self.config["userInfo"])
            self.logger.put({'text':response.text,"level":"debug"})
            if response.status_code==200:
                if accont_wrong:
                    with open('client.json', 'w', encoding="utf8") as f:
                        f.write(json.dumps(self.config,ensure_ascii=False, indent=4))
                break
            if response.status_code == 504:
                self.logger.put({'text':"server Time out||服务器连接超时,5秒后重试,请联系服主","level":"warning"})
                time.sleep(5)
                continue
            if response.status_code == 401: 
                accont_wrong=True
                self.logger.put({'text':"password or account error , please enter again||账户或密码错误,请重新输入","level":"warning"})
                time.sleep(3)
                self.config["userInfo"]["username"] = input("请输入用户名: ")
                self.config["userInfo"]["password"] = input("请输入密码: ")
                continue
            if response.status_code == 403:
                self.logger.put({'text':response.text,"level":"debug"})
                self.logger.put({'text':"password or account error , please enter again||账号已被禁用,请联系管理员","level":"error"})
                return {}
            return {}
            

                
            

        

        res=response.json()
        return {'Authorization': 'Bearer '+res["access_token"]}
    def getMics(self):
        # 创建 PyAudio 实例
        try:
            p = pyaudio.PyAudio()
            host_api_count=p.get_host_api_count()
            
            # 获取设备数量
            device_count = p.get_device_count()
        
            hostapis=[]
            self.micList=['' for _ in range(device_count)]
            self.outPutList=['' for _ in range(device_count)]
            for j in range(host_api_count):
                hostapi=p.get_host_api_info_by_index(j)
                hostapis.append(hostapi["name"])
            for i in range(device_count):
                # 获取每个设备的详细信息
                dev_info = p.get_device_info_by_index(i)
                # 检查设备是否是输入设备（麦克风）
                if dev_info['maxInputChannels'] > 0 and hostapis[dev_info['hostApi']]=="MME":
                    self.micList[i]=f"{hostapis[dev_info['hostApi']]} - {dev_info['name']}"
                if dev_info['maxOutputChannels'] > 0 and hostapis[dev_info['hostApi']]=="MME":
                    self.outPutList[i]= f"{hostapis[dev_info['hostApi']]} - {dev_info['name']}"
            
            # 安全地获取默认设备索引
            try:
                self.defautMicIndex=p.get_default_input_device_info()['index']
            except OSError as e:
                print("\n" + "="*50)
                print("错误：未找到默认麦克风设备，程序将停止运行")
                print("请检查麦克风设备是否正确连接或启用")
                print("")
                print("按任意键退出程序...")
                print("="*50)
                self.logger.put({'text':"未找到默认麦克风设备，程序将停止运行","level":"error"})
                self.logger.put({'text':"请检查麦克风设备是否正确连接或启用","level":"error"})
                try:
                    input()
                except:
                    pass
                sys.exit(1)
                
            try:
                self.defautOutPutIndex=p.get_default_output_device_info()['index']
            except OSError as e:
                print("\n" + "="*50)
                print("错误：未找到默认输出设备，程序将停止运行")
                print("请检查音频输出设备是否正确连接或启用")
                print("")
                print("按任意键退出程序...")
                print("="*50)
                self.logger.put({'text':"未找到默认输出设备，程序将停止运行","level":"error"})
                self.logger.put({'text':"请检查音频输出设备是否正确连接或启用","level":"error"})
                try:
                    input()
                except:
                    pass
                sys.exit(1)
                
            # 关闭 PyAudio 实例
            p.terminate()
            
        except Exception as e:
            print("\n" + "="*50)
            print(f"错误：获取音频设备时发生严重错误: {str(e)}")
            print("程序无法继续运行，请检查音频设备配置")
            print("")
            print("按任意键退出程序...")
            print("="*50)
            self.logger.put({'text':f"获取音频设备时发生严重错误: {str(e)}","level":"error"})
            self.logger.put({'text':"程序无法继续运行，请检查音频设备配置","level":"error"})
            try:
                input()
            except:
                pass
            sys.exit(1)
            
    def list_loopback_devices(self):
        """列出所有可用环路录音设备"""
        try:
            import pyaudiowpatch    
            p1 = pyaudiowpatch.PyAudio()
            try:
                self.loopbackList=[]
                self.loopbackIndexList=[]
                for device in p1.get_loopback_device_info_generator():
                    # # 提取关键信息
                    # info = {
                    #     "index": device["index"],
                    #     "name": device["name"],
                    #     "defaultSampleRate": device["defaultSampleRate"],
                    #     "maxInputChannels": device["maxInputChannels"]
                    # }
                    self.loopbackList.append(device["name"])
                    self.loopbackIndexList.append({"index": device["index"],"name": device["name"]})
                
            finally:
                p1.terminate()
        except ImportError:
            self.logger.put({'text':"pyaudiowpatch模块未安装，环路录音功能将不可用","level":"warning"})
            self.loopbackList = []
            self.loopbackIndexList = []
        except Exception as e:
            self.logger.put({'text':f"获取环路录音设备时发生错误: {str(e)}","level":"error"})
            self.loopbackList = []
            self.loopbackIndexList = []

    # # 设置ffmpeg路径（必须在所有pydub操作之前）
    # def set_ffmpeg_path(self):
    #     # 动态获取项目根目录
    #     if getattr(sys, 'frozen', False):
    #         base_path = sys._MEIPASS  # 打包后的临时资源目录
    #     else:
    #         base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    #     # 构造ffmpeg绝对路径
    #     ffmpeg_path = os.path.join(
    #         base_path, 
    #         "ffmpeg", 
    #         "bin", 
    #         "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    #     )
        
    #     # 验证路径有效性
    #     if not os.path.isfile(ffmpeg_path):
    #         raise FileNotFoundError(f"FFmpeg未找到于：{ffmpeg_path}")
        
    #     # 设置路径（关键！必须同时设置converter和ffprobe）
    #     AudioSegment.converter = ffmpeg_path
    #     AudioSegment.ffprobe = os.path.join(os.path.dirname(ffmpeg_path), "ffprobe.exe")
