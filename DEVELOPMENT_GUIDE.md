# VRCLS 开发指南

## 项目概述

VRCLS (VRChat Language System) 是一个专为VRChat设计的实时语音识别、翻译和语音合成系统。该系统支持多语言实时翻译，本地语音识别，以及TTS语音合成功能。

### 核心功能
- **实时语音识别**: 支持麦克风和桌面音频捕获
- **多语言翻译**: 支持100+语言的实时翻译
- **语音合成(TTS)**: 支持多种语音引擎
- **VRChat集成**: 通过OSC协议与VRChat通信
- **SteamVR支持**: 集成SteamVR功能
- **Web界面**: 现代化的配置界面

## 系统架构

### 整体架构图
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   Flask Server  │    │   Core Modules  │
│   (Vue.js)      │◄──►│   (Python)      │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   OSC Client    │    │   Audio Capture │
                       │   (VRChat)      │    │   (PyAudio)     │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   SteamVR       │    │   TTS Engine    │
                       │   Integration   │    │   (Edge TTS)    │
                       └─────────────────┘    └─────────────────┘
```

### 核心模块架构

#### 1. 启动模块 (`src/core/startup.py`)
**类**: `StartUp`
- **职责**: 程序初始化和配置管理
- **主要方法**:
  - `__init__(logger, params)`: 初始化启动器，加载配置文件
  - `run()`: 执行启动流程
  - `configCheck()`: 验证配置完整性
  - `checkAccount()`: 验证用户账户
  - `getMics()`: 获取音频设备列表
  - `list_loopback_devices()`: 获取回环设备列表

#### 2. 日志系统 (`src/core/logger.py`)
**类**: `MyLogger`
- **职责**: 统一的日志管理和统计
- **主要方法**:
  - `getlogger(name, filepath)`: 创建日志记录器
  - `logger_process(queue, copyqueue, params, socketQueue)`: 日志处理进程

#### 3. OSC通信模块 (`src/core/osc_client.py`)
**类**: `OSCClient`
- **职责**: 与VRChat的OSC通信
- **主要方法**:
  - `send_message(address, data)`: 发送OSC消息
  - `send_avatar_parameter(parameter, value)`: 发送Avatar参数

#### 4. 服务器监听模块 (`src/core/serverListener.py`)
**主要函数**:
- `selfMic_listen(params, logger, micList, defautMicIndex, filter, steamvrQueue, customEmoji, outputList, ttsVoice)`: 麦克风监听
- `gameMic_listen_capture(params, logger, micList, defautMicIndex, filter, steamvrQueue, customEmoji, outputList, ttsVoice)`: 桌面音频捕获
- `gameMic_listen_VoiceMeeter(params, logger, micList, defautMicIndex, filter, steamvrQueue, customEmoji, outputList, ttsVoice)`: VoiceMeeter音频捕获

## 开发环境搭建

### 系统要求
- **操作系统**: Windows 10/11
- **Python**: 3.8+
- **Node.js**: 14+
- **Git**: 最新版本
- **FFmpeg**: 音频处理工具
- **SteamVR**: VR环境支持
- **VRChat**: 目标应用

### 1. 克隆项目
```bash
git clone https://github.com/VoiceLinkVR/VRCLS.git
cd VRCLS
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 3. 安装Node.js依赖
```bash
cd webUI
npm install
```

### 4. 安装额外工具
- **FFmpeg**: 下载并添加到系统PATH
- **SteamVR**: 安装SteamVR
- **VRChat**: 安装VRChat

## 项目结构详解

### 核心源代码结构 (`src/`)
```
src/
├── core/                    # 核心功能模块
│   ├── __init__.py
│   ├── startup.py          # 启动和初始化
│   ├── logger.py           # 日志系统
│   ├── osc_client.py       # OSC客户端
│   ├── OSCListener.py      # OSC监听器
│   ├── OSCListenerThread.py # OSC监听线程
│   ├── serverListener.py   # 服务器监听
│   ├── steamvrProcess.py   # SteamVR处理
│   ├── update.py           # 更新模块
│   ├── defaultConfig.py    # 默认配置
│   ├── keypress.py         # 按键处理
│   ├── recordLocal.py      # 本地录音
│   ├── serverActionProcess.py # 服务器动作处理
│   └── tinyoscquery/       # OSC查询模块
├── handler/                # 处理器模块
│   ├── __init__.py
│   ├── base_handler.py     # 处理器基类
│   ├── Avatar.py           # Avatar控制
│   ├── ChatBox.py          # 聊天框处理
│   ├── Color.py            # 颜色处理
│   ├── DefaultCommand.py   # 默认命令
│   ├── SelfRead.py         # 自读功能
│   ├── tts.py              # TTS处理
│   └── VRCBitmapLedHandler.py # 点阵屏显示
└── module/                 # 功能模块
    ├── __init__.py
    ├── bitLedColor.py      # LED颜色控制
    ├── copybox.py          # 复制框功能
    ├── ffmpegInit.py       # FFmpeg初始化
    ├── oscserver.py        # OSC服务器
    ├── sherpaOnnx.py       # 语音识别
    ├── steamvr.py          # SteamVR功能
    └── translate.py        # 翻译功能
```

