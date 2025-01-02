# VRCLS

VRCLS 全称 VRChat LinguaSync， 是一个用于在VRCHAT中使用语音来控制模型或作为翻译器输出内容的程序

## 启动方法

### 构筑包
如没有python环境可以访问通过[下载链接](https://github.com/VoiceLinkVR/VRCLS/releases)下载打包后的程序

解压压缩包后双击VRCLS.exe 

---
### 本地python运行

克隆或下载仓库源码后运行以下命令
```bash
pip install -r requirements.txt 
python client.py
```

## 使用方法

### 登录

#### 1. 使用默认开发者提供的服务器（测试用）

    程序默认使用开发者提供的服务器网址
    如需使用，请加QQ群: 1011986554 ，问题答案为VoiceLinkVR

    根据提示，输入账号和密码

    等待噪声检查后可以开始使用


####  2. 使用本地搭建的服务器或他人的服务器

    如果要使用其他人的服务器请与VoiceLinkVR-server服务器管理员联系并获取账号密码

    先运行程序后修改配置文件client.json中的baseurl，请看下方 配置文件参数详解

    根据提示，输入账号和密码

    等待噪声检查后可以开始使用




---

### 默认指令

### 配置文件参数详解

```json
{
    //账户信息
    "userInfo": {
        "username": "",
        "password": ""
    },
    //默认为开发者服务器，本地服务器请填写服务器apiURL 例： http://192.168.2.10:8980/api
    "baseurl": "https://whisper.boyqiu001.cn:7070",
    //vrc osc 接收端口号
    "port": 9000,
    //vrc osc ip
    "ip": "127.0.0.1",
    //启动默认运行模式  控制模式为"control" 翻译模式为"trasnlation"
    "defaultMode": "control",
    //退出语音助手的触发文本
    "exitText": "关闭语音助手",
    //启动热词，设置后只有说了这个词之后才会检查触发词
    "activateText": "",
    //结束热词，设置后只有说了开始词和结束词之后才会检查中间的触发词
    "stopText": "",
    //使用者语音语言
    "sourceLanguage": "zh",
    //默认翻译输出的语言
    "targetTranslationLanguage": "en",
    //官方语音触发脚本,每次更新会检查新增，可以修改text中的触发词
    "defaultScripts": [
        {
            "action": "changToTrans",
            "text": [
                "切换到翻译模式",
                "到翻译模式"
            ]
        },
       ...
        {
            "action": "changToKorean",
            "text": [
                "切换到韩语翻译"
            ]
        }
    ],
    //用户自定义语音触发脚本
    "scripts": [
        //控制模型参数示例
        {
            //日志显示的动作名称
            "action": "openTailCloud",
            //脚本触发词，可配置多个
            "text": [
                "打开尾巴云朵"
            ],
            //执行的操作，可配置多个，每个操作间隔半秒
            "vrcActions": [
                {
                    //osc路径 请查看 https://docs.vrchat.com/docs/osc-overview 下的内容
                    //请注意在vrc中，中文路径为Unicode
                    // 如：模型参数为 “衣服” 其osc路径为 "/avatar/parameters/\\u8863\\u670d”
                    //转码网站：https://www.gseen.com/online_tools/code_change/unicode_ascii
                    "vrcPath": "/avatar/parameters/TailCloud",
                    //osc 设置参数值
                    "vrcValue": 1,
                    //osc 参数格式 "float","bool","int"
                    "vrcValueType": "float",
                    //状态持续时间
                    "sleeptime": 0.1
                }
            ]
        },
        //作为input,控制静音开关示例
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
        }
}

```
