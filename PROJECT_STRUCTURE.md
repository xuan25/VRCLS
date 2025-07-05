# VRCLS 项目目录结构说明

## 项目概述

VRCLS (VRChat LinguaSync) 是一个用于在VRChat中使用语音控制模型或作为翻译器输出内容的程序。该项目采用服务器-客户端架构，支持本地语音识别、语音合成、SteamVR覆盖显示等功能。

## 目录结构详解

### 根目录文件

| 文件/目录 | 功能说明 |
|-----------|----------|
| `main.py` | **主程序入口文件** - 包含Flask Web服务器、进程管理、API接口等核心功能 |
| `main.spec` | PyInstaller打包配置文件，用于生成可执行文件 |
| `requirements.txt` | Python依赖包列表 |
| `requirements copy.txt` | 依赖包备份文件 |
| `README.md` | 项目中文说明文档 |
| `README-en.md` | 项目英文说明文档 |
| `LICENSE` | 项目许可证文件 |
| `VRCLS_changeLog.md` | 项目更新日志 |

### 核心源代码目录 (`src/`)

#### `src/core/` - 核心功能模块

| 文件 | 功能说明 |
|------|----------|
| `startup.py` | **启动管理模块** - 程序初始化、配置加载、服务启动 |
| `defaultConfig.py` | **默认配置管理** - 程序默认配置参数定义 |
| `logger.py` | **日志系统** - 多进程日志记录和管理 |
| `serverListener.py` | **服务器监听器** - 处理与VoiceLinkVR服务器的通信 |
| `serverActionProcess.py` | **服务器动作处理** - 处理服务器返回的动作指令 |
| `OSCListener.py` | **OSC监听器** - 监听VRChat OSC消息 |
| `OSCListenerThread.py` | **OSC监听线程** - 麦克风状态监听线程 |
| `steamvrProcess.py` | **SteamVR进程管理** - SteamVR覆盖显示功能 |
| `keypress.py` | **按键处理** - 全局热键监听和处理 |
| `update.py` | **更新管理** - 程序自动更新功能 |
| `recordLocal.py` | **本地录音** - 本地音频录制和处理 |
| `osc_client.py` | **OSC客户端** - 向VRChat发送OSC消息 |

#### `src/handler/` - 处理器模块

| 文件 | 功能说明 |
|------|----------|
| `base_handler.py` | **基础处理器** - 所有处理器的基类 |
| `Avatar.py` | **Avatar处理器** - 处理VRChat角色相关操作 |
| `ChatBox.py` | **聊天框处理器** - 处理聊天框显示 |
| `DefaultCommand.py` | **默认命令处理器** - 处理内置语音命令 |
| `SelfRead.py` | **自读处理器** - 处理文本朗读功能 |
| `tts.py` | **语音合成处理器** - 文本转语音功能 |
| `VRCBitmapLedHandler.py` | **点阵屏处理器** - 处理VRChat点阵屏显示 |
| `Color.py` | **颜色处理** - 颜色相关工具函数 |

#### `src/module/` - 功能模块

| 文件 | 功能说明 |
|------|----------|
| `sherpaOnnx.py` | **语音识别模块** - 基于Sherpa-ONNX的本地语音识别 |
| `steamvr.py` | **SteamVR模块** - SteamVR覆盖显示和交互 |
| `oscserver.py` | **OSC服务器** - OSC消息服务器 |
| `translate.py` | **翻译模块** - 文本翻译功能 |
| `copybox.py` | **剪贴板模块** - 剪贴板操作功能 |
| `ffmpegInit.py` | **FFmpeg初始化** - FFmpeg音频处理初始化 |
| `bitLedColor.py` | **点阵屏颜色** - 点阵屏颜色处理 |

#### `src/core/tinyoscquery/` - OSC查询模块

| 文件 | 功能说明 |
|------|----------|
| `query.py` | OSC查询功能 |
| `queryservice.py` | OSC查询服务 |
| `utility.py` | OSC工具函数 |
| `shared/node.py` | OSC节点定义 |

### Web界面目录 (`webUI/`)