### Web界面结构 (`webUI/`)
```
webUI/
├── src/
│   ├── App.vue             # 主应用组件
│   ├── components/         # Vue组件
│   │   ├── config-page.vue # 配置页面
│   │   ├── side-info.vue   # 侧边信息
│   │   └── side-info-four.vue # 四栏信息
│   ├── i18n/              # 国际化
│   │   ├── index.js       # i18n配置
│   │   └── locales/       # 语言文件
│   │       ├── en.js      # 英文
│   │       ├── ja.js      # 日文
│   │       └── zh.js      # 中文
│   ├── store/             # Vuex状态管理
│   ├── styles/            # 样式文件
│   └── utils/             # 工具函数
├── public/                # 静态资源
└── package.json           # 依赖配置
```

## 核心模块详细说明

### 1. 语音识别模块 (`src/module/sherpaOnnx.py`)

#### 主要函数

**`create_recognizer(logger, source)`**
- **功能**: 创建语音识别器
- **参数**: 
  - `logger`: 日志记录器
  - `source`: 语言代码 (zh, en, ja, etc.)
- **返回**: sherpa_onnx.OnlineRecognizer 实例
- **说明**: 根据语言代码加载对应的ONNX模型

**`sherpa_onnx_run_local(sendClient, params, logger, micList, defautMicIndex, filter, steamvrQueue, customEmoji, outputList, ttsVoice)`**
- **功能**: 本地语音识别处理
- **参数**:
  - `sendClient`: OSC客户端
  - `params`: 配置参数
  - `logger`: 日志记录器
  - `micList`: 麦克风设备列表
  - `defautMicIndex`: 默认麦克风索引
  - `filter`: 过滤器配置
  - `steamvrQueue`: SteamVR队列
  - `customEmoji`: 自定义表情
  - `outputList`: 输出设备列表
  - `ttsVoice`: TTS语音配置
- **说明**: 处理桌面音频的本地语音识别

**`sherpa_onnx_run_mic(sendClient, params, logger, micList, defautMicIndex, filter, steamvrQueue, customEmoji, outputList, ttsVoice)`**
- **功能**: 麦克风语音识别处理
- **说明**: 处理麦克风输入的语音识别

**`sherpa_onnx_run(sendClient, params, logger, micList, defautMicIndex, filter, steamvrQueue, customEmoji, outputList, ttsVoice)`**
- **功能**: 服务器语音识别处理
- **说明**: 使用服务器进行语音识别

**`sherpa_once(result, sendClient, params, logger, filter, mode, steamvrQueue, customEmoji, outputList, ttsVoice)`**
- **功能**: 单次语音识别结果处理
- **参数**:
  - `result`: 识别结果
  - `mode`: 处理模式 (mic/cap)
- **说明**: 处理语音识别结果，包括翻译和TTS

### 2. 翻译模块 (`src/module/translate.py`)

#### 主要函数

**`developer_trasnlator(logger, baseurl, sourceLanguage, tragetTranslateLanguage, res, params)`**
- **功能**: 开发者翻译器
- **参数**:
  - `logger`: 日志记录器
  - `baseurl`: 翻译服务器地址
  - `sourceLanguage`: 源语言
  - `tragetTranslateLanguage`: 目标语言
  - `res`: 识别结果
  - `params`: 配置参数
- **返回**: 翻译后的文本
- **说明**: 使用开发者服务器进行翻译

**`openai_translator(logger, sourceLanguage, tragetTranslateLanguage, res, params)`**
- **功能**: OpenAI翻译器
- **参数**: 同上
- **返回**: 翻译后的文本
- **说明**: 使用OpenAI API进行翻译

**`other_trasnlator(logger, translator, sourceLanguage, tragetTranslateLanguage, res)`**
- **功能**: 其他翻译器
- **参数**:
  - `translator`: 翻译器类型
- **说明**: 支持多种翻译引擎

### 3. TTS模块 (`src/handler/tts.py`)

#### 主要类

**`TTSHandler`**
- **职责**: TTS语音合成处理
- **主要方法**:
  - `__init__(logger, params, mode, header, outputList, ttsVoice)`: 初始化TTS处理器
  - `tts_audio(text, language='zh')`: 生成TTS音频
  - `__del__()`: 清理资源

#### 语音映射配置

**`whisper_voice_mapping`**: Whisper语音映射
- 支持100+语言的语音合成
- 格式: `{'语言代码': '语音名称'}`

