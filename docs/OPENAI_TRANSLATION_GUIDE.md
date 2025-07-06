# OpenAI翻译功能快速使用指南

## 🚀 快速开始

### 1. 获取API密钥
- **智谱AI** (推荐国内用户): https://open.bigmodel.cn/
- **OpenAI官方**: https://platform.openai.com/
- 注册账号 → 创建应用 → 获取API密钥

### 2. 配置VRCLS
1. 打开VRCLS配置界面
2. 进入"程序设置" → "翻译引擎"
3. 选择"OpenAI"作为翻译引擎
4. 填入配置信息：
   - **API密钥**: 你的API密钥
   - **API地址**: `https://open.bigmodel.cn/api/paas/v4/` (智谱AI)
   - **模型**: `glm-4-flash` (推荐)

### 3. 开始使用
- 选择"翻译模式"
- 说话即可获得AI翻译结果
- 支持多语言同时翻译

## ⚙️ 配置选项

### 推荐配置 (智谱AI)
```json
{
    "translateService": "openai",
    "openai_config": {
        "api_key": "your-api-key",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "model": "glm-4-flash"
    }
}
```

### 其他服务商
- **OpenAI官方**: `https://api.openai.com/v1`
- **Azure OpenAI**: `https://your-resource.openai.azure.com/`
- **自定义服务**: 任何兼容OpenAI API的服务

## 💰 费用参考

### 智谱AI (推荐)
- **glm-4-flash**: ¥0.006/1K tokens (输入) + ¥0.012/1K tokens (输出)
- **glm-4**: ¥0.1/1K tokens (输入) + ¥0.2/1K tokens (输出)
- **glm-3-turbo**: ¥0.005/1K tokens (输入) + ¥0.01/1K tokens (输出)

### OpenAI官方
- **GPT-3.5-turbo**: $0.0015/1K tokens (输入) + $0.002/1K tokens (输出)
- **GPT-4**: $0.03/1K tokens (输入) + $0.06/1K tokens (输出)

## 🔧 故障排除

### 常见问题

#### 1. API密钥错误
```
错误: OpenAI API密钥未配置
解决: 检查API密钥是否正确填入
```

#### 2. 网络连接问题
```
错误: 连接超时
解决: 检查网络连接和防火墙设置
```

#### 3. 模型不支持
```
错误: 模型不存在
解决: 检查模型名称和API服务是否支持
```

### 调试步骤
1. **查看日志**: 程序运行日志包含详细错误信息
2. **测试脚本**: 运行 `python testScripts/testOpenAITranslate.py`
3. **网络检查**: 确认API服务可访问性

## 📊 性能优化

### 批量翻译优势
- **减少API调用**: 从3次调用减少到1次
- **降低延迟**: 减少网络往返时间
- **节省成本**: 减少API调用次数

### 推荐设置
- **模型**: glm-4-flash (快速且准确)
- **温度**: 0.3 (翻译一致性)
- **最大tokens**: 1000 (适合大多数翻译)

## 🌍 支持的语言

### 主要语言
- **中文** (zh/zt): 简体中文/繁体中文
- **英语** (en): English
- **日语** (ja): 日本語
- **韩语** (ko): 한국어
- **俄语** (ru): Русский
- **法语** (fr): Français
- **德语** (de): Deutsch
- **西班牙语** (es): Español

### 其他语言
支持100+种全球语言，包括阿拉伯语、印地语、泰语、越南语等。

## 🎯 使用技巧

### 1. 多语言翻译
- 设置第二语言和第三语言
- 一次性获得多种语言翻译
- 节省API调用成本

### 2. 翻译质量
- 使用glm-4获得更高质量翻译
- 使用glm-4-flash获得更快响应
- 根据需求选择合适的模型

### 3. 成本控制
- 使用批量翻译减少API调用
- 选择合适的模型控制成本
- 监控API使用量

## 📝 测试验证

### 运行测试脚本
```bash
python testScripts/testOpenAITranslate.py
```

### 验证步骤
1. 配置API密钥
2. 运行测试脚本
3. 检查翻译结果
4. 确认功能正常

## 🔗 相关资源

- [完整文档](./OPENAI_INTEGRATION_SUMMARY.md)
- [智谱AI文档](https://open.bigmodel.cn/doc/api)
- [OpenAI API文档](https://platform.openai.com/docs)
- [项目GitHub](https://github.com/your-repo/VRCLS)

## 💡 提示

- 首次使用建议先运行测试脚本验证配置
- 推荐使用智谱AI服务，国内访问稳定
- 批量翻译功能可以显著节省成本
- 定期检查API使用量和费用

---

**注意**: 使用OpenAI翻译服务需要遵守相关服务条款和API使用规范。 