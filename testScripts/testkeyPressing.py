from pynput import keyboard

class VoiceRecognitionController:
    def __init__(self):
        self.alt_pressed = False
        self.q_pressed = False
        self.recording = False
        self.listener = None

    def _on_press(self, key):
        # 处理Alt键按下
        if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            self.alt_pressed = True
        # 处理Q键按下（不区分大小写）
        elif hasattr(key, 'char') and key.char.lower() == 'q':
            self.q_pressed = True

        # 检查组合键条件
        if not self.recording and self.alt_pressed and self.q_pressed:
            self.recording = True
            print("Recording START (Alt+Q pressed)")

    def _on_release(self, key):
        # 处理Alt键释放
        if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            self.alt_pressed = False
        # 处理Q键释放
        elif hasattr(key, 'char') and key.char.lower() == 'q':
            self.q_pressed = False

        # 检查是否需要停止录音
        if self.recording and (not self.alt_pressed or not self.q_pressed):
            self.recording = False
            print("Recording STOP (Key released)")

    def start(self):
        """启动键盘监听"""
        self.listener = keyboard.Listener(
            on_press=self._on
