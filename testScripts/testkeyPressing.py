import keyboard

keyboard.add_hotkey('ctrl+2', lambda: print("快捷键触发"))

keyboard.wait('esc')  # 阻塞直到按下Esc键
