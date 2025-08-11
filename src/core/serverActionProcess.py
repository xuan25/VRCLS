def once(audioQueue,sendClient,params,logger,filter,mode,steamvrQueue,customEmoji:dict,outputList,ttsVoice):
    import requests
    import time
    import translators
    import html
    import traceback
    from ..handler.DefaultCommand import DefaultCommand
    from ..handler.ChatBox import ChatboxHandler
    from ..handler.Avatar import AvatarHandler
    from ..handler.VRCBitmapLedHandler import VRCBitmapLedHandler
    from ..handler.SelfRead import SelfReadHandler
    from ..handler.tts import TTSHandler
    from hanziconv import HanziConv
    from ..module.translate import other_trasnlator
    from ..module.translate import openai_translator
    
    # 初始化处理器
    avatar=AvatarHandler(logger=logger,osc_client=sendClient,params=params)
    defaultCommand=DefaultCommand(logger=logger,osc_client=sendClient,params=params)
    if mode=="mic":chatbox=ChatboxHandler(logger=logger,osc_client=sendClient,params=params)
    bitMapLed=VRCBitmapLedHandler(logger=logger,osc_client=sendClient,params=params)
    selfRead=SelfReadHandler(logger=logger,osc_client=sendClient,steamvrQueue=steamvrQueue,params=params)
    tts=TTSHandler(logger=logger,params=params,mode=mode,header=params['headers'],outputList=outputList,ttsVoice=ttsVoice)
    baseurl=params["config"].get('baseurl')
    
    # 初始化OpenAI客户端（只初始化一次）
    openai_client = None
    if params["config"].get('translateService') == "openai" or params["config"].get('translateServicecap') == "openai":
        try:
            from openai import OpenAI
            openai_config = params["config"].get("openai_config", {})
            api_key = openai_config.get("api_key", "")
            base_url = openai_config.get("base_url", "https://open.bigmodel.cn/api/paas/v4/")
            
            if api_key:
                openai_client = OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
                logger.put({"text": f"OpenAI客户端初始化成功，API地址: {base_url}", "level": "info"})
            else:
                logger.put({"text": "OpenAI API密钥未配置", "level": "warning"})
        except Exception as e:
            logger.put({"text": f"OpenAI客户端初始化失败: {str(e)}", "level": "error"})
    
    # 多语言翻译函数
    def translate_multiple_languages(text, source_lang, target_langs, translator_type, openai_client=None):
        """一次性翻译到多个目标语言"""
        results = {}
        
        if translator_type == "openai" and openai_client:
            try:
                # 构建多语言翻译提示
                target_lang_names = []
                for lang in target_langs:
                    if lang != "none":
                        # 语言代码映射（简化版，可以根据需要扩展）
                        lang_names = {
                            'en': 'English', 'ja': 'Japanese', 'ko': 'Korean', 'ru': 'Russian',
                            'zh': 'Chinese', 'zt': 'Traditional Chinese', 'es': 'Spanish',
                            'fr': 'French', 'de': 'German', 'it': 'Italian', 'pt': 'Portuguese'
                        }
                        target_lang_names.append(lang_names.get(lang, lang))
                
                if not target_lang_names:
                    return results
                
                # 构建翻译提示
                system_prompt = f"""你是一个专业的翻译助手。请将以下文本翻译成多种语言。

翻译要求：
1. 保持原文的意思和语气
2. 确保翻译准确、自然、流畅
3. 如果是语音识别错误，请尝试修正并翻译
4. 严格按照JSON格式返回结果

请将以下文本翻译成：{', '.join(target_lang_names)}

返回格式：
{{
    "translations": {{
        "en": "英语翻译",
        "ja": "日语翻译",
        "ko": "韩语翻译"
    }}
}}

原文："""

                # 调用OpenAI API
                model = params["config"].get("openai_config", {}).get("model", "glm-4-flash")
                completion = openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                
                # 解析翻译结果
                response_text = completion.choices[0].message.content.strip()
                try:
                    import json
                    # 尝试解析JSON响应
                    if response_text.startswith('{') and response_text.endswith('}'):
                        parsed = json.loads(response_text)
                        if 'translations' in parsed:
                            for lang in target_langs:
                                if lang != "none" and lang in parsed['translations']:
                                    results[lang] = parsed['translations'][lang]
                    else:
                        # 如果不是JSON格式，按行分割处理
                        lines = response_text.split('\n')
                        for i, lang in enumerate(target_langs):
                            if lang != "none" and i < len(lines):
                                results[lang] = lines[i].strip()
                except:
                    # 如果解析失败，使用简单分割
                    lines = response_text.split('\n')
                    for i, lang in enumerate(target_langs):
                        if lang != "none" and i < len(lines):
                            results[lang] = lines[i].strip()
                            
            except Exception as e:
                logger.put({"text": f"OpenAI多语言翻译异常：{str(e)}", "level": "error"})
                # 降级到单语言翻译
                for lang in target_langs:
                    if lang != "none":
                        try:
                            results[lang] = openai_translator(logger, source_lang, lang, {"text": text}, params)
                        except:
                            results[lang] = ""
        else:
            # 使用其他翻译引擎
            for lang in target_langs:
                if lang != "none":
                    try:
                        results[lang] = html.unescape(translators.translate_text(
                            text, translator=translator_type, 
                            from_language=source_lang, to_language=lang
                        ))
                    except Exception as e:
                        logger.put({"text": f"翻译到{lang}失败：{str(e)}", "level": "error"})
                        results[lang] = ""
        
        return results
    

    while params["running"]:
        try:
            tragetTranslateLanguage2=params["config"].get("targetTranslationLanguage2")
            tragetTranslateLanguage3=params["config"].get("targetTranslationLanguage3")
            tragetTranslateLanguage=params["tragetTranslateLanguage"]
            sourceLanguage=params["sourceLanguage"]
            translator=params["config"].get('translateService') if mode=="mic" else params["config"].get('translateServicecap')
            audio=audioQueue.get()

            st=time.time()
            
            changed_rate=16000
            raw_pcm_data = audio.get_raw_data(convert_rate=changed_rate)
            sample_width = audio.sample_width
            
            data_size = len(raw_pcm_data)
            duration = data_size / (changed_rate * 1 * sample_width)
            logger.put({"text":f"{'麦克风' if mode=='mic' else '桌面'}音频输出完毕, opus音频长度：{round(duration,2)} s","level":"info"})

            opus_bytes=pcm_to_packaged_opus_stream_opuslib(raw_pcm_data,1,sample_width,changed_rate)
            files = {'file': ('filename', opus_bytes , 'audio/opus')}
            # else:
            #     wav_bytes =audio.get_wav_data()
            #     # 解析 WAV 头部信息
            #     with BytesIO(wav_bytes) as wav_file:
            #         # 读取前 44 字节的 WAV 头部
            #         header = wav_file.read(44)
                    
            #         # 提取关键参数（偏移量参考标准 WAV 格式）
            #         channels = struct.unpack('<H', header[22:24])[0]  # 声道数
            #         sample_rate = struct.unpack('<I', header[24:28])[0]  # 采样率
            #         data_size = struct.unpack('<I', header[40:44])[0]  # 音频数据总字节数

            #     # 计算时长（单位：秒）
            #     duration = data_size / (sample_rate * channels * 2)  # 2 表示 16-bit（2字节）采样
            #     logger.put({"text":f"{"麦克风" if mode=="mic" else "桌面"}音频输出完毕, wav音频长度：{round(duration,2)} s","level":"info"})
            #     files = {'file': ('filename', wav_bytes , 'audio/wav')}
            if params["runmode"] == "control" or params["runmode"] == "text" or params["runmode"] == "bitMapLed":
                url=baseurl+"/whisper/multitranscription"
            elif params["runmode"] == "translation":
                if mode =="cap":
                    tmp=sourceLanguage
                    sourceLanguage=tragetTranslateLanguage
                    tragetTranslateLanguage=tmp
                if params["config"]["translationServer"] == "libre":
                    url=baseurl+"/func/multitranslateToOtherLanguage" if translator=="developer" else baseurl+"/whisper/multitranscription"
                elif params["config"]["translationServer"] == "vllm":
                    url=baseurl+"/func/vllmTest"
                else:
                    url=baseurl+"/func/doubleTransciption"
            else: 
                logger.put({"text":"运行模式异常,运行默认控制模式","level":"debug"})
                params["runmode"] = "control"
                url = baseurl+"/whisper/multitranscription"
            logger.put({"text":f"url:{url},tragetTranslateLanguage:{tragetTranslateLanguage}","level":"debug"})
            
            
            data = {'targetLanguage': tragetTranslateLanguage,
                    'targetLanguage2': tragetTranslateLanguage2,
                    'targetLanguage3': tragetTranslateLanguage3,
                    'sourceLanguage': "zh" if sourceLanguage=="zt" else  sourceLanguage,
                    'emojiOutput': params["config"].get("filteremoji","true")
                    }
            response = requests.post(url, files=files, data=data, headers=params['headers'])
            # 检查响应状态码
            if response.status_code != 200:
                if response.status_code == 430:
                    res=response.json()
                    logger.put({"text":f"{'桌面音频'if mode=='cap'else'麦克风'}请求过于频繁,触发规则{res.get('limit')}","level":"warning"})
                else:    
                    logger.put({"text":f"{'桌面音频'if mode=='cap'else'麦克风'}服务器数据接收异常:{response.text}","level":"warning"})
                continue
            # 解析JSON响应
            res = response.json()
            logger.put({"text":f"返回数据信息：{res}","level":"debug"})
            if res["text"] =="":
                logger.put({"text":"返回值过滤-服务端规则","level":"info"})
                continue
            if res["text"] in filter:
                logger.put({"text":"返回值过滤-自定义规则","level":"info"})
                continue
            
            if sourceLanguage== "zh":res["text"]=HanziConv.toSimplified(res["text"])
            elif sourceLanguage=="zt":res["text"]=HanziConv.toTraditional(res["text"])
            et0=time.time()
            if params["runmode"] == "translation" and translator!="developer":
                res['translatedText2']=''
                res['translatedText3']=''
                try:
                    logger.put({"text":f"restext:{res['text']}","level":"debug"})

                    # 收集需要翻译的目标语言
                    target_langs = []
                    if tragetTranslateLanguage != "none":
                        target_langs.append(tragetTranslateLanguage)
                    if mode == "mic":
                        if tragetTranslateLanguage2 != "none":
                            target_langs.append(tragetTranslateLanguage2)
                        if tragetTranslateLanguage3 != "none":
                            target_langs.append(tragetTranslateLanguage3)
                    
                    if translator == "openai" and openai_client and target_langs:
                        # 使用批量翻译优化
                        translations = translate_multiple_languages(
                            res["text"], sourceLanguage, target_langs, translator, openai_client
                        )
                        
                        # 分配翻译结果
                        if tragetTranslateLanguage != "none":
                            res['translatedText'] = translations.get(tragetTranslateLanguage, "")
                        if tragetTranslateLanguage2 != "none":
                            res['translatedText2'] = translations.get(tragetTranslateLanguage2, "")
                        if tragetTranslateLanguage3 != "none":
                            res['translatedText3'] = translations.get(tragetTranslateLanguage3, "")
                    else:
                        # 使用传统单语言翻译
                        if tragetTranslateLanguage != "none":
                            if translator == "openai":
                                res['translatedText'] = openai_translator(logger, sourceLanguage, tragetTranslateLanguage, res, params)
                            else:
                                res['translatedText']=html.unescape(translators.translate_text(res["text"],translator=translator,from_language=sourceLanguage,to_language=tragetTranslateLanguage))
                        
                        # 第二语言
                        if tragetTranslateLanguage2 != "none":
                            if translator == "openai":
                                res['translatedText2'] = openai_translator(logger, sourceLanguage, tragetTranslateLanguage2, res, params)
                            else:
                                res['translatedText2']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage2,res)
                        # 第三语言
                        if tragetTranslateLanguage3 != "none":
                            if translator == "openai":
                                res['translatedText3'] = openai_translator(logger, sourceLanguage, tragetTranslateLanguage3, res, params)
                            else:
                                res['translatedText3']=other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage3,res)
                    
                except Exception as e:
                    if all(i in str(e) for i in["from_language[","] and to_language[","] should not be same"]):
                        logger.put({"text":f"翻译语言检测同语言：{e}","level":"debug"})
                        res['translatedText']=res["text"]
                    else:
                        logger.put({"text":f"翻译异常,请尝试更换翻译引擎：{e};","level":"error"})
                        logger.put({"text":f"翻译异常：{traceback.format_exc()}","level":"debug"})
                        res['translatedText']=''
                        
            et=time.time()
            if translator!="developer":
                logger.put({"text":f"识别用时：{round(et0-st,2)}s，翻译用时：{round(et-et0,2)}s 识别结果: " + res["text"],"level":"info"})
            else:
                logger.put({"text":f"服务器识别+翻译用时：{round(et-st,2)}s 识别结果: " + res["text"],"level":"info"})
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
                        tts.tts_audio(res['translatedText'],language=tragetTranslateLanguage)
                    if params["config"].get("TTSToggle")==1 and mode == 'mic' and params["runmode"] == "translation" :
                        tts.tts_audio(res['translatedText'],language=tragetTranslateLanguage)
                    if params["config"].get("TTSToggle")==2 and mode == 'mic'and params["runmode"] == "text" :
                        tts.tts_audio(res['text'],language=sourceLanguage)
                if params["runmode"] == "control":avatar.handle(res)
                if params["runmode"] == "bitMapLed":bitMapLed.handle(res,params=params)
            et=time.time()

            logger.put({"text":f"服务器识别总用时：{round(et-st,2)}s, 音频长度：{duration} s","level":"debug"})

        except requests.JSONDecodeError:
            logger.put({"text":"json解析异常,code:"+str(response.status_code)+" info:"+response.text,"level":"warning"})
            continue
        except Exception as e:
            logger.put({"text":"once未知异常"+str(e),"level":"error"})
            continue

