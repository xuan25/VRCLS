#!/usr/bin/env python3
"""测试透明overlay窗口功能"""

import requests
import time
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.defaultConfig import defaultConfig

def test_overlay_routes():
    """测试overlay路由是否可访问"""
    
    # 使用默认配置
    config = defaultConfig
    
    # 构建基础URL
    base_url = f"http://{config['api-ip']}:{config['api-port']}"
    
    print(f"测试基础URL: {base_url}")
    
    try:
        # 测试根路径
        response = requests.get(base_url, timeout=5)
        print(f"✓ 根路径访问成功: {response.status_code}")
        
        # 测试overlay路由 (通过Vue Router的hash模式)
        overlay_url = f"{base_url}/#/overlay"
        print(f"测试overlay路由: {overlay_url}")
        
        # 注意：对于Vue Router的hash模式，我们测试的是SPA页面
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✓ overlay路由可访问 (通过SPA)")
            
            # 检查页面内容
            if "overlay" in response.text.lower():
                print("✓ overlay相关内容在页面中找到")
            else:
                print("⚠ overlay内容未在页面中找到")
                
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 测试异常: {e}")
        return False

def test_config():
    """测试overlay配置"""
    print("\n=== 配置测试 ===")
    
    config = defaultConfig
    
    overlay_config = {
        'enableRecognitionOverlay': config.get('enableRecognitionOverlay', False),
        'overlayWidth': config.get('overlayWidth', 400),
        'overlayHeight': config.get('overlayHeight', 200),
        'overlayX': config.get('overlayX', 100),
        'overlayY': config.get('overlayY', 100)
    }
    
    print("overlay配置:")
    for key, value in overlay_config.items():
        print(f"  {key}: {value}")
    
    return True

if __name__ == "__main__":
    print("=== VRCLS Overlay 功能测试 ===")
    
    # 测试配置
    test_config()
    
    # 测试路由访问
    test_overlay_routes()
    
    print("\n测试完成！请确保:")
    print("1. Flask服务器已启动")
    print("2. 前端已构建 (npm run build)")
    print("3. 访问 http://127.0.0.1:8980/#/overlay 查看overlay页面")