**`libretranslate_voice_mapping`**: LibreTranslate语音映射
- 支持LibreTranslate的语音合成

### 4. OSC通信模块 (`src/core/osc_client.py`)

#### 主要类

**`OSCClient`**
- **职责**: OSC协议客户端
- **主要方法**:
  - `send_message(address, data)`: 发送OSC消息
  - `send_avatar_parameter(parameter, value)`: 发送Avatar参数
  - `send_chat_message(message)`: 发送聊天消息

### 5. SteamVR模块 (`src/core/steamvrProcess.py`)

#### 主要函数

**`steamvr_process(steamvrQueue, logger)`**
- **功能**: SteamVR处理进程
- **参数**:
  - `steamvrQueue`: SteamVR队列
  - `logger`: 日志记录器
- **说明**: 处理SteamVR相关功能

## 开发流程

### 1. 功能开发流程

#### 添加新功能模块
1. 在 `src/module/` 创建新模块文件
2. 在 `src/handler/` 创建对应的处理器
3. 在 `main.py` 中注册新功能
4. 更新配置文件结构

#### 示例：添加新的语音命令
```python
# src/module/newCommand.py
class NewCommandModule:
    def __init__(self):
        self.name = "newCommand"
    
    def execute(self, text):
        # 实现命令逻辑
        pass

# src/handler/NewCommandHandler.py
from src.handler.base_handler import BaseHandler

class NewCommandHandler(BaseHandler):
    def handle(self, data):
        # 处理命令
        pass
```

### 2. Web界面开发

#### Vue组件结构

**主应用组件 (`webUI/src/App.vue`)**
```vue
<template>
  <configPage/>
</template>

<script>
import configPage from './components/config-page.vue'

export default {
  name: 'App',
  components: {
    configPage
  }
}
</script>
```

**配置页面组件 (`webUI/src/components/config-page.vue`)**
- **功能**: 主要配置界面
- **主要功能**:
  - 用户信息配置
  - 服务器设置
  - 音频设备配置
  - 翻译设置
  - TTS配置

**侧边信息组件 (`webUI/src/components/side-info.vue`)**
- **功能**: 显示系统状态信息
- **显示内容**:
  - 麦克风状态
  - 桌面音频状态
  - VR状态
  - 识别统计

#### 国际化支持 (`webUI/src/i18n/`)

**支持语言**:
- 中文 (`zh.js`)
- 英文 (`en.js`) 
- 日文 (`ja.js`)

**使用示例**:
```javascript
// 在组件中使用
import { useI18n } from 'vue-i18n'

export default {
  setup() {
    const { t } = useI18n()
    return { t }
  }
}
```

#### 添加新页面流程
1. 在 `webUI/src/components/` 创建Vue组件
2. 在 `webUI/src/i18n/locales/` 添加语言文件
3. 在 `webUI/src/store/` 添加状态管理
4. 更新路由配置

#### 示例：添加新的配置页面
```vue
<!-- webUI/src/components/NewConfigPage.vue -->
<template>
  <div class="new-config-page">
    <el-form :model="config" label-width="120px">
      <el-form-item :label="$t('server.address')">
        <el-input v-model="config.baseurl"></el-input>
      </el-form-item>
      <el-form-item :label="$t('server.port')">
        <el-input-number v-model="config.port"></el-input-number>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n'

export default {
  name: 'NewConfigPage',
  setup() {
    const { t } = useI18n()
    return { t }
  },
  data() {
    return {
      config: {}
    }
  },
  methods: {
    async loadConfig() {
      const response = await fetch('/api/getConfig')
      this.config = await response.json()
    },
    async saveConfig() {
      await fetch('/api/saveConfig', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.config)
      })
    }
  }
}
</script>
```

### 3. API开发

#### Flask应用结构 (`main.py`)

**主要路由函数**:

**`@app.route('/api/getConfig', methods=['get'])`**
- **功能**: 获取配置信息
- **返回**: JSON格式的配置数据
- **说明**: 前端获取当前系统配置

**`@app.route('/api/saveConfig', methods=['post'])`**
- **功能**: 保存配置信息
- **参数**: JSON格式的配置数据
- **返回**: 保存结果
- **说明**: 前端保存系统配置

**`@app.route('/api/sendTextandTranslate', methods=['post'])`**
- **功能**: 发送文本并翻译
- **参数**: 
  - `text`: 要翻译的文本
  - `sourceLanguage`: 源语言
  - `targetLanguage`: 目标语言
- **返回**: 翻译结果
- **说明**: 处理文本翻译请求

**`@app.route('/api/getMics', methods=['get'])`**
- **功能**: 获取麦克风设备列表
- **返回**: 音频设备信息
- **说明**: 获取系统可用的音频输入设备

**`@app.route('/api/getOutputs', methods=['get'])`**
- **功能**: 获取音频输出设备列表
- **返回**: 音频输出设备信息
- **说明**: 获取系统可用的音频输出设备

