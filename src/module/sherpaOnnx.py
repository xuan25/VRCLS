import pyaudiowpatch
import numpy as np
import sherpa_onnx
from multiprocessing import Process
import baidu_translate as fanyi
import os,sys,time
import pyttsx3
def create_recognizer(logger,source):

        # 2. 动态路径注入（核心防护）
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))  # 适配 src/core 的层级
    if source in ["zh","en","zt"] :
        #中英
        onnx_bin = os.path.join(base_dir,"sherpa-onnx-models", "sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20")
    elif source in ["zh","zt","ja","jp",'vi','th',"id",'ar',"ru","en"] :
        #中日
        onnx_bin = os.path.join(base_dir,"sherpa-onnx-models", "sherpa-onnx-streaming-zipformer-ar_en_id_ja_ru_th_vi_zh-2025-02-10")
    else:return None
    # 新增路径检查
    if not os.path.exists(onnx_bin):
        logger.put({"text": f"模型路径不存在：{onnx_bin},\n请去qq群1011986554下载并安装VRCLS本地识别模型包", "level": "error"})
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
def sherpa_onnx_run_local(sendClient,config,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji):
    if config.get("gameMicName")== "" or config.get("gameMicName") is None or config.get("gameMicName")== "default":
        logger.put({"text":"使用系统默认桌面音频","level":"info"})
        micIndex=None
    else:
        device_index=False
        for i in micList:
            if config.get("gameMicName")==i.get("name"):
                device_index=True
                micIndex=i.get('index')
                logger.put({"text":f"当前桌面音频：{config.get("gameMicName")}","level":"info"})
                break
        
        
        if not device_index:
            logger.put({"text":"无法找到指定桌面音频，使用系统默认桌面音频","level":"info"})
            micIndex=None
    pa = pyaudiowpatch.PyAudio()
    # 获取输入设备信息  
    device_info = pa.get_default_wasapi_loopback() if micIndex is None else pa.get_device_info_by_index(micIndex)
   

    recognizer = create_recognizer(logger,config.get("targetTranslationLanguage"))
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
    try:
        while params["running"]:
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
                
            if is_endpoint:
                if result:
                    p = Process(target=sherpa_once,daemon=True, args=(result,sendClient,config,params,logger,filter,"cap",steamvrQueue,customEmoji))
                    p.start()
                recognizer.reset(stream)
                
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        logger.put({"text":"sound process exited complete||本地桌面音频进程退出完毕","level":"info"})
        params["gameStopped"] = True
def sherpa_onnx_run(sendClient,config,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji):
    if config.get("micName")== "" or config.get("micName") is None or config.get("micName")== "default":
        logger.put({"text":"使用系统默认麦克风","level":"info"})
        micIndex=defautMicIndex
    else:
        try:
            micIndex=micList.index(config.get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定游戏麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前游戏麦克风：{micList[micIndex]}","level":"info"})
    pa = pyaudiowpatch.PyAudio()
    
    # 获取输入设备信息
    input_device = pa.get_device_info_by_index(micIndex)
    

    recognizer = create_recognizer(logger,config.get("sourceLanguage"))
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
    try:
        while params["running"]:
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
                
            if is_endpoint or len(result)>30:
                if result:
                    p = Process(target=sherpa_once,daemon=True, args=(result,sendClient,config,params,logger,filter,"mic",steamvrQueue,customEmoji))
                    p.start()
                recognizer.reset(stream)

                
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        logger.put({"text":"sound process exited complete||麦克风音频进程退出完毕","level":"info"})
        params["micStopped"]=True
def sherpa_onnx_run_mic(sendClient,config,params,logger,micList:list,defautMicIndex,filter,steamvrQueue,customEmoji):
    if config.get("gameMicName")== "" or config.get("gameMicName") is None :
        logger.put({"text":"请指定游戏麦克风，游戏麦克风线程退出","level":"warning"})
        return
    else:
        try:
            micIndex=micList.index(config.get("micName"))
        except ValueError:
            logger.put({"text":"无法找到指定游戏麦克风，使用系统默认麦克风","level":"info"})
            micIndex=defautMicIndex
    logger.put({"text":f"当前游戏麦克风：{micList[micIndex]}","level":"info"})
    pa = pyaudiowpatch.PyAudio()
    
    # 获取输入设备信息
    input_device = pa.get_device_info_by_index(micIndex)
    

    recognizer = create_recognizer(logger,config.get("targetTranslationLanguage"))
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
    try:
        while params["running"]:
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
                
            if is_endpoint or len(result)>30:
                if result:
                    p = Process(target=sherpa_once,daemon=True, args=(result,sendClient,config,params,logger,filter,"cap",steamvrQueue,customEmoji))
                    p.start()
                recognizer.reset(stream)

                
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        logger.put({"text":"sound process exited complete||游戏音频进程退出完毕","level":"info"})
        params["gameStopped"] = True
def sherpa_once(result,sendClient,config,params,logger,filter,mode,steamvrQueue,customEmoji:dict):
    from ..handler.DefaultCommand import DefaultCommand
    from ..handler.ChatBox import ChatboxHandler
    from ..handler.Avatar import AvatarHandler
    from ..handler.VRCBitmapLedHandler import VRCBitmapLedHandler
    from ..handler.SelfRead import SelfReadHandler
    from hanziconv import HanziConv

    st=time.time()
    tragetTranslateLanguage=params["tragetTranslateLanguage"]
    sourceLanguage=params["sourceLanguage"]
    avatar=AvatarHandler(logger=logger,osc_client=sendClient,config=config)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,config=config)
    chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,config=config)
    bitMapLed=VRCBitmapLedHandler(logger=logger,osc_client=sendClient,config=config,params=params)
    selfRead=SelfReadHandler(logger=logger,osc_client=sendClient,steamvrQueue=steamvrQueue,config=config)
    try:
        if mode=="cap":
            lan=whisper_to_baidu[sourceLanguage] if whisper_to_baidu[sourceLanguage] else fanyi.Lang.ZH
        else:
            lan=libretranslate_to_baidu[tragetTranslateLanguage] if libretranslate_to_baidu[tragetTranslateLanguage] else fanyi.Lang.EN
        res={}
        res['text']=result
        if params["runmode"] == "translation":
            res['translatedText']=fanyi.translate_text(
                result,
                to=lan)
        if sourceLanguage== "zh":res["text"]=HanziConv.toSimplified(res["text"])
        elif sourceLanguage=="zt":res["text"]=HanziConv.toTraditional(res["text"])
        et=time.time()
        logger.put({"text":f"用时：{round(et-st,2)}s 识别结果: " + res["text"],"level":"info"})
        if defaultCommand.handle(res["text"],params=params):return
        if mode=="cap":selfRead.handle(res,"桌面音频",params["steamReady"])
        else:
            if params["runmode"] == "text" or params["runmode"] == "translation": 
                for key in list(customEmoji.keys()):res['text']=res['text'].replace(key,customEmoji[key])
                if config.get("textInSteamVR"):selfRead.handle(res,"麦克风",params["steamReady"])
                if params["runmode"] == "translation" : 
                    for key in list(customEmoji.keys()):res['translatedText']=res['translatedText'].replace(key,customEmoji[key])
                chatbox.handle(res,runMode=params["runmode"])
            if params["runmode"] == "control":avatar.handle(res)
            if params["runmode"] == "bitMapLed":bitMapLed.handle(res,params=params)

    except Exception as e:
        logger.put({"text":"sherpa_once未知异常"+str(e),"level":"error"})
        return
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
