import threading
import webview
import time

def start_overlay_window(config, socket_queue=None):
    """启动透明overlay窗口"""
    
    def run_overlay():
        try:
            # 创建透明窗口
            window = webview.create_window(
                'VRCLS识别结果',
                f'http://{config["api-ip"]}:{config["api-port"]}/#/overlay',
                width=config.get('overlayWidth', 400),
                height=config.get('overlayHeight', 200),
                x=config.get('overlayX', 100),
                y=config.get('overlayY', 100),
                frameless=True,
                on_top=True,
                transparent=True,
                resizable=False
            )
            
            webview.start(debug=False)
            
        except Exception as e:
            print(f"启动透明窗口失败: {e}")
    
    # 在独立线程中启动
    overlay_thread = threading.Thread(target=run_overlay, daemon=True)
    overlay_thread.start()
    return overlay_thread