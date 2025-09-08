import threading
import webview
import time
import os

# 全局变量存储透明窗口实例
transparent_window = None

def start_overlay_window(config, socket_queue=None):
    """启动透明overlay窗口"""
    global transparent_window
    
    # 设置WebView2背景透明
    # os.environ["WEBVIEW2_DEFAULT_BACKGROUND_COLOR"] = "00FFFFFF"
    
    try:
        # 根据尺寸设置确定窗口大小
        size_config = config.get('transparentWindowSize', 'large')
        if size_config == 'large':
            width, height = 800, 500
        elif size_config == 'small':
            width, height = 400, 250
        elif size_config == 'custom':
            width = config.get('overlayWidth', 800)
            height = config.get('overlayHeight', 500)
        else:
            width, height = 800, 500  # 默认
        
        # 窗口位置固定为100,100
        x, y = 100, 100
        
        # 创建透明窗口
        transparent_window = webview.create_window(
            'VRCLS识别结果',
            f'http://{config["api-ip"]}:{config["api-port"]}/#/overlay',
            width=width,
            height=height,
            x=x,
            y=y,
            frameless=True,
            background_color='#00FFFFFF',
            on_top=True,
            resizable=False
        )
        webview.start(debug=False)
        
    except Exception as e:
        print(f"启动透明窗口失败: {e}")
        transparent_window = None
        return None

def close_transparent_window():
    """关闭透明窗口"""
    global transparent_window
    if transparent_window is not None:
        try:
            transparent_window.destroy()
            transparent_window = None
            return True
        except Exception as e:
            print(f"关闭透明窗口失败: {e}")
            return False
    return False