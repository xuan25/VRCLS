# VRCLS
([简体中文](README.md)|english)

VRCLS, also known as VRChat LinguaSync, is a program used in VRCHAT to control models or output content as a translator using speech

## Program Features

-Low load. Use server client mode in conjunction with VoiceLinkVR server.
-Support the use of streaming local recognition models
-Support the use of speech synthesis output
-Support monitoring local desktop audio
-Support Steam VR overlay display
-Support dot matrix display of in-game models
-No performance requirements for client devices
-The client does not require excessive configuration, only the account password and model control function configuration are needed
-Client integrated HTTP API
-Both the client and server support local deployment

## Startup method

### Build Package
If there is no Python environment available, you can access it through [download link](https://github.com/VoiceLinkVR/VRCLS/releases )Download the packaged program

After decompressing the compressed file, double-click VRCLS.exe

---
### Local Python Run

After cloning or downloading the repository source code, run the following command
```bash
pip install -r requirements.txt 
python main.py
```

## Usage method

Bilibili Usage Tutorial: [[VRCLS] VRCHAT Voice Control and Translation Software Basic Usage Tutorial (Translation Related)](https://www.bilibili.com/video/BV14hNae6Ext/?share_source=copy_web&vd_source=ffd2f3e2acd107095c2208f7864e9582)

### Login

#### 1.  Use the default developer provided server (for testing purposes)

The program defaults to using the server URL provided by the developer
The default free account limit on the server is 800 requests per day and 4 requests per minute
If you need to increase your account limit and lift the request limit, please donate for Support Server Operation and Maintenance
donate link: https://afdian.com/a/boyqiu001


####  2.  Use a locally built server or someone else's server

    If you want to use someone else's server, please contact the VoiceLinkVR server administrator

    Run the program first and then modify the baseURL in the client. json configuration file. Please refer to the detailed explanation of the configuration file parameters below

    Follow the prompts and enter your account and password

    Wait for noise inspection before starting to use




---

###Default command (default in chinese ,modifiable)
```
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
```
###Detailed explanation of configuration file parameters

```json
{
    //Account information
    "userInfo": {
    "username": "",
    "password": ""
    },
    //Default is developer server. For local servers, please fill in the server apiURL example: http://192.168.2.10:8980/api
    "baseurl": " https://whisper.boyqiu001.cn:7070 ",
    //VRC OSC receiving port number
    "port": 9000,
    //vrc osc ip
    "ip": "127.0.0.1",
    //Start default running mode, control mode is set to "control", translation mode is set to "traction"
    "defaultMode": "control",
    //The trigger text for exiting the voice assistant
    "exitText":  "Close the voice assistant",
    //Activate the hot word, and only check the trigger word after saying it
    "activateText": "",
    //End the hot word, only after the start and end words are spoken will the trigger word in between be checked
    "stopText": "",
    //User's voice language
    "sourceLanguage": "zh",
    //Default translation output language
    "targetTranslationLanguage": "en",
    //Whisper "and" libre "can be translated using libreTranslte or Whisper
    "translationServer":"libre",
    //Official voice trigger script, checks for new additions every time it is updated, and can modify trigger words in the text
    "defaultScripts": [
    {
        "action": "changToTrans",
        "text": [
        "Switch to translation mode",
        "To Translation Mode"
        ]
    },
    ...
    {
        "action": "changToKorean",
        "text": [
        "Switch to Korean translation"
        ]
    }
    ],
    //User defined voice trigger script
    "scripts": [
    //Example of Control Model Parameters
    {
    //The action name displayed in the log
        "action": "openTailCloud",
        //Script trigger words, multiple can be configured
        "text": [
            "Open the tail cloud"
        ],
        //Multiple operations can be configured, with an interval of half a second between each operation
        "vrcActions": [
        {
            //Please check the OSC path https://docs.vrchat.com/docs/osc-overview The following content
            //Please note that in VRC, the Chinese path is Unicode
            //For example, if the model parameter is "clothing", its OSC path is "/avatar/parameters/\ u8863 \ \ u670d"
            //Transcoding website: https://www.gseen.com/online_tools/code_change/unicode_ascii
            "vrcPath": "/avatar/parameters/TailCloud",
            //OSC sets parameter values
            "vrcValue": 1,
            //OSC parameter format "float", "boolean", "int"
            "vrcValueType": "float",
            //Duration of Status
            "sleeptime": 0.1
        }
        ]
    },
    //As an input, control the mute switch example
    {
        "action": "toggle Mic",
        "text": [
            "Switch microphone",
            "Switch microphone"
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
    }
}

```
