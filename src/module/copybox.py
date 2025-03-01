import tkinter as tk
from multiprocessing import Process, Queue
import time
import threading

class ScrollableListApp:
    def __init__(self, root, data_queue):
        self.root = root
        self.root.title("队列监听滚动列表")
        self.data_queue = data_queue
        
        # 存储显示行的列表（最多10行）
        self.row_frames = []
        
        # 初始化界面
        self.create_widgets()
        
        # 启动队列监听线程
        self.running = True
        self.start_queue_listener()

    def create_widgets(self):
        """ 创建界面组件 """
        # 列表容器
        self.list_container = tk.Frame(self.root)
        self.list_container.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # 初始化10个空行
        for _ in range(10):
            self._create_empty_row()

    def _create_empty_row(self):
        """ 创建空行占位 """
        frame = tk.Frame(self.list_container)
        frame.pack(fill=tk.X, pady=2)
        self.row_frames.append(frame)

    def _shift_rows_up(self, new_row):
        """ 滚动更新行 """
        # 移除最旧行
        oldest = self.row_frames.pop(0)
        oldest.destroy()
        
        # 添加新行
        new_row.pack(fill=tk.X, pady=2)
        self.row_frames.append(new_row)
        
        # 重新打包所有行
        for frame in self.row_frames:
            frame.pack_forget()
            frame.pack(fill=tk.X, pady=2)

    def start_queue_listener(self):
        """ 启动队列监听线程 """
        def listen():
            while self.running:
                # 非阻塞获取队列数据
                while not self.data_queue.empty():
                    text = self.data_queue.get()
                    self._add_new_item(text)
                
                # 控制刷新频率
                time.sleep(0.1)
        
        # 使用守护线程避免阻塞主线程
        threading.Thread(target=listen, daemon=True).start()

    def _add_new_item(self, text):
        """ 线程安全添加新条目 """
        # 必须在主线程操作GUI
        self.root.after(0, lambda: self._create_new_row(text))

    def _create_new_row(self, text):
        """ 实际创建新行 """
        new_row = tk.Frame(self.list_container)
        
        # 文本标签
        lbl = tk.Label(new_row, text=text, anchor="w", width=40)
        lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 复制按钮
        copy_btn = tk.Button(new_row, text="复制", 
                           command=lambda t=text: self._copy_text(t))
        copy_btn.pack(side=tk.RIGHT)
        
        # 滚动更新
        self._shift_rows_up(new_row)

    def _copy_text(self, text):
        """ 复制到剪贴板 """
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        
    def on_close(self):
        """ 窗口关闭处理 """
        self.running = False
        self.root.destroy()

# def data_producer(queue):
#     """ 数据生产者进程 """
#     counter = 1
#     while True:
#         # 模拟数据生成
#         time.sleep(1.5)
#         queue.put(f"识别结果：数据条目{counter}")
#         counter += 1

if __name__ == "__main__":
    # 创建进程间通信队列
    shared_queue = Queue()
    
    # # 启动数据生产进程
    # producer = Process(target=data_producer, args=(shared_queue,))
    # producer.daemon = True  # 设为守护进程随主进程退出
    # producer.start()
    
    # 启动GUI
    root = tk.Tk()
    app = ScrollableListApp(root, shared_queue)
    root.geometry("500x400")
    
    # 绑定关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
