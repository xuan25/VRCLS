import tkinter as tk
from tkinter import colorchooser, messagebox
import queue
import threading

class UltimateOverlay:
    def __init__(self, msg_queue=None):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # 队列设置
        self.msg_queue = msg_queue or queue.Queue()
        
        # 透明背景设置
        self.transparent_color = 'gray15'
        self.root.config(bg=self.transparent_color)
        self.root.attributes('-transparentcolor', self.transparent_color)
        
        # 初始化窗口尺寸
        self.width, self.height = 300, 100
        self.root.geometry(f"{self.width}x{self.height}+100+100")
        
        # 创建画布
        self.canvas = tk.Canvas(
            self.root,
            bg=self.transparent_color,
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # 文字设置
        self.text_color = 'white'
        self.stroke_color = 'black'
        self.stroke_width = 2
        self._draw_stroked_text("初始化文字")
        
        # 事件绑定
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<Button-3>", self.show_menu)
        self.root.bind("<Enter>", self.show_border)
        self.root.bind("<Leave>", self.hide_border)
        self.root.bind("<Escape>", self.close)
        
        # 右键菜单
        self.init_context_menu()
        
        # 窗口调整相关变量
        self.resize_area = 10
        self.resizing = False
        self.dragging = False
        self.start_x = 0
        self.start_y = 0
        
        # 启动队列检查
        self.check_queue()

    def check_queue(self):
        """ 定期检查消息队列 """
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                self._draw_stroked_text(msg)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def _draw_stroked_text(self, text):
        """ 绘制带黑色描边的文字 """
        self.canvas.delete("all")
        x, y = self.width//2, self.height//2
        
        # 绘制文字描边（8个方向偏移）
        offsets = [(-1,-1), (-1,0), (-1,1),
                   (0,-1),         (0,1),
                   (1,-1),  (1,0), (1,1)]
        for dx, dy in offsets:
            self.canvas.create_text(
                x + dx*self.stroke_width,
                y + dy*self.stroke_width,
                text=text,
                fill=self.stroke_color,
                font=('微软雅黑', 16, 'bold'),
                anchor='center'
            )
        
        # 绘制主文字
        self.text_item = self.canvas.create_text(
            x, y,
            text=text,
            fill=self.text_color,
            font=('微软雅黑', 16, 'bold'),
            anchor='center'
        )
    def show_border(self, event=None):
        """ 显示红色边框 """
        self.canvas.create_rectangle(
            2, 2, self.width-2, self.height-2,
            outline='red',
            width=2,
            tags='temp_border'
        )

    def hide_border(self, event=None):
        """ 隐藏红色边框 """
        self.canvas.delete('temp_border')

    def on_click(self, event):
        """ 处理鼠标点击事件 """
        self.start_x = event.x_root
        self.start_y = event.y_root
        
        # 判断是否在调整区域（右下角10x10像素）
        if (self.width - self.resize_area < event.x < self.width and 
            self.height - self.resize_area < event.y < self.height):
            self.resizing = True
            self.dragging = False
        else:
            self.dragging = True
            self.resizing = False

    def on_drag(self, event):
        """ 处理拖动事件 """
        if self.dragging:
            # 移动窗口
            dx = event.x_root - self.start_x
            dy = event.y_root - self.start_y
            self.root.geometry(f"+{self.root.winfo_x()+dx}+{self.root.winfo_y()+dy}")
            self.start_x = event.x_root
            self.start_y = event.y_root
        elif self.resizing:
            # 调整窗口大小
            new_width = max(100, self.width + (event.x_root - self.start_x))
            new_height = max(50, self.height + (event.y_root - self.start_y))
            self.width = new_width
            self.height = new_height
            self.root.geometry(f"{new_width}x{new_height}")
            self.start_x = event.x_root
            self.start_y = event.y_root
            self._draw_stroked_text(self.canvas.itemcget(self.text_item, 'text'))

    def init_context_menu(self):
        """ 初始化右键菜单 """
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="修改文字颜色", command=self.change_color)
        self.menu.add_checkbutton(
            label="窗口置顶",
            command=self.toggle_topmost,
            variable=tk.BooleanVar(value=True)
        )
        self.menu.add_separator()
        self.menu.add_command(label="关闭窗口", command=self.close)

    def show_menu(self, event):
        """ 显示右键菜单 """
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def change_color(self):
        """ 修改文字颜色 """
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color
            self._draw_stroked_text(self.canvas.itemcget(self.text_item, 'text'))

    def toggle_topmost(self):
        """ 切换置顶状态 """
        current = self.root.attributes('-topmost')
        self.root.attributes('-topmost', not current)

    def close(self, event=None):
        """ 安全关闭窗口 """
        if messagebox.askokcancel("关闭", "确认要关闭悬浮窗吗？"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    # 创建消息队列
    msg_queue = queue.Queue()
    
    # 启动悬浮窗线程
    def run_overlay():
        app = UltimateOverlay(msg_queue)
        app.run()
    
    overlay_thread = threading.Thread(target=run_overlay, daemon=True)
    overlay_thread.start()

    # 示例：从主线程发送消息
    import time

       
    i=1
    # 保持主线程运行
    while True:
        time.sleep(1)
        msg_queue.put(f"消息更新 {'a'*i*5}/5")
        i+=1
