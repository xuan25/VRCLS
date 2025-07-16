#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证本地模型下载和程序更新下载的日志输出区分
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.update import fast_download, main_update, module_download

def test_logging_differentiation():
    """测试日志输出区分"""
    print("=" * 60)
    print("测试本地模型下载和程序更新下载的日志输出区分")
    print("=" * 60)
    
    # 模拟logger类
    class MockLogger:
        def __init__(self):
            self.messages = []
        
        def put(self, message):
            self.messages.append(message)
            print(f"[{message['level'].upper()}] {message['text']}")
    
    logger = MockLogger()
    
    # 测试URL（这些URL不会真正下载，只是测试日志输出）
    model_url = "https://example.com/model.7z"
    update_url = "https://example.com/update.exe"
    
    print("\n1. 测试本地模型下载日志输出:")
    print("-" * 40)
    try:
        # 模拟模型下载（会失败，但可以看到日志输出）
        result = fast_download(model_url, Path("test_model.7z"), logger=logger, download_type="模型包")
        print(f"模型下载结果: {result}")
    except Exception as e:
        print(f"模型下载测试异常: {e}")
    
    print("\n2. 测试程序更新下载日志输出:")
    print("-" * 40)
    try:
        # 模拟程序更新下载（会失败，但可以看到日志输出）
        result = fast_download(update_url, Path("test_update.exe"), logger=logger, download_type="安装程序")
        print(f"程序更新下载结果: {result}")
    except Exception as e:
        print(f"程序更新下载测试异常: {e}")
    
    print("\n3. 测试module_download函数:")
    print("-" * 40)
    try:
        # 模拟module_download调用
        result = module_download(model_url, Path("."), logger=logger)
        print(f"module_download结果: {result}")
    except Exception as e:
        print(f"module_download测试异常: {e}")
    
    print("\n4. 测试main_update函数:")
    print("-" * 40)
    try:
        # 模拟main_update调用
        result = main_update(update_url, Path("."))
        print(f"main_update结果: {result}")
    except Exception as e:
        print(f"main_update测试异常: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    # 清理测试文件
    for test_file in ["test_model.7z", "test_update.exe"]:
        if Path(test_file).exists():
            Path(test_file).unlink()

if __name__ == "__main__":
    test_logging_differentiation() 