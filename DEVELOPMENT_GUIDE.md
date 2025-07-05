# VRCLS 开发指南

## 开发环境搭建

### 系统要求
- Windows 10/11
- Python 3.8+
- Node.js 14+
- Git

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

## 项目结构理解

### 核心架构
```
VRCLS/
├── main.py                 # 主程序入口
├── src/                    # 核心源代码
│   ├── core/              # 核心功能模块
│   ├── handler/           # 处理器模块
│   ├── module/            # 功能模块
│   └── core/tinyoscquery/ # OSC查询模块
├── webUI/                 # Web前端
└── testScripts/           # 测试脚本
```

### 模块职责

#### 核心模块 (`src/core/`)
- **startup.py**: 程序启动和初始化
- **logger.py**: 日志系统
- **serverListener.py**: 服务器通信
- **steamvrProcess.py**: SteamVR集成

#### 处理器模块 (`src/handler/`)
- **base_handler.py**: 处理器基类
- **Avatar.py**: Avatar控制
- **tts.py**: 语音合成
- **VRCBitmapLedHandler.py**: 点阵屏显示

#### 功能模块 (`src/module/`)
- **sherpaOnnx.py**: 语音识别
- **steamvr.py**: SteamVR功能
- **translate.py**: 翻译功能

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

#### 添加新页面
1. 在 `webUI/src/views/` 创建Vue组件
2. 在 `webUI/src/router/` 添加路由
3. 在 `webUI/src/store/` 添加状态管理

#### 示例：添加配置页面
```vue
<!-- webUI/src/views/ConfigPage.vue -->
<template>
  <div class="config-page">
    <el-form :model="config" label-width="120px">
      <el-form-item label="服务器地址">
        <el-input v-model="config.baseurl"></el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'ConfigPage',
  data() {
    return {
      config: {}
    }
  },
  methods: {
    async loadConfig() {
      const response = await fetch('/api/getConfig')
      this.config = await response.json()
    }
  }
}
</script>
```

### 3. API开发

#### 添加新API接口
1. 在 `main.py` 中添加路由
2. 实现接口逻辑
3. 添加错误处理
4. 更新API文档

#### 示例：添加设备状态API
```python
@app.route('/api/deviceStatus', methods=['GET'])
def get_device_status():
    try:
        status = {
            'mic_active': mic_status,
            'desktop_audio_active': desktop_audio_status,
            'vr_active': vr_status
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 调试技巧

### 1. 日志调试
```python
from src.core.logger import logger

logger.info("调试信息")
logger.error("错误信息")
logger.debug("详细调试信息")
```

### 2. 测试脚本
使用 `testScripts/` 目录中的脚本进行功能测试：
```bash
python testScripts/oscclient.py  # 测试OSC通信
python testScripts/edgeTTs.py    # 测试TTS功能
```

### 3. Web界面调试
```bash
cd webUI
npm run serve  # 启动开发服务器
```

### 4. 进程调试
```python
# 在main.py中添加调试信息
import psutil
print(f"当前进程: {psutil.Process().pid}")
print(f"内存使用: {psutil.Process().memory_info().rss / 1024 / 1024} MB")
```

## 配置管理

### 配置文件结构
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
    "scripts": []
}
```

### 配置验证
```python
def validate_config(config):
    required_fields = ['userInfo', 'baseurl', 'port']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"缺少必需配置: {field}")
```

## 性能优化

### 1. 内存优化
- 使用生成器处理大量数据
- 及时释放不需要的对象
- 使用弱引用避免循环引用

### 2. CPU优化
- 使用多进程处理CPU密集型任务
- 缓存计算结果
- 优化算法复杂度

### 3. 网络优化
- 使用连接池
- 实现请求重试机制
- 压缩传输数据

## 错误处理

### 1. 异常处理模式
```python
def safe_function():
    try:
        # 可能出错的代码
        result = risky_operation()
        return result
    except SpecificException as e:
        logger.error(f"特定错误: {e}")
        return fallback_value
    except Exception as e:
        logger.error(f"未知错误: {e}")
        raise
```

### 2. 错误恢复
```python
def resilient_function():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
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