**`@app.route('/api/toggleMicAudio', methods=['get'])`**
- **功能**: 切换麦克风音频状态
- **返回**: 切换结果
- **说明**: 开启/关闭麦克风音频处理

**`@app.route('/api/toggleDesktopAudio', methods=['get'])`**
- **功能**: 切换桌面音频状态
- **返回**: 切换结果
- **说明**: 开启/关闭桌面音频处理

**`@app.route('/api/getMicStatus', methods=['get'])`**
- **功能**: 获取麦克风状态
- **返回**: 麦克风状态信息
- **说明**: 获取当前麦克风处理状态

**`@app.route('/api/stats', methods=['GET'])`**
- **功能**: 获取统计信息
- **返回**: 系统使用统计
- **说明**: 获取识别次数、成功率等统计信息

**`@app.route('/api/reboot', methods=['get'])`**
- **功能**: 重启系统
- **返回**: 重启结果
- **说明**: 重启VRCLS系统

**`@app.route('/api/upgrade', methods=['get'])`**
- **功能**: 系统升级
- **返回**: 升级结果
- **说明**: 检查并执行系统升级

#### WebSocket支持

**Socket.IO集成**:
```python
@socketio.on('connect')
def handle_connect():
    """处理WebSocket连接"""
    emit('status', {'data': 'Connected'})
```

**实时日志推送**:
```python
def ws_log_sender():
    """WebSocket日志发送器"""
    while True:
        try:
            log_data = socketQueue.get()
            socketio.emit('log', log_data)
        except Exception as e:
            logger.error(f"WebSocket发送错误: {e}")
```

#### 添加新API接口流程
1. 在 `main.py` 中添加路由装饰器
2. 实现接口逻辑函数
3. 添加参数验证和错误处理
4. 更新API文档
5. 在前端添加对应的调用

#### 示例：添加设备状态API
```python
@app.route('/api/deviceStatus', methods=['GET'])
def get_device_status():
    """获取设备状态API"""
    try:
        # 获取各种设备状态
        mic_status = params.get("voiceKeyRun", False)
        desktop_audio_status = params.get("gameVoiceKeyRun", False)
        vr_status = steamvrQueue.qsize() > 0
        
        status = {
            'mic_active': mic_status,
            'desktop_audio_active': desktop_audio_status,
            'vr_active': vr_status,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(status)
    except Exception as e:
        logger.error(f"获取设备状态失败: {e}")
        return jsonify({'error': str(e)}), 500
```

#### 错误处理模式
```python
def api_error_handler(func):
    """API错误处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API错误: {e}")
            return jsonify({'error': str(e)}), 500
    return wrapper

@app.route('/api/example', methods=['GET'])
@api_error_handler
def example_api():
    """示例API"""
    # API逻辑
    return jsonify({'success': True})
```

## 调试技巧

### 1. 日志调试

#### 日志系统使用
```python
from src.core.logger import logger

# 不同级别的日志
logger.debug("详细调试信息")  # 开发时使用
logger.info("一般信息")       # 正常运行信息
logger.warning("警告信息")    # 潜在问题
logger.error("错误信息")      # 错误信息
logger.critical("严重错误")   # 严重错误
```

#### 日志文件位置
- **主日志**: `VRCLS.log` (项目根目录)
- **备份日志**: `VRCLS.log.1`, `VRCLS.log.2` 等
- **数据库日志**: `Documents/VRCLS/log_statistics.db`

#### 日志统计功能
```python
# 日志统计关键词
keyweod_list = [
    "返回值过滤-",
    "服务器翻译成功：",
    "麦克风识别结果：",
    "桌面音频识别结果：",
    "TTS文本生成: "
]
```

### 2. 测试脚本

#### 可用的测试脚本 (`testScripts/`)
```bash
# OSC通信测试
python testScripts/oscclient.py

# TTS功能测试
python testScripts/edgeTTs.py

# 音频设备测试
python testScripts/pyaudiotest/t1.py

# 翻译功能测试
python testScripts/testOpenAITranslate.py

# SteamVR测试
python testScripts/steamvrOutput/steamvrDevices.py

# 按键测试
python testScripts/testkeyPressing.py
```

#### 自定义测试脚本
```python
# testScripts/custom_test.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.module.sherpaOnnx import create_recognizer
from src.core.logger import MyLogger

def test_speech_recognition():
    """测试语音识别功能"""
    logger = MyLogger().logger
    
    # 创建识别器
    recognizer = create_recognizer(logger, "zh")
    if recognizer:
        print("语音识别器创建成功")
    else:
        print("语音识别器创建失败")

if __name__ == "__main__":
    test_speech_recognition()
```

### 3. Web界面调试

#### 开发服务器启动
```bash
cd webUI
npm run serve  # 启动开发服务器
# 访问 http://localhost:8080
```

