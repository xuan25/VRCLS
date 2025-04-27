from pynput import keyboard
import time

class VKeyHandler:
    def __init__(self,params,keyname):
        self.listener = None
        self.params=params
        self.keyname=keyname
        self.checkKey=params['config'].get("capPressingKey") if keyname=='gameVoiceKeyRun' else params['config'].get("micPressingKey")
        self.checkKey=self.checkKey[0].lower()
    def on_press(self, key):
        # 检测按下V键（包括Shift+V的大写情况）
        try:
            if key.char.lower() == self.checkKey:
                self.handle_key_press()
        except AttributeError:
            pass

    def on_release(self, key):
        # 检测释放V键
        try:
            if key.char.lower() == self.checkKey:
                self.handle_key_release()
        except AttributeError:
            pass

    def handle_key_press(self):
        if not self.params[self.keyname]:
            self.params[self.keyname]=True 
        # print("V键被按下，执行按下操作")
        # 在此处添加按下V键时需要执行的代码

    def handle_key_release(self):
        if self.params[self.keyname]:
            time.sleep(2)
            self.params[self.keyname]=False
        # print("V键被释放，执行释放操作")
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