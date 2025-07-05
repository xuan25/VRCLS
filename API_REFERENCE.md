# VRCLS API 接口参考文档

## 概述

VRCLS提供了丰富的REST API接口，用于程序配置、状态监控、功能控制等。所有API都通过Flask Web服务器提供，默认运行在本地端口。

## 基础信息

- **基础URL**: `http://localhost:5000/api`
- **内容类型**: `application/json`
- **认证方式**: 无（本地服务）

## API 接口列表

### 1. 配置管理

#### 获取配置
```http
GET /api/getConfig
```

**响应示例**:
```json
{
    "userInfo": {
        "username": "user",
        "password": "pass"
    },
    "baseurl": "https://whisper.boyqiu001.cn:7070",
    "port": 9000,
    "ip": "127.0.0.1",
    "defaultMode": "control"
}
```

#### 保存配置
```http
POST /api/saveConfig
Content-Type: application/json

{
    "userInfo": {
        "username": "newuser",
        "password": "newpass"
    },
    "baseurl": "https://newserver.com:7070"
}
```

#### 保存并重启
```http
POST /api/saveandreboot
Content-Type: application/json

{
    "config": {
        // 配置数据
    }
}
```

### 2. 窗口控制

#### 关闭窗口
```http
GET /api/closewindow
```

#### 最大化窗口
```http
GET /api/maximize
```

#### 最小化窗口
```http
GET /api/minimize
```

#### 恢复窗口
```http
GET /api/windowrestore
```

### 3. 音频控制

#### 切换麦克风音频
```http
GET /api/toggleMicAudio
```

#### 切换桌面音频
```http
GET /api/toggleDesktopAudio
```

#### VAD校准
```http
GET /api/vadCalibrate
```

### 4. 设备信息

#### 获取麦克风列表
```http
GET /api/getMics
```

**响应示例**:
```json
[
    {
        "name": "麦克风 (Realtek High Definition Audio)",
        "index": 0
    },
    {
        "name": "虚拟麦克风",
        "index": 1
    }
]
```

#### 获取输出设备列表
```http
GET /api/getOutputs
```

#### 获取捕获设备列表
```http
GET /api/getcapture
```

### 5. VRChat集成

#### 获取Avatar参数
```http
GET /api/getAvatarParameters
```

**响应示例**:
```json
[
    {
        "name": "TailCloud",
        "type": "float",
        "value": 0.0
    },
    {
        "name": "Voice",
        "type": "bool",
        "value": true
    }
]
```

#### 发送文本并翻译
```http
POST /api/sendTextandTranslate
Content-Type: application/json

{
    "text": "Hello world",
    "sourceLanguage": "en",
    "targetLanguage": "zh"
}
```

### 6. 系统信息

#### 获取版本信息
```http
GET /api/version
```

**响应示例**:
```json
{
    "version": "1.0.0",
    "build": "20231201"
}
```

#### 获取统计信息
```http
GET /api/stats
```

**响应示例**:
```json
{
    "uptime": 3600,
    "memory_usage": 1024000,
    "cpu_usage": 15.5,
    "requests_processed": 1500
}
```

#### 检查更新
```http
GET /api/getUpdate
```

### 7. 系统控制

#### 重启程序
```http
GET /api/reboot
```

#### 升级程序
```http
GET /api/upgrade
```

## WebSocket 接口

### 连接
```javascript
const socket = io('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to VRCLS');
});
```

### 事件监听

#### 日志事件
```javascript
socket.on('log', (data) => {
    console.log('Log:', data.message);
});
```

#### 状态事件
```javascript
socket.on('status', (data) => {
    console.log('Status:', data.status);
});
```

## 错误处理

### 错误响应格式
```json
{
    "error": true,
    "message": "错误描述",
    "code": 400
}
```

### 常见错误码
- `400`: 请求参数错误
- `404`: 接口不存在
- `500`: 服务器内部错误

## 使用示例

### JavaScript 示例
```javascript
// 获取配置
async function getConfig() {
    const response = await fetch('/api/getConfig');
    const config = await response.json();
    return config;
}

// 保存配置
async function saveConfig(config) {
    const response = await fetch('/api/saveConfig', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    });
    return response.json();
}

// 切换麦克风
async function toggleMic() {
    const response = await fetch('/api/toggleMicAudio');
    return response.json();
}
```

### Python 示例
```python
import requests

# 获取配置
def get_config():
    response = requests.get('http://localhost:5000/api/getConfig')
    return response.json()

# 保存配置
def save_config(config):
    response = requests.post('http://localhost:5000/api/saveConfig', 
                           json=config)
    return response.json()

# 切换麦克风
def toggle_mic():
    response = requests.get('http://localhost:5000/api/toggleMicAudio')
    return response.json()
```

## 注意事项

1. **本地服务**: 所有API都是本地服务，不需要网络连接
2. **端口配置**: 默认端口为5000，可在配置中修改
3. **CORS**: 支持跨域请求，但主要用于本地开发
4. **安全性**: 由于是本地服务，没有额外的安全验证
5. **性能**: API响应时间通常在毫秒级别

## 更新日志

- **v1.0.0**: 初始版本，包含基础配置和音频控制API
- **v1.1.0**: 新增VRChat集成API
- **v1.2.0**: 新增WebSocket实时通信
- **v1.3.0**: 新增系统监控和统计API 