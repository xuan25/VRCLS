import webview
import ctypes
import ctypes.wintypes
import platform
import threading # 仅用于演示从 Python 线程触发，通常 JS API 更合适

# --- 辅助函数，用于在 Windows 上设置窗口边框颜色 (与之前相同) ---
def set_window_frame_color_windows(hwnd, use_dark_mode: bool):
    if platform.system() == "Windows":
        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1 if use_dark_mode else 0)
            hwnd_proper = ctypes.wintypes.HWND(hwnd)
            hr = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd_proper,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
            if hr != 0:
                print(f"警告: DwmSetWindowAttribute (属性 {DWMWA_USE_IMMERSIVE_DARK_MODE}) 失败, HRESULT: {hr:#08x}")
                # 尝试后备属性 19
                DWMWA_USE_IMMERSIVE_DARK_MODE_FALLBACK = 19
                hr_fallback = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd_proper,
                    DWMWA_USE_IMMERSIVE_DARK_MODE_FALLBACK,
                    ctypes.byref(value),
                    ctypes.sizeof(value)
                )
                if hr_fallback == 0:
                    print(f"成功使用后备属性 {DWMWA_USE_IMMERSIVE_DARK_MODE_FALLBACK} 应用模式。")
                else:
                    print(f"警告: DwmSetWindowAttribute (属性 {DWMWA_USE_IMMERSIVE_DARK_MODE_FALLBACK}) 也失败, HRESULT: {hr_fallback:#08x}")
            else:
                print(f"成功应用沉浸式 {'暗色' if use_dark_mode else '亮色'} 模式。")
            return True
        except Exception as e:
            print(f"设置窗口边框颜色时出错: {e}")
            return False
    else:
        print("此功能仅限 Windows。")
        return False

# --- 模拟您的 startUp 和 toggle_console ---
class MockStartUp:
    config = {'api-ip': '127.0.0.1', 'api-port': 8080}

startUp = MockStartUp()

def toggle_console(show_console_flag):
    print(f"toggle_console (Python 控制台) 被调用，参数: {show_console_flag}")
    # 实际的控制台切换逻辑会更复杂

# --- 用于暴露给 JavaScript 的 API 类 ---
class WindowApi:
    def __init__(self, window_instance):
        self.window = window_instance # pywebview 窗口实例

    def change_frame_theme(self, use_dark_theme: bool):
        """
        从 JavaScript 调用的函数，用于更改窗口边框主题。
        """
        if self.window and self.window.hwnd:
            print(f"从 JS 请求更改边框主题为: {'暗色' if use_dark_theme else '亮色'}")
            success = set_window_frame_color_windows(self.window.hwnd, use_dark_theme)
            return {"success": success, "theme": "dark" if use_dark_theme else "light"}
        else:
            print("错误: window 对象或 hwnd 不可用。")
            return {"success": False, "error": "Window or HWND not available."}

    def get_initial_theme_preference(self):
        """允许 JS 获取初始主题设置（如果需要）"""
        # 这里可以返回一个预设值或从某处读取
        return {"is_dark": True} # 示例：初始为暗色

# --- 主应用程序逻辑 ---
if __name__ == '__main__':
    initial_dark_frame = True # 初始边框颜色
    show_console_initially = False

    # HTML 内容，包含调用 Python API 的按钮
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>控制面板</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; }}
            button {{ margin: 10px; padding: 10px 15px; font-size: 16px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>VRCLS 控制面板</h1>
        <p>点击下方按钮动态更改窗口边框颜色：</p>
        <button onclick="setDarkFrame()">应用暗色边框</button>
        <button onclick="setLightFrame()">应用亮色边框</button>
        <p id="status"></p>

        <script>
            async function setDarkFrame() {{
                try {{
                    let result = await window.pywebview.api.change_frame_theme(true);
                    document.getElementById('status').innerText = '设置暗色边框结果: ' + JSON.stringify(result);
                }} catch (e) {{
                    document.getElementById('status').innerText = '错误: ' + e;
                    console.error(e);
                }}
            }}

            async function setLightFrame() {{
                try {{
                    let result = await window.pywebview.api.change_frame_theme(false);
                    document.getElementById('status').innerText = '设置亮色边框结果: ' + JSON.stringify(result);
                }} catch (e) {{
                    document.getElementById('status').innerText = '错误: ' + e;
                    console.error(e);
                }}
            }}

            // 可以在加载时获取初始主题（如果 API 支持）
            // window.pywebview.api.get_initial_theme_preference().then(prefs => {{
            //     console.log("初始主题偏好:", prefs);
            //     // 根据 prefs.is_dark 设置初始状态（如果需要）
            // }});
        </script>
    </body>
    </html>
    """

    # 创建窗口实例
    # 注意：这里不直接使用 f-string 格式化 URL，而是使用 html 参数加载本地内容
    # 如果您确实需要从 http://ip:port 加载，请确保该服务器正在运行并提供相应的 JS 调用。
    window_obj = webview.create_window(
        'VRCLS控制面板',
        html=html_content, # 加载上面的 HTML 字符串
        # url=f'http://{startUp.config["api-ip"]}:{startUp.config["api-port"]}', # 或者您的 URL
        width=1200,
        height=800
    )

    # 创建 API 实例，并传入窗口对象
    api = WindowApi(window_obj)

    # 'shown' 事件，用于设置初始边框颜色
    def on_shown():
        print(f"窗口已显示。HWND: {window_obj.hwnd}")
        if window_obj.hwnd:
            set_window_frame_color_windows(window_obj.hwnd, initial_dark_frame)
        else:
            print("错误: window.hwnd 在 'shown' 事件后仍然不可用。")

    window_obj.events.shown += on_shown

    toggle_console(show_console_initially)

    # 启动 webview，并传入 js_api 参数
    webview.start(debug=True, js_api=api) # debug=True 可以方便地打开开发者工具