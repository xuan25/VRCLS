def developer_trasnlator(logger,baseurl,sourceLanguage,tragetTranslateLanguage,res,params):
    import requests
    url2=baseurl+'/func/webtranslate'
    data2 = {"text":res['text'],"targetLanguage": tragetTranslateLanguage, "sourceLanguage": "zh" if sourceLanguage=="zt" else  sourceLanguage}
    logger.put({"text":f"url:{url2},tragetTranslateLanguage:{tragetTranslateLanguage}","level":"debug"})
    response=requests.post(url2, json=data2, headers=params['headers'])

    # 检查响应状态码
    if response.status_code != 200:
        if response.status_code == 430:
            res=response.json()
            logger.put({"text":f"请求过于频繁,可以尝试更换其他翻译引擎,触发规则{res.get('limit')}","level":"warning"})
        else:    
            logger.put({"text":f"数据接收异常:{response.text}","level":"warning"})
        return ''
    # 解析JSON响应
    res = response.json()
    return res["translatedText"]

def openai_translator(logger, sourceLanguage, tragetTranslateLanguage, res, params):
    """OpenAI翻译器"""
    import time
    import traceback
    from openai import OpenAI
    
    try:
        # 获取OpenAI配置
        openai_config = params["config"].get("openai_config", {})
        api_key = openai_config.get("api_key", "")
        base_url = openai_config.get("base_url", "https://api.openai.com/v1")
        model = openai_config.get("model", "gpt-3.5-turbo")
        
        if not api_key:
            logger.put({"text": "OpenAI API密钥未配置", "level": "error"})
            return ''
        
        # 创建OpenAI客户端
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # 语言代码映射
        language_mapping = {
            'en': 'English',
            'ja': 'Japanese', 
            'ko': 'Korean',
            'ru': 'Russian',
            'zh': 'Chinese',
            'zt': 'Traditional Chinese',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'cs': 'Czech',
            'sk': 'Slovak',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'el': 'Greek',
            'he': 'Hebrew',
            'fa': 'Persian',
            'bn': 'Bengali',
            'ur': 'Urdu',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'mr': 'Marathi',
            'ne': 'Nepali',
            'si': 'Sinhala',
            'my': 'Burmese',
            'km': 'Khmer',
            'lo': 'Lao',
            'ka': 'Georgian',
            'am': 'Amharic',
            'sw': 'Swahili',
            'zu': 'Zulu',
            'af': 'Afrikaans',
            'is': 'Icelandic',
            'mt': 'Maltese',
            'cy': 'Welsh',
            'ga': 'Irish',
            'sq': 'Albanian',
            'mk': 'Macedonian',
            'sr': 'Serbian',
            'bs': 'Bosnian',
            'me': 'Montenegrin',
            'uk': 'Ukrainian',
            'be': 'Belarusian',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'uz': 'Uzbek',
            'tg': 'Tajik',
            'mn': 'Mongolian',
            'hy': 'Armenian',
            'az': 'Azerbaijani',
            'ka': 'Georgian',
            'ab': 'Abkhaz',
            'os': 'Ossetian',
            'cv': 'Chuvash',
            'tt': 'Tatar',
            'ba': 'Bashkir',
            'sah': 'Yakut',
            'ce': 'Chechen',
            'av': 'Avar',
            'lez': 'Lezgin',
            'tab': 'Tabasaran',
            'dar': 'Dargwa',
            'lbe': 'Lak',
            'agx': 'Aghul',
            'rut': 'Rutul',
            'tsx': 'Tsakhur',
            'udi': 'Udi',
            'inh': 'Ingush',
            'kbd': 'Kabardian',
            'ady': 'Adyghe',
            'krc': 'Karachay-Balkar',
            'nog': 'Nogai',
            'kum': 'Kumyk',
            'crh': 'Crimean Tatar',
            'gag': 'Gagauz',
            'tr': 'Turkish',
            'az': 'Azerbaijani',
            'tk': 'Turkmen',
            'ug': 'Uyghur',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'uz': 'Uzbek',
            'tg': 'Tajik',
            'mn': 'Mongolian',
            'bo': 'Tibetan',
            'dz': 'Dzongkha',
            'ne': 'Nepali',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'pa': 'Punjabi',
            'gu': 'Gujarati',
            'or': 'Odia',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'si': 'Sinhala',
            'my': 'Burmese',
            'th': 'Thai',
            'lo': 'Lao',
            'km': 'Khmer',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Tagalog',
            'ceb': 'Cebuano',
            'jv': 'Javanese',
            'su': 'Sundanese',
            'mad': 'Madurese',
            'min': 'Minangkabau',
            'ace': 'Acehnese',
            'ban': 'Balinese',
            'bug': 'Buginese',
            'mak': 'Makassarese',
            'gor': 'Gorontalo',
            'kha': 'Khasi',
            'mni': 'Manipuri',
            'as': 'Assamese',
            'brx': 'Bodo',
            'doi': 'Dogri',
            'ks': 'Kashmiri',
            'sa': 'Sanskrit',
            'mr': 'Marathi',
            'ur': 'Urdu',
            'fa': 'Persian',
            'ps': 'Pashto',
            'bal': 'Balochi',
            'ku': 'Kurdish',
            'ar': 'Arabic',
            'he': 'Hebrew',
            'am': 'Amharic',
            'ti': 'Tigrinya',
            'so': 'Somali',
            'sw': 'Swahili',
            'zu': 'Zulu',
            'xh': 'Xhosa',
            'af': 'Afrikaans',
            'st': 'Southern Sotho',
            'tn': 'Tswana',
            'ts': 'Tsonga',
            've': 'Venda',
            'ss': 'Swati',
            'nr': 'Southern Ndebele',
            'nd': 'Northern Ndebele',
            'yo': 'Yoruba',
            'ig': 'Igbo',
            'ha': 'Hausa',
            'ff': 'Fula',
            'wo': 'Wolof',
            'sn': 'Shona',
            'rw': 'Kinyarwanda',
            'lg': 'Ganda',
            'ak': 'Akan',
            'tw': 'Twi',
            'ee': 'Ewe',
            'fon': 'Fon',
            'dyu': 'Dyula',
            'bam': 'Bambara',
            'man': 'Mandinka',
            'kpe': 'Kpelle',
            'vai': 'Vai',
            'mende': 'Mende',
            'tem': 'Temne',
            'lim': 'Limbu',
            'new': 'Newari',
            'tcy': 'Tulu',
            'sat': 'Santali',
            'brh': 'Brahui',
            'sd': 'Sindhi',
            'ks': 'Kashmiri',
            'ur': 'Urdu',
            'pa': 'Punjabi',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'as': 'Assamese',
            'or': 'Odia',
            'te': 'Telugu',
            'ta': 'Tamil',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'ne': 'Nepali',
            'si': 'Sinhala',
            'my': 'Burmese',
            'th': 'Thai',
            'lo': 'Lao',
            'km': 'Khmer',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Tagalog',
            'ceb': 'Cebuano',
            'jv': 'Javanese',
            'su': 'Sundanese',
            'mad': 'Madurese',
            'min': 'Minangkabau',
            'ace': 'Acehnese',
            'ban': 'Balinese',
            'bug': 'Buginese',
            'mak': 'Makassarese',
            'gor': 'Gorontalo',
            'kha': 'Khasi',
            'mni': 'Manipuri',
            'brx': 'Bodo',
            'doi': 'Dogri',
            'sa': 'Sanskrit',
            'ps': 'Pashto',
            'bal': 'Balochi',
            'ku': 'Kurdish',
            'ti': 'Tigrinya',
            'so': 'Somali',
            'st': 'Southern Sotho',
            'tn': 'Tswana',
            'ts': 'Tsonga',
            've': 'Venda',
            'ss': 'Swati',
            'nr': 'Southern Ndebele',
            'nd': 'Northern Ndebele',
            'ff': 'Fula',
            'wo': 'Wolof',
            'sn': 'Shona',
            'rw': 'Kinyarwanda',
            'lg': 'Ganda',
            'ak': 'Akan',
            'tw': 'Twi',
            'ee': 'Ewe',
            'fon': 'Fon',
            'dyu': 'Dyula',
            'bam': 'Bambara',
            'man': 'Mandinka',
            'kpe': 'Kpelle',
            'vai': 'Vai',
            'mende': 'Mende',
            'tem': 'Temne',
            'lim': 'Limbu',
            'new': 'Newari',
            'tcy': 'Tulu',
            'sat': 'Santali',
            'brh': 'Brahui',
            'sd': 'Sindhi'
        }
        
        # 获取源语言和目标语言名称
        source_lang_name = language_mapping.get(sourceLanguage, sourceLanguage)
        target_lang_name = language_mapping.get(tragetTranslateLanguage, tragetTranslateLanguage)
        
        # 构建翻译提示
        system_prompt = f"""你是一个专业的翻译助手。请将以下文本从{source_lang_name}翻译成{target_lang_name}。

翻译要求：
1. 保持原文的意思和语气
2. 确保翻译准确、自然、流畅
3. 如果是语音识别错误，请尝试修正并翻译
4. 只返回翻译结果，不要添加任何解释或额外内容

请翻译以下文本："""

        logger.put({"text":f"OpenAI翻译开始，源语言：{source_lang_name}，目标语言：{target_lang_name}","level":"debug"})
        
        st = time.time()
        
        # 调用OpenAI API
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": res["text"]}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        et = time.time()
        
        # 获取翻译结果
        translated_text = completion.choices[0].message.content.strip()
        
        logger.put({"text":f"OpenAI翻译完成，用时：{round(et-st,2)}s","level":"debug"})
        
        return translated_text
        
    except Exception as e:
        logger.put({"text":f"OpenAI翻译异常：{str(e)}","level":"error"})
        logger.put({"text":f"OpenAI翻译异常详情：{traceback.format_exc()}","level":"debug"})
        return ''

def other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage,res):
    import translators,html,traceback
    try:
        logger.put({"text":f"restext:{res['text']}","level":"debug"})
        return html.unescape(translators.translate_text(res["text"],translator=translator,from_language=sourceLanguage,to_language=tragetTranslateLanguage))
    except Exception as e:
        if all(i in str(e) for i in["from_language[","] and to_language[","] should not be same"]):
            logger.put({"text":f"翻译语言检测同语言：{e}","level":"debug"})
            return res["text"]
        else:
            logger.put({"text":f"翻译异常,请尝试更换翻译引擎：{e};","level":"error"})
            logger.put({"text":f"翻译异常：{traceback.format_exc()}","level":"debug"})
            return ''