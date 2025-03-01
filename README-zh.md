# VRCLS
(简体中文|[english](README.md))

VRCLS 全称 VRChat LinguaSync， 是一个用于在VRCHAT中使用语音来控制模型或作为翻译器输出内容的程序

## 程序特性

- 低负载。使用服务器客户端模式，配合VoiceLinkVR server一起使用。
- 对客户端设备无性能要求
- 客户端无需过多配置，只需要账号密码与模型控制功能配置
- 客户端集成http api
- 客户端与服务端都支持本地部署

## 启动方法

### 构筑包

如没有python环境可以访问通过[百度网盘链接](https://pan.baidu.com/s/11orFzXGRVjv3vMuadvq0LQ?pwd=78xa)下载打包后的程序

解压压缩包后双击VRCLS.exe 


---
### 本地python运行

克隆或下载仓库源码后运行以下命令
```bash
pip install -r requirements.txt 
python main.py
```

## 使用方法

B站使用教程：[[VRCLS]VRCHAT语音控制与翻译软件基础使用教程（翻译相关）](https://www.bilibili.com/video/BV14hNae6Ext/?share_source=copy_web&vd_source=ffd2f3e2acd107095c2208f7864e9582)

### 登录

#### 1. 使用默认开发者提供的服务器（测试用）

    程序默认使用开发者提供的服务器网址
    如需使用，请加QQ群: 1011986554 ，问题答案为VoiceLinkVR

    根据控制台提示，输入账号和密码，或在网页中输入账户密码

    等待噪声检查后可以开始使用


####  2. 使用本地搭建的服务器或他人的服务器

    如果要使用其他人的服务器请与VoiceLinkVR-server服务器管理员联系

    先运行程序后修改配置文件client.json中的baseurl，请看下方 配置文件参数详解

    根据提示，输入账号和密码

    等待噪声检查后可以开始使用

---

### 配置

请根据开启时的WEBUI在浏览器配置参数


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
    //"whisper","libre" 使用libreTranslte翻译或者whisper翻译
    "translationServer":"libre",
    //浏览器exe绝对路径，
    "webBrowserPath":"",
    //动态音量阈值
    "dynamicThreshold":false,
    //自定义阈值
    "customThreshold":0.02,
    //麦克风开关快捷键
    "voiceHotKey":"alt+q",
    //VRCBitmapLed行数
    "VRCBitmapLed_row":8,
    //VRCBitmapLed列数
    "VRCBitmapLed_col":16,
    //VRCBitmapLed是否开启颜色
    "VRCBitmapLed_COLOR":true,
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
                    //现在推荐使用UI
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
