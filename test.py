import keyboard
import time

# 定义快捷键回调函数
def on_hotkey_1():
    print("Hotkey Ctrl+Shift+A pressed!")

def on_hotkey_2():
    print("Hotkey Alt+Q pressed!")

# 注册快捷键
keyboard.add_hotkey('ctrl+shift+a', on_hotkey_1)
keyboard.add_hotkey('alt+q', on_hotkey_2)

print("Listening for hotkeys in the background. Press Ctrl+C to exit.")

try:
    # 保持程序运行以监听快捷键
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    # 清理资源
    keyboard.unhook_all()