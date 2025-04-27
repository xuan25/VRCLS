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
            logger.put({"text":f"请求过于频繁,可以尝试更换其他翻译引擎,触发规则{res.get("limit")}","level":"warning"})
        else:    
            logger.put({"text":f"数据接收异常:{response.text}","level":"warning"})
        return ''
    # 解析JSON响应
    res = response.json()
    return res["translatedText"]

def other_trasnlator(logger,translator,sourceLanguage,tragetTranslateLanguage,res):
    import translators,html,traceback
    try:
        logger.put({"text":f"restext:{res["text"]}","level":"debug"})
        return html.unescape(translators.translate_text(res["text"],translator=translator,from_language=sourceLanguage,to_language=tragetTranslateLanguage))
    except Exception as e:
        if all(i in str(e) for i in["from_language[","] and to_language[","] should not be same"]):
            logger.put({"text":f"翻译语言检测同语言：{e}","level":"debug"})
            return res["text"]
        else:
            logger.put({"text":f"翻译异常,请尝试更换翻译引擎：{e};","level":"error"})
            logger.put({"text":f"翻译异常：{traceback.format_exc()}","level":"debug"})
            return ''