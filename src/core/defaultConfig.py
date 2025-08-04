defaultConfig={
    "userInfo": {
        "username": "testuser",
        "password": "abc123!"
    },
    "baseurl": "https://whisper.boyqiu001.cn:7070",
    "api-ip":"127.0.0.1",
    "api-port":8980,
    "osc-port": 9000,
    "osc-ip": "127.0.0.1",
    "defaultMode": "translation",
    "activateText": "",
    "stopText": "",
    "micName":"default",
    "voiceMode":0,
    "webBrowserPath":"",
    "dynamicThreshold":False,
    "customThreshold":0.01,
    "voiceHotKey_new":"<alt>+1",
    "sourceLanguage": "zh",
    "targetTranslationLanguage": "en",
    "targetTranslationLanguage2": "none",
    "targetTranslationLanguage3": "none",
    "translationServer":"libre",# "whisper","libre"
    "VRCBitmapLed_row":8,
    "VRCBitmapLed_col":16,
    "VRCBitmapLed_COLOR":True,
    "Separate_Self_Game_Mic":0,
    "gameMicName":"default",
    "gameVoiceMode":0,
    "gameCustomThreshold":0.01,
    "gameVoiceHotKey_new":"<alt>+2",
    "textInSteamVR":False,
    "SteamVRHad":0,#右手单手，左手单手 双手
    "SteamVRSize":0.15,
    "localizedSpeech":False,
    "localizedCapture":False,
    "CopyBox":False,
    "TTSToggle":0,#0 关闭 1 翻译模式麦克风译文输出 2 文字发送模式麦克风原文 3 翻译模式麦克风+桌面音频译文输出
    "TTSOutputName":'default',
    "translateService":'developer',
    "translateRegion":'CN',
    "oscShutdown":False,
    "VRCChatboxformat_new":"{translatedText}\n{translatedText2}\n{translatedText3}\n{text}",
    "VRCChatboxformat_text":"{text}",
    "realtimeOutputDelay":-1.0,
    "micPressingKey":'v',
    "capPressingKey":'b',
    "enableOscServer":False,
    "oscServerIp":'127.0.0.1',
    "oscServerPort":9003,
    "chatboxOscMixTemplate":r'{clientdata}{serverdata}',
    "darkmode":False,
    "enableRecognitionOverlay":False,
    "overlayWidth":400,
    "overlayHeight":200,
    "overlayX":100,
    "overlayY":100,
    "filteremoji":"false",
    "translateServicecap":'developer',
    "openai_config": {
        "api_key": "",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "model": "glm-4-flash"
    },
    "defaultScripts": [
        {
            "action": "sendText",
            "text": [
                "切换到文字发送模式",
                "到文字发送模式",
	            "文字发送"
            ]
        },
        {
            "action": "changToTrans",
            "text": [
                "切换到翻译模式",
                "到翻译模式"
            ]
        },
        {
            "action": "changToControl",
            "text": [
                "切换到控制模式",
                "到控制模式"
            ]
        },
        {
            "action": "changTobitMapLed",
            "text": [
                "切换到屏幕"
            ]
        },
        {
            "action": "changToEnglish",
            "text": [
                "切换到英语翻译"
            ]
        },
        {
            "action": "changTojapanese",
            "text": [
                "切换到日语翻译"
            ]
        },
        {
            "action": "changToRussian",
            "text": [
                "切换到俄语翻译"
            ]
        },
        {
            "action": "changToKorean",
            "text": [
                "切换到韩语翻译"
            ]
        }
    ],
    "scripts": [
        {
            "action": "toggle Mic",
            "text": [
                "切换麦克风",
                "切換麥克風"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/input/Voice",
                    "vrcValue": 0,
                    "vrcValueType": "bool",
                    "sleeptime": 0.1
                },
                {
                    "vrcPath": "/input/Voice",
                    "vrcValueType": "bool",
                    "vrcValue": 1
                },
                {
                    "vrcPath": "/input/Voice",
                    "vrcValueType": "bool",
                    "vrcValue": 0
                }
            ]
        },
        {
            "action": "blackCloth",
            "text": [
                "黑色衣服"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/Change_material",
	                "vrcValueType": "float",
                    "vrcValue": 0
                }
            ]
        },
        {
            "action": "whiteCloth",
            "text": [
                "白色衣服"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/Change_material",
	                "vrcValueType": "float",
                    "vrcValue": 0.5
                }
            ]
        },
        {
            "action": "openBaseballBat",
            "text": [
                "打开棒球棒"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/IsBaseballBat",
	                "vrcValueType": "bool",
                    "vrcValue": 1
                }
            ]
        },
        {
            "action": "closeBaseballBat",
            "text": [
                "关闭棒球棒"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/IsBaseballBat",
	                "vrcValueType": "bool",
                    "vrcValue": 0
                }
            ]
        },
        {
            "action": "openTailCloud",
            "text": [
                "打开尾巴云朵"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/TailCloud",
	                "vrcValueType": "bool",
                    "vrcValue": 1
                }
            ]
        },
        {
            "action": "closeTailCloud",
            "text": [
                "关闭尾巴云朵"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/TailCloud",
	                "vrcValueType": "bool",
                    "vrcValue": 0
                }
            ]
        }
    ]
}

defaultFilter=[
    "谢谢大家",
    "謝謝大家",
    "感谢观看"
]
