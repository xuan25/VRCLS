import unicodedata
import openvr
import time,os,math,sys,ctypes
from PIL import Image, ImageDraw, ImageFont
import psutil
from collections import deque
class BoundedQueue:
    def __init__(self, max_size=3):
        self.queue = deque(maxlen=max_size)
    
    def enqueue(self, item):
        if not isinstance(item, str):
            raise ValueError("Only strings can be enqueued")
        self.queue.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        else:
            raise IndexError("Dequeue from an empty queue")
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def __repr__(self):
        return f"BoundedQueue({list(self.queue)})"
    

class VRTextOverlay:
    def __init__(self, text="          欢迎使用VRCLS           \n    桌面音频捕捉的文字将显示在此处", font_size=40):
        self.overlay = None
        self.textList=BoundedQueue()
        self.text = text
        self.font_size = font_size
        self.vr_system = None
        self.overlay_handle = None
        self.texture_handle = None
        # self.font_manger=FontManager()
        self.fontPath=os.path.join(sys._MEIPASS,"font","gnuunifontfull-pm9p.ttf") if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"font","gnuunifontfull-pm9p.ttf")
    def is_steamvr_running(self):
        # 遍历所有正在运行的进程
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # 检查进程名称是否为 'vrserver.exe'
                if proc.info['name'] == 'vrserver.exe':
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def initialize(self,logger,params, hand=0):
        # 等待SteamVR启动
        ready=False
        once=True
        
        while True:
            if self.is_steamvr_running():
                # 尝试初始化OpenVR
                self.vr_system = openvr.init(openvr.VRApplication_Overlay)
                time.sleep(5)
                break
            else:
                if once:
                    logger.put({"text":"等待SteamVR启动...","level":"warning"})
                    once=False
                time.sleep(5)
        logger.put({"text":"已检测到SteamVR正在运行","level":"info"})
        # 初始化Overlay系统
        self.overlay = openvr.IVROverlay()
        
        # 等待手柄检测（最长等待180秒）
        target_role = openvr.TrackedControllerRole_LeftHand if hand == 1 else openvr.TrackedControllerRole_RightHand
        HAND_CHECK_INTERVAL = 3  # 秒
        MAX_RETRIES = 180
        once=True
        for _ in range(MAX_RETRIES):
            hand_index = self.vr_system.getTrackedDeviceIndexForControllerRole(target_role)
            if hand_index != openvr.k_unTrackedDeviceIndexInvalid:
                ready=True
                time.sleep(3)
                break
            if once:
                logger.put({"text":f"等待{'左手柄' if hand ==1 else '右手柄'}连接...","level":"info"})
                once=False
            time.sleep(HAND_CHECK_INTERVAL)
        else:
            logger.put({"text":"手柄检测超时，请确认手柄已连接并激活,SteamVR线程退出",'level':'warning'})
        
        # 创建Overlay（带时间戳保证唯一性）
        overlay_key = f"python.vroverlay.example.{time.time()}"
        overlay_name = f"Python VR Overlay.{time.time()}"
        self.overlay_handle = self.overlay.createOverlay(overlay_key, overlay_name)
        
        # 设置到指定手柄
        if ready:
            self.set_overlay_to_hand(hand)
            params["steamReady"] = True
            return True
        return False


    def set_overlay_position(self, position):
        if self.overlay_handle:
            transform = openvr.HmdMatrix34_t()
            transform[0][3] = position[0]  # X
            transform[1][3] = position[1]  # Y
            transform[2][3] = position[2]  # Z
            transform[0][0] = transform[1][1] = transform[2][2] = 1.0  # 单位矩阵
            openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(
                self.overlay_handle,
                openvr.k_unTrackedDeviceIndex_Hmd,
                transform
            )

    def update_text(self, new_text):
        self.format_string(new_text)
        self._create_text_texture()
    # def format_string(self,s, max_length=20):
    #     paragraphs = s.split('\n')
    #     result = []
    #     for para in paragraphs:
    #         for i in range(0, len(para), max_length):
    #             result.append(para[i:i+max_length])
    #     self.text= '\n'.join(result)
    def format_string(self, s, max_chinese_chars=20):
        from PIL import ImageFont
        import re


        font = ImageFont.truetype(self.fontPath, self.font_size)
        
        # 计算目标行宽（20个中文的像素宽度）
        sample_text = "中" * max_chinese_chars
        target_width = font.getlength(sample_text)
        
        # 按段落处理
        paragraphs = s.split('\n')
        result = []
        
        for para in paragraphs:
            words = []
            # 使用正则表达式分割中英文单词
            for word in re.findall(r'[\u4e00-\u9fff]+|[^\u4e00-\u9fff]+', para):
                # 中文按字符分割，英文按空格分割
                if re.match(r'^[\u4e00-\u9fff]+$', word):
                    words.extend(list(word))
                else:
                    words.extend(word.split(' '))
            
            current_line = []
            current_width = 0
            
            for word in words:
                # 单词可能是空字符串（当有多个空格时）
                if not word:
                    continue
                    
                word_width = font.getlength(word)
                
                # 如果当前行不为空，需要加上空格宽度
                space_width = font.getlength(' ') if current_line else 0
                
                if current_width + space_width + word_width <= target_width:
                    if current_line:
                        current_line.append(' ')
                        current_width += space_width
                    current_line.append(word)
                    current_width += word_width
                else:
                    # 处理当前行对齐
                    self._justify_line(current_line, current_width, target_width, font, result)
                    
                    # 开始新行
                    current_line = [word]
                    current_width = word_width
            
            # 处理最后一行（左对齐）
            if current_line:
                result.append(''.join(current_line))
        self.textList.enqueue('\n'.join(result))
        self.text = '\n----------------------------------\n'.join(list(self.textList.queue))

    def _justify_line(self, line, line_width, target_width, font, result):
        if not line:
            return
        
        # 计算需要填充的总空间
        total_space = target_width - line_width
        spaces_count = line.count(' ')
        
        # 如果没有空格或最后一行，直接添加
        if spaces_count == 0 or total_space <= 0:
            result.append(''.join(line))
            return
        
        # 计算每个空格需要增加的空间（转换为字符数近似值）
        space_add = total_space / spaces_count
        average_add = round(space_add / font.getlength(' '))
        
        # 重建带额外空格的字符串
        justified = []
        space_used = 0
        for i, char in enumerate(line):
            if char == ' ' and space_used < spaces_count:
                # 添加额外空格
                extra_spaces = min(average_add, spaces_count - space_used)
                justified.append(' ' * (1 + extra_spaces))
                space_used += 1
            else:
                justified.append(char)
        
        result.append(''.join(justified))

    def _create_text_texture(self):
        # 使用PIL创建文字图像
            # 自动检测文字系统
        # font=self.get_font()
        font = ImageFont.truetype(self.fontPath, self.font_size)
        # font = ImageFont.truetype("simhei.ttf", self.font_size)
        
        # 创建临时ImageDraw对象用于计算文本尺寸
        temp_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        draw = ImageDraw.Draw(temp_img)
        
        # 使用新的textbbox方法代替getsize
        bbox = draw.textbbox((0, 0), self.text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 创建带边距的实际图像
        img = Image.new("RGBA", (text_width + 20, text_height + 60), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        # 绘制文字（考虑新的坐标系）
        draw.text(
            (10 - bbox[0], 10 - bbox[1]),  # 补偿文本起始偏移
            self.text,
            font=font,
            fill=(255,255,255,255),
            stroke_width=2,
            stroke_fill=(0,0,0,255)
        )
        _img_data = img.tobytes()
        _buffer = (ctypes.c_char * len(_img_data)).from_buffer_copy(_img_data)
        path=os.path.join(sys._MEIPASS, 'tmp_texture.png') if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(__file__), 'tmp_texture.png')
        img.save(path)  # 添加在tobytes()之前

        # openvr.VROverlay().setOverlayFromFile(self.overlay_handle,path)
        openvr.VROverlay().setOverlayRaw(self.overlay_handle, _buffer, text_width + 20, text_height + 60, 4)
        

    def set_overlay_to_hand(self, hand=0):
        """设置Overlay到手上
        hand: 0-右手，1-左手"""
        device_index = openvr.k_unTrackedDeviceIndex_Hmd
        # 查找控制器设备
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            device_class = self.vr_system.getTrackedDeviceClass(i)
            if device_class == openvr.TrackedDeviceClass_Controller:
                role = self.vr_system.getControllerRoleForTrackedDeviceIndex(i)
                if (hand == 0 and role == openvr.TrackedControllerRole_RightHand) or \
                (hand == 1 and role == openvr.TrackedControllerRole_LeftHand):
                    device_index = i
                    break
                # 创建3D变换矩阵
        transform = openvr.HmdMatrix34_t()
        # ===== 位置调整 =====
        # 单位：米（相对于控制器坐标系）
        transform[0][3] = -0.03 if hand==0 else 0.03  # X轴：右(+) 左(-) 
        transform[1][3] = -0.04  # Y轴：上(+) 下(-)
        transform[2][3] = 0.06   # Z轴：前(+) 后(-)
        
        # ===== 旋转调整 =====
        # 需要同时调整三个轴的旋转量（单位：弧度）
        if hand==1:
            x_rot = math.radians(-90)  # X轴旋转（上下倾斜）
            y_rot = math.radians(30)    # Y轴旋转（左右转动）
            z_rot = math.radians(-90)   # Z轴旋转（平面方向）
        else:
            x_rot = math.radians(-90)  # X轴旋转（上下倾斜）
            y_rot = math.radians(-30)    # Y轴旋转（左右转动）
            z_rot = math.radians(90)   # Z轴旋转（平面方向）
        # 构建旋转矩阵（使用欧拉角转旋转矩阵）
        cosX = math.cos(x_rot)
        sinX = math.sin(x_rot)
        cosY = math.cos(y_rot)
        sinY = math.sin(y_rot)
        cosZ = math.cos(z_rot)
        sinZ = math.sin(z_rot)
        
        # 旋转矩阵计算（ZYX顺序）
        transform[0][0] = cosZ * cosY
        transform[0][1] = cosZ * sinY * sinX - sinZ * cosX
        transform[0][2] = cosZ * sinY * cosX + sinZ * sinX
        
        transform[1][0] = sinZ * cosY
        transform[1][1] = sinZ * sinY * sinX + cosZ * cosX
        transform[1][2] = sinZ * sinY * cosX - cosZ * sinX
        
        transform[2][0] = -sinY
        transform[2][1] = cosY * sinX
        transform[2][2] = cosY * cosX
        openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(
            self.overlay_handle,
            device_index,
            transform
        )
    def run(self):
        try:
            self.initialize(0)
            self._create_text_texture()
            self.overlay.setOverlayWidthInMeters(self.overlay_handle,0.15)
            self.overlay.showOverlay(self.overlay_handle)
            time.sleep(5)
            count=0
            while True:
                        
                self.update_text(f" loop:{count}\n"+"""windows官方中文字库安装-中文-字体分类-发现字体-求字体网""")
                count+=1
                time.sleep(2)
        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:  # 确保始终执行清理
            if self.overlay_handle:
                self.overlay.hideOverlay(self.overlay_handle)
                self.overlay.destroyOverlay(self.overlay_handle)
            openvr.shutdown()
            time.sleep(5)


if __name__ == "__main__":

        overlay = VRTextOverlay()
        overlay.run()
    # import openvr
    # from..module.steamvr import VRTextOverlay
    # from multiprocessing
    # textOverlay=VRTextOverlay()
    # try:
    #     textOverlay.initialize(0)
    #     textOverlay._create_text_texture()
    #     textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle,0.15)
    #     textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
    #     print({"text":f"手腕显示启动完毕","level":"info"})
    #     while True:
    #         if queue.empty():
    #             time.sleep(0.5)
    #             continue
            
    #         text=queue.get() 
    #         textOverlay.update_text(text)
    #         time.sleep(1)
    # except Exception as e:
    #     logger.put({"text":f"发生错误: {str(e)}","level":"error"})
    # finally:  # 确保始终执行清理
    #     if textOverlay.overlay_handle:
    #         textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
    #         textOverlay.overlay.destroyOverlay(textOverlay.overlay_handle)
    #     openvr.shutdown()
    #     time.sleep(1)