#### Vue开发者工具
- 安装Vue DevTools浏览器扩展
- 在浏览器中调试Vue组件
- 查看组件状态和事件

#### 热重载调试
```javascript
// 在Vue组件中添加调试信息
console.log('组件数据:', this.config)
console.log('API响应:', response)
```

### 4. 进程调试

#### 进程监控
```python
import psutil
import os

def debug_process_info():
    """调试进程信息"""
    current_process = psutil.Process()
    
    print(f"进程ID: {current_process.pid}")
    print(f"进程名称: {current_process.name()}")
    print(f"内存使用: {current_process.memory_info().rss / 1024 / 1024:.2f} MB")
    print(f"CPU使用率: {current_process.cpu_percent()}%")
    print(f"工作目录: {current_process.cwd()}")
    
    # 子进程信息
    children = current_process.children()
    print(f"子进程数量: {len(children)}")
    for child in children:
        print(f"  子进程: {child.pid} - {child.name()}")

# 在main.py中调用
debug_process_info()
```

#### 内存泄漏检测
```python
import gc
import sys

def check_memory_usage():
    """检查内存使用情况"""
    # 强制垃圾回收
    gc.collect()
    
    # 获取内存使用统计
    objects = gc.get_objects()
    print(f"对象数量: {len(objects)}")
    
    # 按类型统计对象
    type_counts = {}
    for obj in objects:
        obj_type = type(obj).__name__
        type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
    
    # 显示前10个最多的对象类型
    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    for obj_type, count in sorted_types[:10]:
        print(f"{obj_type}: {count}")
```

### 5. 网络调试

#### API请求调试
```python
import requests

def debug_api_request(url, data=None):
    """调试API请求"""
    try:
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None
```

#### OSC通信调试
```python
from pythonosc import udp_client

def debug_osc_communication():
    """调试OSC通信"""
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    
    # 发送测试消息
    test_message = "Hello VRChat"
    client.send_message("/chatbox/input", [test_message, True])
    print(f"发送OSC消息: {test_message}")
```

## 配置管理

### 配置文件结构

#### 主配置文件 (`client.json`)
```json
{
    "userInfo": {
        "username": "",
        "password": ""
    },
    "baseurl": "https://whisper.boyqiu001.cn:7070",
    "port": 9000,
    "ip": "127.0.0.1",
    "defaultMode": "control",
    "scripts": [],
    "micName": "default",
    "gameMicName": "default",
    "micVoiceMode": 0,
    "gameVoiceMode": 0,
    "micVoiceHotKey_new": null,
    "gameVoiceHotKey_new": null,
    "tragetTranslateLanguage": "en",
    "translator": "developer",
    "TTSToggle": 0,
    "TTSVoice": "zh-CN-XiaoxiaoNeural",
    "openai_config": {
        "api_key": "",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo"
    }
}
```

#### 过滤器配置 (`filter.json`)
```json
[
    {
        "type": "keyword",
        "pattern": "敏感词",
        "action": "replace",
        "replacement": "***"
    },
    {
        "type": "regex",
        "pattern": "\\b\\w+@\\w+\\.\\w+\\b",
        "action": "remove"
    }
]
```

#### TTS配置 (`ttsConfig.json`)
```json
{
    "libretranslate_voice_mapping": {
        "zh": "zh-CN-XiaoxiaoNeural",
        "en": "en-US-JennyNeural",
        "ja": "ja-JP-NanamiNeural"
    },
    "whisper_voice_mapping": {
        "zh": "zh-CN-XiaoxiaoNeural",
        "en": "en-US-JennyNeural",
        "ja": "ja-JP-NanamiNeural"
    }
}
```

### 配置文件位置

#### 默认位置
- **Windows**: `%USERPROFILE%\Documents\VRCLS\`
- **配置文件**:
  - `client.json` - 主配置
  - `filter.json` - 过滤器配置
  - `ttsConfig.json` - TTS配置
  - `customEmoji.json` - 自定义表情

#### 配置文件迁移
```python
# 自动迁移旧配置文件
docs_dir = os.path.join(os.environ['USERPROFILE'], 'Documents','VRCLS')
for config_file in ['client.json','filter.json','ttsConfig.json','customEmoji.json']:
    if os.path.exists(config_file) and not os.path.exists(os.path.join(docs_dir, config_file)):
        shutil.move(config_file, os.path.join(docs_dir, config_file))
