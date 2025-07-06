#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI集成验证脚本
检查所有相关文件是否正确配置
"""

import os
import sys

def check_file_exists(file_path):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {file_path}")
        return True
    else:
        print(f"❌ {file_path} - 文件不存在")
        return False

def check_imports():
    """检查模块导入"""
    try:
        # 添加项目根目录到路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(project_root)
        
        # 检查翻译模块
        from src.module.translate import openai_translator
        print("✅ OpenAI翻译模块导入成功")
        
        # 检查默认配置
        from src.core.defaultConfig import defaultConfig
        if "openai_config" in defaultConfig:
            print("✅ OpenAI配置已添加到默认配置")
        else:
            print("❌ OpenAI配置未添加到默认配置")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def check_frontend_files():
    """检查前端文件"""
    frontend_files = [
        "webUI/src/components/config-page.vue",
        "webUI/src/i18n/locales/zh.js",
        "webUI/src/i18n/locales/en.js", 
        "webUI/src/i18n/locales/ja.js"
    ]
    
    success = True
    for file_path in frontend_files:
        if not check_file_exists(file_path):
            success = False
            
    return success

def check_backend_files():
    """检查后端文件"""
    backend_files = [
        "src/module/translate.py",
        "src/core/defaultConfig.py",
        "src/core/serverActionProcess.py",
        "requirements.txt"
    ]
    
    success = True
    for file_path in backend_files:
        if not check_file_exists(file_path):
            success = False
            
    return success

def check_test_files():
    """检查测试文件"""
    test_files = [
        "testScripts/testOpenAITranslate.py",
        "OPENAI_INTEGRATION_SUMMARY.md"
    ]
    
    success = True
    for file_path in test_files:
        if not check_file_exists(file_path):
            success = False
            
    return success

def main():
    """主验证函数"""
    print("=== OpenAI集成验证 ===")
    print()
    
    # 检查文件存在性
    print("1. 检查文件存在性:")
    backend_ok = check_backend_files()
    frontend_ok = check_frontend_files()
    test_ok = check_test_files()
    
    print()
    print("2. 检查模块导入:")
    import_ok = check_imports()
    
    print()
    print("=== 验证结果 ===")
    
    if backend_ok and frontend_ok and test_ok and import_ok:
        print("🎉 所有验证通过！OpenAI集成已完成")
        print()
        print("下一步:")
        print("1. 配置API密钥")
        print("2. 运行测试脚本: python testScripts/testOpenAITranslate.py")
        print("3. 在VRCLS中选择OpenAI翻译引擎")
        return True
    else:
        print("⚠️  部分验证失败，请检查相关文件")
        return False

if __name__ == "__main__":
    main() 