#!/usr/bin/env python3
"""简单测试overlay窗口"""

import os
import sys
import json
import webbrowser

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.defaultConfig import defaultConfig

def test_overlay_url():
    """测试overlay URL格式"""
    
    config = defaultConfig
    
    # 构建正确的URL
    base_url = f"http://{config['api-ip']}:{config['api-port']}"
    overlay_url = f"{base_url}/#/overlay"
    
    print("=== Overlay URL 测试 ===")
    print(f"基础URL: {base_url}")
    print(f"Overlay URL: {overlay_url}")
    print(f"主页URL: {base_url}/")
    
    return overlay_url

def test_config_values():
    """测试overlay配置值"""
    
    config = defaultConfig
    
    overlay_config = {
        'enableRecognitionOverlay': config.get('enableRecognitionOverlay', False),
        'overlayWidth': config.get('overlayWidth', 400),
        'overlayHeight': config.get('overlayHeight', 200),
        'overlayX': config.get('overlayX', 100),
        'overlayY': config.get('overlayY', 100)
    }
    
    print("\n=== Overlay 配置 ===")
    for key, value in overlay_config.items():
        print(f"{key}: {value}")
    
    return overlay_config

if __name__ == "__main__":
    print("VRCLS Overlay 测试")
    print("=" * 30)
    
    # 测试URL
    url = test_overlay_url()
    
    # 测试配置
    config = test_config_values()
    
    print("\n" + "=" * 30)
    print("使用方法:")
    print("1. 启动主程序: python main.py")
    print("2. 在client.json中设置: 'enableRecognitionOverlay': true")
    print("3. 或者手动访问:", url)
    print("4. 测试: 在浏览器中打开", url)
    
    # 询问是否要在浏览器中打开测试URL
    try:
        import webbrowser
        webbrowser.open(url)
        print("已在浏览器中打开测试URL")
    except:
        print("无法自动打开浏览器，请手动访问URL")