```

### 配置验证

#### 配置完整性检查
```python
def validate_config(config):
    """验证配置完整性"""
    required_fields = {
        'userInfo': dict,
        'baseurl': str,
        'port': int,
        'ip': str,
        'defaultMode': str
    }
    
    for field, field_type in required_fields.items():
        if field not in config:
            raise ValueError(f"缺少必需配置: {field}")
        
        if not isinstance(config[field], field_type):
            raise TypeError(f"配置字段 {field} 类型错误，期望 {field_type}")
    
    # 验证端口范围
    if not (1024 <= config['port'] <= 65535):
        raise ValueError(f"端口号 {config['port']} 超出有效范围 (1024-65535)")
    
    # 验证URL格式
    if not config['baseurl'].startswith(('http://', 'https://')):
        raise ValueError(f"无效的URL格式: {config['baseurl']}")
    
    return True
```

#### 配置备份和恢复
```python
def backup_config(config_path):
    """备份配置文件"""
    import shutil
    from datetime import datetime
    
    backup_path = f"{config_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(config_path, backup_path)
    return backup_path

def restore_config(config_path, backup_path):
    """恢复配置文件"""
    import shutil
    shutil.copy2(backup_path, config_path)
```

### 配置热重载

#### 配置监听器
```python
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, config_path, callback):
        self.config_path = config_path
        self.callback = callback
        self.last_modified = 0
    
    def on_modified(self, event):
        if event.src_path == self.config_path:
            current_time = time.time()
            if current_time - self.last_modified > 1:  # 防抖
                self.last_modified = current_time
                self.callback()

def watch_config_file(config_path, callback):
    """监听配置文件变化"""
    event_handler = ConfigFileHandler(config_path, callback)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(config_path), recursive=False)
    observer.start()
    return observer
```

## 性能优化

### 1. 内存优化

#### 对象生命周期管理
```python
import weakref
import gc

class MemoryOptimizedClass:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
        self._large_data = None
    
    def load_large_data(self, data):
        """加载大量数据"""
        self._large_data = data
    
    def clear_large_data(self):
        """清理大量数据"""
        self._large_data = None
        gc.collect()  # 强制垃圾回收
    
    def __del__(self):
        """析构函数"""
        self.clear_large_data()
```

#### 生成器处理大数据
```python
def process_large_audio_file(file_path, chunk_size=1024*1024):
    """使用生成器处理大音频文件"""
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield process_audio_chunk(chunk)

def process_audio_chunk(chunk):
    """处理音频块"""
    # 音频处理逻辑
    return processed_chunk
```

#### 内存监控
```python
import psutil
import os

def monitor_memory_usage():
    """监控内存使用"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"虚拟内存: {memory_info.vms / 1024 / 1024:.2f} MB")
    
    # 内存使用率警告
    if memory_info.rss > 500 * 1024 * 1024:  # 500MB
        print("警告: 内存使用过高")
        gc.collect()  # 强制垃圾回收
```

### 2. CPU优化

#### 多进程处理
```python
from multiprocessing import Process, Queue, Pool
import multiprocessing as mp

def cpu_intensive_task(data):
    """CPU密集型任务"""
    # 复杂的计算逻辑
    result = complex_calculation(data)
    return result

def parallel_process_data(data_list, num_processes=None):
    """并行处理数据"""
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(cpu_intensive_task, data_list)
    
    return results

# 使用示例
def process_audio_files(audio_files):
    """并行处理音频文件"""
    return parallel_process_data(audio_files, num_processes=4)
```

#### 缓存机制
```python
import functools
import time
from collections import OrderedDict

class LRUCache:
    """LRU缓存实现"""
    def __init__(self, maxsize=128):
        self.maxsize = maxsize
        self.cache = OrderedDict()
    
    def get(self, key):
        """获取缓存值"""
        if key in self.cache:
            # 移动到末尾
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        """放入缓存"""
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.maxsize:
                # 删除最旧的项
                self.cache.popitem(last=False)
        self.cache[key] = value

# 函数缓存装饰器
def timed_cache(ttl_seconds=300):
    """带过期时间的缓存装饰器"""
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        return wrapper
    return decorator

# 使用示例
@timed_cache(ttl_seconds=60)
def expensive_translation(text, source_lang, target_lang):
    """昂贵的翻译操作"""
    # 翻译逻辑
    return translated_text
```

### 3. 网络优化

#### 连接池管理
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OptimizedHTTPClient:
    """优化的HTTP客户端"""
    def __init__(self, pool_connections=10, pool_maxsize=20):
        self.session = requests.Session()
        
        # 配置连接池
        adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=Retry(
                total=3,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def request(self, method, url, **kwargs):
        """发送请求"""
        return self.session.request(method, url, **kwargs)

# 使用示例
http_client = OptimizedHTTPClient()
response = http_client.request('POST', 'https://api.example.com/translate', 
                              json={'text': 'Hello'})
```

#### 请求重试机制
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """指数退避重试机制"""
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                # 指数退避 + 随机抖动
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(delay)
        
        return None
    
    return wrapper

# 使用示例
@retry_with_backoff(max_retries=3)
def api_request(url, data):
    """API请求"""
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
```

### 4. 音频处理优化

#### 音频流处理
```python
import numpy as np
import pyaudio

class OptimizedAudioProcessor:
    """优化的音频处理器"""
    def __init__(self, chunk_size=1024, sample_rate=16000):
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.audio_buffer = np.array([])
    
    def process_audio_stream(self, audio_stream):
        """处理音频流"""
        for chunk in audio_stream:
            # 转换为numpy数组进行批量处理
            audio_data = np.frombuffer(chunk, dtype=np.int16)
            
            # 批量处理音频数据
            processed_data = self.batch_process(audio_data)
            
            yield processed_data
    
    def batch_process(self, audio_data):
        """批量处理音频数据"""
        # 使用numpy进行向量化操作
        normalized_data = audio_data.astype(np.float32) / 32768.0
        
        # 应用滤波器
        filtered_data = self.apply_filter(normalized_data)
        
        return filtered_data
    
    def apply_filter(self, data):
        """应用音频滤波器"""
        # 简单的低通滤波器
        alpha = 0.1
        filtered = np.zeros_like(data)
        filtered[0] = data[0]
        
        for i in range(1, len(data)):
            filtered[i] = alpha * data[i] + (1 - alpha) * filtered[i-1]
        
        return filtered
```

### 5. 数据库优化

#### SQLite优化
```python
import sqlite3
import threading

class OptimizedDatabase:
    """优化的数据库管理器"""
    def __init__(self, db_path):
        self.db_path = db_path
        self._lock = threading.Lock()
    
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # 优化设置
        conn.execute("PRAGMA journal_mode=WAL")  # 写前日志
        conn.execute("PRAGMA synchronous=NORMAL")  # 同步模式
        conn.execute("PRAGMA cache_size=10000")  # 缓存大小
        conn.execute("PRAGMA temp_store=MEMORY")  # 临时表存储在内存
        
        return conn
    
    def execute_with_retry(self, query, params=None):
        """带重试的数据库操作"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self._lock:
                    conn = self.get_connection()
                    cursor = conn.cursor()
                    
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    
                    result = cursor.fetchall()
                    conn.commit()
                    conn.close()
                    return result
                    
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    time.sleep(0.1 * (2 ** attempt))  # 指数退避
                    continue
                raise e

