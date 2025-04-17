# # import keyboard

# # keyboard.add_hotkey('ctrl+2', lambda: print("快捷键触发"))

# # keyboard.wait('esc')  # 阻塞直到按下Esc键



# import keyboard
# from threading import Event
# import time

# class ComboDetector:
#     def __init__(self):
#         self.combination = {'ctrl', 'shift', 'a'}
#         self.current_keys = set()
#         self.active = False
#         self.last_trigger = 0
        
#         keyboard.on_press(self._on_press)
#         keyboard.on_release(self._on_release)
        


#     def _normalize_key(self, key):
#         # key = key.replace(' ', '_').lower()
#         print(key)
#         # 统一处理修饰键变体
#         return key
#     def _on_press(self, e):
#         key = self._normalize_key(e.name)
#         self.current_keys.add(key)
#         self._check()
        
#     def _on_release(self, e):
#         key = self._normalize_key(e.name)
#         if key in self.current_keys:
#             self.current_keys.remove(key)
#         self._check()
        
#     def _check(self):
#         now = time.time()
#         if self.combination.issubset(self.current_keys):
#             if not self.active and (now - self.last_trigger) > 0.5:
#                 self.active = True
#                 self.last_trigger = now
#                 self.on_activate()
#         else:
#             if self.active:
#                 self.active = False
#                 self.on_deactivate()
                
#     def on_activate(self):
#         print("🔔 组合键激活！启动特殊模式")
        
#     def on_deactivate(self):
#         print("🔕 组合键释放！返回普通模式")

# if __name__ == "__main__":
#     detector = ComboDetector()
#     Event().wait()  # 保持程序运行
from pynput import keyboard
import time

class VKeyHandler:
    def __init__(self,params):
        self.listener = None
        self.params=params

    def on_press(self, key):
        # 检测按下V键（包括Shift+V的大写情况）
        try:
            if key.char.lower() == 'v':
                self.handle_key_press()
        except AttributeError:
            pass

    def on_release(self, key):
        # 检测释放V键
        try:
            if key.char.lower() == 'v':
                self.handle_key_release()
        except AttributeError:
            pass

    def handle_key_press(self):
        print("V键被按下，执行按下操作")
        # 在此处添加按下V键时需要执行的代码

    def handle_key_release(self):
        print("V键被释放，执行释放操作")
        # 在此处添加释放V键时需要执行的代码

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop(self):
        if self.listener is not None:
            self.listener.stop()

# 使用示例
if __name__ == "__main__":
    v_handler = VKeyHandler()
    v_handler.start()

    try:
        # 模拟主程序运行
        while True:
            print("主程序正在运行...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("正在退出程序...")
        v_handler.stop()
