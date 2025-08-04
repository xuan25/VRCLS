# VRCLS 透明识别结果窗口使用指南

## 功能概述
透明识别结果窗口是一个底框透明的pywebview子窗口，用于显示最新的三条麦克风识别结果（左侧）和桌面音频识别结果（右侧）。

## 启用方法

### 方法一：通过配置文件启用
1. 打开 `client.json` 配置文件
2. 添加或修改以下配置：
```json
{
  "enableRecognitionOverlay": true,
  "overlayWidth": 400,
  "overlayHeight": 200,
  "overlayX": 100,
  "overlayY": 100
}
```

### 方法二：通过Web界面配置
1. 启动程序后访问 http://127.0.0.1:8980
2. 在设置中找到"启用透明识别窗口"选项
3. 启用后保存配置并重启程序

## 访问方式

### 直接访问
- **透明窗口URL**: http://127.0.0.1:8980/#/overlay
- **主界面URL**: http://127.0.0.1:8980/

### 浏览器测试
在浏览器中直接访问透明窗口路由：
```
http://127.0.0.1:8980/#/overlay
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enableRecognitionOverlay` | `false` | 是否启用透明识别窗口 |
| `overlayWidth` | `400` | 窗口宽度（像素） |
| `overlayHeight` | `200` | 窗口高度（像素） |
| `overlayX` | `100` | 窗口X坐标（像素） |
| `overlayY` | `100` | 窗口Y坐标（像素） |

## 技术架构

### 前端部分
- **Vue 3**: 前端框架
- **Vue Router**: 路由管理
- **Vuex**: 状态管理
- **Socket.io**: 实时通信
- **透明样式**: CSS3 rgba和backdrop-filter

### 后端部分
- **Flask**: Web服务器
- **Socket.io**: WebSocket实时通信
- **PyWebView**: 透明窗口创建

### 通信机制
- 麦克风识别结果通过 `socket.emit('mic', {text: '识别内容'})`
- 桌面音频识别结果通过 `socket.emit('cap', {text: '识别内容'})`
- 前端实时接收并显示最新3条记录

## 故障排除

### 404错误
如果访问 `/#/overlay` 出现404：
1. 确保前端已正确构建：`cd webUI && npm run build`
2. 检查templates目录是否存在构建后的文件
3. 确认Flask服务器正常运行

### 窗口不显示
1. 检查配置文件中的 `enableRecognitionOverlay` 是否为 `true`
2. 确认WebView2运行时已安装
3. 检查防火墙是否阻止了端口8980

### 内容不更新
1. 确认socket.io连接正常
2. 检查后端日志是否有识别结果输出
3. 验证网络连接是否稳定

## 开发测试

### 快速测试
```bash
# 构建前端
cd webUI
npm run build

# 启动测试程序
python main.py

# 在浏览器中测试
http://127.0.0.1:8980/#/overlay
```

### 测试脚本
```bash
# 运行路由测试
python testScripts/test_routes.py

# 运行简单测试
python testScripts/test_overlay_simple.py
```

## 注意事项
1. 透明窗口需要WebView2运行时支持
2. 首次使用可能需要安装Microsoft Edge WebView2
3. 窗口位置可以根据需要调整配置参数
4. 透明效果在部分系统上可能需要GPU支持