## 错误处理

### 1. 异常处理模式

#### 分层异常处理
```python
import logging
from typing import Optional, Any

class VRCLSError(Exception):
    """VRCLS基础异常类"""
    pass

class AudioError(VRCLSError):
    """音频处理异常"""
    pass

class TranslationError(VRCLSError):
    """翻译服务异常"""
    pass

class OSCError(VRCLSError):
    """OSC通信异常"""
    pass

def safe_function_with_logging(func, logger, fallback_value=None):
    """带日志的安全函数执行器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AudioError as e:
            logger.error(f"音频处理错误: {e}")
            return fallback_value
        except TranslationError as e:
            logger.error(f"翻译服务错误: {e}")
            return fallback_value
        except OSCError as e:
            logger.error(f"OSC通信错误: {e}")
            return fallback_value
        except Exception as e:
            logger.error(f"未知错误: {e}")
            logger.debug(f"错误详情: {traceback.format_exc()}")
            raise
    
    return wrapper

# 使用示例
@safe_function_with_logging
def process_audio(audio_data):
    """处理音频数据"""
    if not audio_data:
        raise AudioError("音频数据为空")
    # 处理逻辑
    return processed_data
```

#### 上下文管理器
```python
from contextlib import contextmanager

@contextmanager
def error_context(operation_name, logger):
    """错误上下文管理器"""
    try:
        yield
    except Exception as e:
        logger.error(f"{operation_name} 操作失败: {e}")
        raise

# 使用示例
def process_with_context():
    with error_context("音频处理", logger):
        # 音频处理逻辑
        process_audio_data()
```

### 2. 错误恢复机制

#### 自动重试机制
```python
import time
import random
from functools import wraps

def retry_on_failure(max_retries=3, base_delay=1, max_delay=60, 
                    exceptions=(Exception,), backoff_factor=2):
    """失败重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries - 1:
                        raise last_exception
                    
                    # 计算延迟时间
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    delay += random.uniform(0, 1)  # 添加随机抖动
                    
                    logger.warning(f"第 {attempt + 1} 次尝试失败: {e}, "
                                 f"{delay:.2f}秒后重试")
                    time.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator

# 使用示例
@retry_on_failure(max_retries=3, exceptions=(TranslationError,))
def translate_text(text, source_lang, target_lang):
    """翻译文本"""
    # 翻译逻辑
    return translated_text
```

#### 熔断器模式
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # 正常状态
    OPEN = "open"          # 熔断状态
    HALF_OPEN = "half_open"  # 半开状态