| 文件/目录 | 功能说明 |
|-----------|----------|
| `package.json` | Node.js项目配置和依赖 |
| `vue.config.js` | Vue.js构建配置 |
| `babel.config.js` | Babel转译配置 |
| `jsconfig.json` | JavaScript项目配置 |
| `src/` | Vue.js前端源代码 |
| `public/` | 静态资源文件 |
| `node_modules/` | Node.js依赖包 |

#### `webUI/src/` - 前端源代码

| 文件/目录 | 功能说明 |
|-----------|----------|
| `App.vue` | Vue.js主应用组件 |
| `components/` | Vue组件目录 |
| `views/` | 页面视图组件 |
| `store/` | Vuex状态管理 |
| `i18n/` | 国际化配置 |
| `assets/` | 静态资源 |
| `styles/` | 样式文件 |
| `utils/` | 工具函数 |

### 资源目录

| 目录 | 功能说明 |
|------|----------|
| `ffmpeg/` | **FFmpeg工具** - 音频处理工具 |
| `font/` | **字体文件** - 程序使用的字体 |
| `img/` | **图片资源** - 程序图标和图片 |
| `opusdll/` | **Opus库** - 音频编码库 |
| `sherpa-onnx-models/` | **语音识别模型** - 本地语音识别模型文件 |
| `templates/` | **Web模板** - Flask Web界面模板 |
| `upx/` | **UPX压缩工具** - 可执行文件压缩工具 |

### 测试脚本目录 (`testScripts/`)

| 文件/目录 | 功能说明 |
|-----------|----------|
| `baidupublicapi.py` | 百度API测试 |
| `edgeTTs.py` | Edge TTS测试 |
| `oscclient.py` | OSC客户端测试 |
| `portCheck.py` | 端口检查测试 |
| `simpleflask.py` | Flask服务器测试 |
| `steamvrOutput/` | SteamVR输出测试 |
| `translateTest1.py` | 翻译功能测试 |
| `vad2.py` | 语音活动检测测试 |
| `webviewTest.py` | WebView测试 |

### 文档目录 (`docs/`)

| 文件 | 功能说明 |
|------|----------|
| `index.html` | 文档主页 |
| `README.md` | 文档说明 |
| `CNAME` | 域名配置 |

### 旧代码目录 (`oldcode/`)

| 文件 | 功能说明 |
|------|----------|
| `client.py` | 旧版客户端代码 |
| `selflogger.py` | 旧版日志代码 |

## 核心功能模块说明

### 1. 语音识别系统
- **本地识别**: 使用Sherpa-ONNX模型进行本地语音识别
- **服务器识别**: 支持云端语音识别服务
- **VAD检测**: 语音活动检测，提高识别准确性

### 2. 语音合成系统
- **TTS引擎**: 支持多种TTS引擎（Edge TTS等）
- **虚拟麦克风**: 将合成语音输出到虚拟麦克风
- **多语言支持**: 支持多种语言的语音合成

### 3. VRChat集成
- **OSC通信**: 通过OSC协议与VRChat通信
- **Avatar控制**: 控制VRChat角色参数
- **点阵屏显示**: 在VRChat中显示文本信息

### 4. SteamVR集成
- **覆盖显示**: 在VR中显示识别结果和翻译
- **交互界面**: VR中的用户交互界面

### 5. Web管理界面
- **配置管理**: 通过Web界面管理程序配置
- **实时监控**: 实时显示程序状态和日志
- **多语言支持**: 支持中文、英文、日文界面

## 技术架构

### 后端技术栈
- **Python**: 主要开发语言
- **Flask**: Web框架
- **SocketIO**: 实时通信
- **PyAudio**: 音频处理
- **Sherpa-ONNX**: 语音识别
- **FFmpeg**: 音频转码

### 前端技术栈
- **Vue.js**: 前端框架
- **Element UI**: UI组件库
- **WebSocket**: 实时通信
- **i18n**: 国际化

### 部署方式
- **本地部署**: 支持完全本地化部署
- **服务器部署**: 支持服务器-客户端模式
- **打包部署**: 支持PyInstaller打包为可执行文件

## 配置文件说明

主要配置文件包括：
- `client.json`: 客户端配置
- `server.json`: 服务器配置
- `scripts.json`: 语音命令脚本配置

## 开发环境要求

- Python 3.8+
- Node.js 14+
- FFmpeg
- SteamVR
- VRChat

## 许可证

本项目采用开源许可证，具体请查看LICENSE文件。 