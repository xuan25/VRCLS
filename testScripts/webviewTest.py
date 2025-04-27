import webview

window = webview.create_window(
    'VRCLS控制面板', 
    f'http://127.0.0.1:8980',
    width=1200,
    height=800
)
webview.start()