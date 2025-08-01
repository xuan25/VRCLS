# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

VRCLS (VRChat LinguaSync) 是一个用于VRChat的语音控制和翻译系统，采用服务器-客户端架构。支持本地语音识别、语音合成、SteamVR覆盖显示、VRChat OSC通信等功能。

## 快速开始

### 开发环境启动
```bash
# 安装Python依赖
pip install -r requirements.txt

# 启动后端
python main.py

# 前端qing开发（新终端）
cd webUI
npm install
npm run serve
```

### 生产环境打包
```bash
# 打包为可执行文件
pyinstaller main.spec

# 或Docker部署
docker build -t vrcls .
docker run -p 5000:5000 vrcls
```

## 核心架构

### 技术栈
- **后端**: Python 3.8+ + Flask + SocketIO
- **前端**: Vue.js + Element UI
- **语音识别**: Sherpa-ONNX (本地) + Whisper API (云端)
- **语音合成**: Edge TTS + 虚拟麦克风
- **VR集成**: SteamVR + OpenVR + OSC协议

### 核心模块
```
src/
├── core/           # 核心功能
│   ├── startup.py      # 程序启动管理
│   ├── logger.py       # 日志系统
│   ├── serverListener.py   # 服务器通信
│   ├── steamvrProcess.py   # SteamVR集成
│   └── OSCListener.py      # OSC消息监听
├── handler/        # 业务处理器
│   ├── base_handler.py     # 处理器基类
│   ├── Avatar.py           # VRChat角色控制
│   ├── tts.py              # 语音合成
│   ├── VRCBitmapLedHandler.py  # 点阵屏显示
│   └── ChatBox.py          # 聊天框处理
└── module/         # 功能模块
    ├── sherpaOnnx.py   # 本地语音识别
    ├── translate.py    # 翻译功能
    ├── steamvr.py      # SteamVR功能
    └── oscserver.py    # OSC服务器
```

## 开发命令

### 常用开发操作
```bash
# 启动开发服务器
python main.py

# 运行测试脚本
python testScripts/oscclient.py      # 测试OSC通信
python testScripts/edgeTTs.py        # 测试TTS功能
python testScripts/translateTest1.py  # 测试翻译

# 前端开发
cd webUI
npm run serve        # 启动开发服务器
npm run build        # 构建生产版本

# 日志查看
tail -f VRCLS.log    # 实时查看日志
```

### 调试技巧
1. **日志调试**: 使用 `src.core.logger` 模块
2. **进程调试**: 使用 `testScripts/` 中的测试脚本
3. **Web调试**: 前端开发服务器支持热重载
4. **配置调试**: 通过Web UI实时修改配置

## 配置管理

### 主要配置文件
- `client.json`: 客户端配置（用户配置、服务器地址等）
- 配置结构：用户认证、OSC设置、语音识别、翻译设置、脚本配置

### 关键配置项
```json
{
  "baseurl": "服务器地址",
  "port": 9000,
  "ip": "127.0.0.1",
  "defaultMode": "control",
  "scripts": []  // 语音命令脚本
}
```

## 功能扩展

### 添加新语音命令
1. 在 `src/handler/` 创建处理器
2. 在配置文件中添加脚本配置
3. 遵循现有处理器模式继承 `BaseHandler`

### 添加新模块
1. 在 `src/module/` 创建模块文件
2. 在对应处理器中集成
3. 更新配置结构（如需要）

### Web界面扩展
1. 在 `webUI/src/views/` 添加新页面
2. 在 `webUI/src/components/` 添加组件
3. 更新路由和状态管理

## 部署注意事项

### 环境要求
- Windows 10/11 (当前项目为Windows专用)
- Python 3.8+
- Node.js 14+
- FFmpeg (需添加到PATH)
- SteamVR (用于VR功能)

### 打包注意事项
- 使用提供的 `main.spec` 文件
- 确保包含所有依赖库
- 测试所有功能模块
- 验证配置文件路径

## 故障排除

### 常见问题
1. **音频设备**: 检查设备权限和驱动
2. **OSC连接**: 确认端口配置和防火墙设置
3. **SteamVR**: 验证SteamVR运行状态和设备连接
4. **语音识别**: 检查模型文件完整性

### 调试工具
- 使用 `testScripts/` 中的测试脚本
- 查看 `VRCLS.log` 日志文件
- Web界面提供实时监控
- 使用浏览器开发者工具调试前端

## 后续交流语言

**后续所有交流将使用中文进行，包括代码注释、文档和对话。**