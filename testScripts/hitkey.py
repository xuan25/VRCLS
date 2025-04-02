from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from functools import partial

class HotkeyListener:
    def __init__(self,logger):
        self.current_keys = set()
        self.listener = None
        self.hotkey_map = {}

    def _on_press(self, key):
        self.current_keys.add(key)
        self._check_hotkey()

    def _on_release(self, key):
        try:
            self.current_keys.remove(key)
        except KeyError:
            pass

    def _parse_hotkey(self, hotkey_str):
        """将字符串热键解析为键集合，例如 'ctrl+shift+a' -> {Key.ctrl, Key.shift, 'a'}"""
        keys = []
        for part in hotkey_str.lower().split('+'):
            if hasattr(Key, part):
                keys.append(getattr(Key, part))
            else:
                keys.append(KeyCode.from_char(part))
        return set(keys)

    def _check_hotkey(self):
        """检查当前按下的键是否匹配注册的热键"""
        for hotkey_str, (callback, args) in self.hotkey_map.items():
            required_keys = self._parse_hotkey(hotkey_str)
            if required_keys.issubset(self.current_keys):
                callback(*args)

    def add_hotkey(self, hotkey, callback, args=()):
        """注册热键和回调函数"""
        self.hotkey_map[hotkey] = (callback, args)
        if not self.listener:
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release)
            self.listener.start()

    def stop(self):
        """停止监听"""
        if self.listener:
            self.listener.stop()

# 使用示例
def callback_example(param1, logger, action):
    logger.info(f"{action} triggered with param: {param1}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("HotkeyLogger")
    
    # 初始化监听器
    listener = HotkeyListener(logger)
    
    # 注册热键（支持修饰键+普通键的组合）
    listener.add_hotkey(
        hotkey="shift+alt_l+@+#",
        callback=callback_example,
        args=("config_value", logger, "cap")
    )
    
    # 保持主线程运行
    try:
        while True: pass
    except KeyboardInterrupt:
        listener.stop()