import opuslib,io,struct
def pcm_to_packaged_opus_stream_opuslib(
    pcm_bytes,
    channels: int,
    sample_width:int,
    sample_rate:int,
    frame_duration_ms: int = 20,
    opus_application: int = opuslib.APPLICATION_AUDIO
) -> bytes:
    """
    将 speech_recognition.AudioData 对象中的 PCM 数据编码为
    带长度前缀的 Opus 包的单一字节流，使用 opuslib。

    每个 Opus 包前会有一个4字节的大端序无符号整数表示该包的长度。

    参数:
        audio_data (speech_recognition.AudioData): 包含 PCM 数据的 AudioData 对象。
        channels (int): 音频的通道数 (1 表示单声道, 2 表示立体声)。
                        AudioData 对象不包含此信息，必须由调用者提供。
        frame_duration_ms (int): Opus 编码器的帧时长，单位毫秒 (例如 20, 40, 60)。
                                 有效值: 2.5, 5, 10, 20, 40, 60。
        opus_application (int): Opus 应用类型 (例如 opuslib.APPLICATION_AUDIO,
                                opuslib.APPLICATION_VOIP,
                                opuslib.APPLICATION_RESTRICTED_LOWDELAY)。

    返回:
        bytes: 包含多个[长度+Opus包]序列的单一字节流。
               如果编码失败或无数据，可能返回空字节串。
    """

    # --- 参数校验 ---
    if not pcm_bytes:
        print("警告: AudioData 不包含原始 PCM 数据。")
        return b''
    if channels not in [1, 2]:
        raise ValueError("通道数必须是 1 (单声道) 或 2 (立体声)。")
    if sample_width != 2:
        # Opus C API (以及 opuslib) 期望的是 16-bit PCM。
        # speech_recognition.AudioData 通常是 sample_width=2。
        raise ValueError(f"Opuslib 需要 16-bit PCM 数据 (sample_width=2)，但 AudioData 的 sample_width 是 {sample_width}。")
    if sample_rate not in [8000, 12000, 16000, 24000, 48000]:
        raise ValueError(f"不支持的采样率: {sample_rate} Hz。Opus 支持 8, 12, 16, 24, 48 kHz。")
    if frame_duration_ms not in [2.5, 5, 10, 20, 40, 60]:
        raise ValueError(f"不支持的帧时长: {frame_duration_ms} ms。")
    valid_applications = [
        opuslib.APPLICATION_VOIP,
        opuslib.APPLICATION_AUDIO,
        opuslib.APPLICATION_RESTRICTED_LOWDELAY
    ]
    if opus_application not in valid_applications:
        raise ValueError(f"不支持的 Opus 应用类型: {opus_application}")

    # --- 初始化 Opus 编码器 ---
    try:
        encoder = opuslib.Encoder(sample_rate, channels, opus_application)
    except opuslib.OpusError as e:
        raise RuntimeError(f"创建 opuslib.Encoder 失败: {e}")
    except Exception as e: # 捕获其他可能的初始化错误
        raise RuntimeError(f"创建 opuslib.Encoder 时发生未知错误: {e}")

    # --- 计算帧参数 ---
    # Opus 编码器期望的每帧每通道的样本数
    samples_per_channel_per_frame = int(sample_rate * frame_duration_ms / 1000)
    # Opus 编码器期望的每帧 PCM 数据的总字节数
    # (每样本字节数 sample_width 已经确认是 2)
    pcm_bytes_per_opus_frame = samples_per_channel_per_frame * channels * sample_width

    # --- 编码过程 ---
    packaged_opus_stream = io.BytesIO()
    offset = 0
    while offset < len(pcm_bytes):
        # 获取当前帧的 PCM 数据
        frame_pcm_segment = pcm_bytes[offset : offset + pcm_bytes_per_opus_frame]

        # 如果是最后一帧且数据不足，需要用静音数据填充到完整帧大小
        if len(frame_pcm_segment) < pcm_bytes_per_opus_frame:
            # 确保不是因为已经处理完所有数据而 frame_pcm_segment 为空
            if not frame_pcm_segment and offset >= len(pcm_bytes):
                break # 所有数据已处理完毕
            
            padding_needed = pcm_bytes_per_opus_frame - len(frame_pcm_segment)
            frame_pcm_segment += b'\x00' * padding_needed # 使用静音填充
        
        # 如果在填充后仍然为空（不太可能发生，除非原始数据为空或计算错误），则跳过
        if not frame_pcm_segment:
            break

        try:
            # 使用 opuslib 进行编码
            # encoder.encode() 的第二个参数是 samples_per_frame (即 samples_per_channel_per_frame)
            encoded_opus_packet = encoder.encode(frame_pcm_segment, samples_per_channel_per_frame)

            # 将 Opus 包的长度（4字节，大端序无符号整数）和包数据写入流
            packaged_opus_stream.write(struct.pack('>I', len(encoded_opus_packet)))
            packaged_opus_stream.write(encoded_opus_packet)

        except opuslib.OpusError as e:
            # 发生编码错误，可以选择记录并跳过此帧，或直接抛出异常
            print(f"警告: Opus 编码错误 (跳过帧): {e}. PCM 段长度: {len(frame_pcm_segment)}")
            # 若要更健壮，可以考虑如何处理这种情况，例如是否停止整个过程
        except Exception as e:
            print(f"警告: Opus 编码时发生未知错误 (跳过帧): {e}")

        offset += pcm_bytes_per_opus_frame
        # 如果最后一帧被填充，并且我们已经处理了所有原始数据，就结束
        if len(frame_pcm_segment) == pcm_bytes_per_opus_frame and offset >= len(pcm_bytes) and \
           pcm_bytes[offset-pcm_bytes_per_opus_frame:] == frame_pcm_segment[:len(pcm_bytes)- (offset-pcm_bytes_per_opus_frame)]:
             pass # 刚好处理完
        elif offset >= len(pcm_bytes) and len(frame_pcm_segment) < pcm_bytes_per_opus_frame: # 处理了最后一小段
            break


    return packaged_opus_stream.getvalue()