class CircuitBreaker:
    """熔断器实现"""
    def __init__(self, failure_threshold=5, recovery_timeout=60, 
                 expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
    
    def call(self, func, *args, **kwargs):
        """调用函数"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("熔断器开启，拒绝请求")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except self.expected_exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        """成功回调"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# 使用示例
translation_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=30,
    expected_exception=TranslationError
)

def safe_translate(text, source_lang, target_lang):
    """安全的翻译函数"""
    return translation_breaker.call(translate_text, text, source_lang, target_lang)
```

### 3. 错误监控和报告

#### 错误统计
```python
import sqlite3
from datetime import datetime

class ErrorTracker:
    """错误跟踪器"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                stack_trace TEXT,
                context TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_error(self, error_type, error_message, stack_trace=None, context=None):
        """记录错误"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO error_logs (timestamp, error_type, error_message, stack_trace, context)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            error_type,
            error_message,
            stack_trace,
            context
        ))
        
        conn.commit()
        conn.close()
    
    def get_error_stats(self, days=7):
        """获取错误统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT error_type, COUNT(*) as count
            FROM error_logs
            WHERE timestamp > datetime('now', '-{} days')
            GROUP BY error_type
            ORDER BY count DESC
        '''.format(days))
        
        results = cursor.fetchall()
        conn.close()
        
        return dict(results)

# 使用示例
error_tracker = ErrorTracker('error_logs.db')

def monitored_function():
    try:
        # 函数逻辑
        pass
    except Exception as e:
        error_tracker.log_error(
            error_type=type(e).__name__,
            error_message=str(e),
            stack_trace=traceback.format_exc(),
            context="function_name"
        )
        raise
```

### 4. 优雅降级

#### 功能降级策略
```python
class FeatureDegradation:
    """功能降级管理器"""
    def __init__(self):
        self.degradation_levels = {
            'full': 0,
            'basic': 1,
            'minimal': 2,
            'offline': 3
        }
        self.current_level = 'full'
    
    def set_degradation_level(self, level):
        """设置降级级别"""
        if level in self.degradation_levels:
            self.current_level = level
            logger.info(f"功能降级到: {level}")
    
    def should_use_feature(self, feature_name):
        """判断是否应该使用某个功能"""
        feature_levels = {
            'translation': ['full', 'basic'],
            'tts': ['full', 'basic'],
            'advanced_audio': ['full'],
            'steamvr': ['full', 'basic']
        }
        
        return self.current_level in feature_levels.get(feature_name, ['full'])

# 使用示例
degradation_manager = FeatureDegradation()

def translate_with_degradation(text, source_lang, target_lang):
    """带降级的翻译"""
    if not degradation_manager.should_use_feature('translation'):
        logger.warning("翻译功能已降级，跳过翻译")
        return text
    
    try:
        return translate_text(text, source_lang, target_lang)
    except TranslationError:
        degradation_manager.set_degradation_level('basic')
        logger.warning("翻译服务不可用，降级到基础模式")
        return text  # 返回原文
```

## 测试

### 1. 单元测试
```python
import unittest

class TestNewModule(unittest.TestCase):
    def setUp(self):
        self.module = NewModule()
    
    def test_function(self):
        result = self.module.function()
        self.assertEqual(result, expected_value)
```

### 2. 集成测试
```python
def test_full_workflow():
    # 测试完整工作流程
    config = load_test_config()
    app = create_test_app(config)
    result = app.process_audio("测试音频")
    assert result.success
```

### 3. 性能测试
```python
import time

def performance_test():
    start_time = time.time()
    # 执行操作
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 1.0  # 确保性能要求
```

## 部署

### 1. 开发环境
```bash
python main.py
```

### 2. 生产环境
```bash
# 使用PyInstaller打包
pyinstaller main.spec

# 或使用Docker
docker build -t vrcls .
docker run -p 5000:5000 vrcls
```

### 3. 更新部署
```bash
# 自动更新
python -c "from src.core.update import main_update; main_update()"
```

## 贡献指南

### 1. 代码规范
- 使用PEP 8代码风格
- 添加适当的注释
- 编写单元测试
- 更新文档

### 2. 提交规范
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具的变动
```

### 3. 分支管理
- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支

## 常见问题

### 1. 音频设备问题
- 检查设备权限
- 确认设备驱动正常
- 验证音频格式支持

### 2. VRChat连接问题
- 确认OSC端口配置
- 检查防火墙设置
- 验证VRChat版本兼容性

### 3. SteamVR问题
- 确认SteamVR运行状态
- 检查OpenVR路径配置
- 验证VR设备连接

## 资源链接

- [VRChat OSC文档](https://docs.vrchat.com/docs/osc-overview)
- [SteamVR开发文档](https://github.com/ValveSoftware/openvr)
- [Sherpa-ONNX文档](https://github.com/k2-fsa/sherpa-onnx)
- [Flask文档](https://flask.palletsprojects.com/)
- [Vue.js文档](https://vuejs.org/) 