# # from pynput import keyboard
# # from pynput.keyboard import Key, KeyCode
# # from functools import partial

# # class HotkeyListener:
# #     def __init__(self,logger):
# #         self.current_keys = set()
# #         self.listener = None
# #         self.hotkey_map = {}

# #     def _on_press(self, key):
# #         self.current_keys.add(key)
# #         self._check_hotkey()

# #     def _on_release(self, key):
# #         try:
# #             self.current_keys.remove(key)
# #         except KeyError:
# #             pass

# #     def _parse_hotkey(self, hotkey_str):
# #         """将字符串热键解析为键集合，例如 'ctrl+shift+a' -> {Key.ctrl, Key.shift, 'a'}"""
# #         keys = []
# #         for part in hotkey_str.lower().split('+'):
# #             if hasattr(Key, part):
# #                 keys.append(getattr(Key, part))
# #             else:
# #                 keys.append(KeyCode.from_char(part))
# #         return set(keys)

# #     def _check_hotkey(self):
# #         """检查当前按下的键是否匹配注册的热键"""
# #         for hotkey_str, (callback, args) in self.hotkey_map.items():
# #             required_keys = self._parse_hotkey(hotkey_str)
# #             if required_keys.issubset(self.current_keys):
# #                 callback(*args)

# #     def add_hotkey(self, hotkey, callback, args=()):
# #         """注册热键和回调函数"""
# #         self.hotkey_map[hotkey] = (callback, args)
# #         if not self.listener:
# #             self.listener = keyboard.Listener(
# #                 on_press=self._on_press,
# #                 on_release=self._on_release)
# #             self.listener.start()

# #     def stop(self):
# #         """停止监听"""
# #         if self.listener:
# #             self.listener.stop()

# # # 使用示例
# # def callback_example(param1, logger, action):
# #     logger.info(f"{action} triggered with param: {param1}")

# # if __name__ == "__main__":
# #     import logging
# #     logging.basicConfig(level=logging.INFO)
# #     logger = logging.getLogger("HotkeyLogger")
    
# #     # 初始化监听器
# #     listener = HotkeyListener(logger)
    
# #     # 注册热键（支持修饰键+普通键的组合）
# #     listener.add_hotkey(
# #         hotkey="shift+alt_l+@+#",
# #         callback=callback_example,
# #         args=("config_value", logger, "cap")
# #     )
    
# #     # 保持主线程运行
# #     try:
# #         while True: pass
# #     except KeyboardInterrupt:
# #         listener.stop()
# from pynput import keyboard
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("HotkeyLogger")
# # 定义组合键需要的按键（注意：普通字符需转换为字符串）
# COMBINATION = {keyboard.Key.ctrl, 's'}
# current_keys = set()
# combination_met = False  # 标记组合键是否已激活

# def on_press(key):
#     global combination_met
#     # 处理特殊键（如Ctrl、Shift）的左右版本
#     if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
#         current_keys.add(keyboard.Key.ctrl)
#     elif key in (keyboard.Key.shift_l, keyboard.Key.shift_r):
#         current_keys.add(keyboard.Key.shift)
#     else:
#         current_keys.add(key)

#     # 检查是否满足组合键条件
#     if COMBINATION.issubset(current_keys):
#         if not combination_met:
#             combination_met = True
#             function
#             print("组合键按下，触发函数A")
#             function_a()  # 按下时触发的函数

# def on_release(key):
#     global combination_met, current_keys
#     # 处理特殊键的移除
#     if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
#         current_keys.discard(keyboard.Key.ctrl)
#     elif key in (keyboard.Key.shift_l, keyboard.Key.shift_r):
#         current_keys.discard(keyboard.Key.shift)
#     else:
#         current_keys.discard(key)

#     # 如果组合键条件不再满足且之前已被激活
#     if not COMBINATION.issubset(current_keys) and combination_met:
#         combination_met = False
#         print("组合键释放，触发函数B")
#         function_b()  # 释放时触发的函数

# def function_a():
#     # 按下组合键时要执行的操作
#     logger.info('down')

# def function_b():
#     # 释放组合键时要执行的操作
#     logger.info('up')



# # 启动监听
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     logger.info('111')
#     listener.join()
from multiprocessing import Manager,freeze_support
if __name__ == '__main__':
    freeze_support()
    from functools import partial
    from pynput import keyboard

    manager = Manager()
    params=manager.dict()
    import time
    params['a']=True
    def on_activate_h():
        print('<ctrl>+<alt>+h pressed')
    
    def on_activate_i():
        print('<ctrl>+<alt>+i pressed')
    
    def esc(params):
        params['a']=not params['a']
        print(f'<esc> pressed++{params['a']}')
        return False
    
    def esc_shift():
        print('<esc>+<shift> pressed')
        raise Exception
    esc1=partial(esc,params)
    a1=keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+h': on_activate_h,
            '<alt>+1': partial(esc,params),
            '<esc>':          esc1,
            '<esc>+<shift>':  esc_shift})
    a1.start()
    a1.stop()
    while True:
        time.sleep(1)
        print(123123)
    
    
    # with keyboard.GlobalHotKeys({
    #         '<ctrl>+<alt>+h': on_activate_h,
    #         '<ctrl>+<alt>+i': on_activate_i,
    #         '<esc>':          esc,
    #         '<esc>+<shift>':  esc_shift}) as h:
    #     h.join()