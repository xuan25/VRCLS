import openvr
import time
import os
import math
import sys
import ctypes
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
    def __init__(self, text="欢迎使用VR交互系统", font_size=40):
        self.overlay = None
        self.textList = BoundedQueue()
        self.text = text
        self.font_size = font_size
        self.vr_system = None
        self.overlay_handle = None
        self.button_overlay = None
        self.button_callback = None
        self.logger = None
        self.fontPath = self._get_font_path()
        self.last_trigger_state = False

    def _get_font_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_path, "font", "gnuunifontfull-pm9p.ttf")

    def is_steamvr_running(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == 'vrserver.exe':
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def initialize(self, logger, params, hand=0):
        while not self.is_steamvr_running():
            time.sleep(5)
        
        self.vr_system = openvr.init(openvr.VRApplication_Overlay)
        self.overlay = openvr.IVROverlay()
        logger.put({"text":"SteamVR已初始化", "level":"info"})

        # 创建主文本覆盖层
        overlay_key = f"python.text_overlay.{time.time()}"
        self.overlay_handle = self.overlay.createOverlay(overlay_key, "TextOverlay")
        
        # 创建按钮覆盖层
        btn_key = f"python.button_overlay.{time.time()}"
        self.button_overlay = self.overlay.createOverlay(btn_key, "VRButton")
        self._create_button_texture("点击交互")
        
        self.set_overlay_to_hand(hand)
        self._create_text_texture()
        self.overlay.showOverlay(self.overlay_handle)
        self.overlay.showOverlay(self.button_overlay)
        return True

    def _create_button_texture(self, text):
        """创建按钮纹理（带按压效果）"""
        font = ImageFont.truetype(self.fontPath, 30)
        size = (300, 100)
        
        # 正常状态
        img_normal = Image.new("RGBA", size, (40, 40, 40, 200))
        draw = ImageDraw.Draw(img_normal)
        draw.rounded_rectangle([(5,5), (295,95)], 15, fill=(80,80,80,255))
        text_bbox = draw.textbbox((0,0), text, font=font)
        text_pos = ((size[0] - (text_bbox[2]-text_bbox[0]))//2, 
                   (size[1] - (text_bbox[3]-text_bbox[1]))//2)
        draw.text(text_pos, text, font=font, fill=(255,255,255))
        
        # 按压状态
        img_pressed = Image.new("RGBA", size, (40, 40, 40, 200))
        draw = ImageDraw.Draw(img_pressed)
        draw.rounded_rectangle([(5,5), (295,95)], 15, fill=(120,120,120,255))
        draw.text(text_pos, text, font=font, fill=(200,200,200))
        
        # 保存两种状态
        self.btn_textures = {
            'normal': self._image_to_buffer(img_normal),
            'pressed': self._image_to_buffer(img_pressed)
        }
        self.overlay.setOverlayRaw(self.button_overlay, *self.btn_textures['normal'])

    def _image_to_buffer(self, img):
        """将PIL图像转换为OpenVR需要的格式"""
        return (
            (ctypes.c_char * len(img.tobytes())).from_buffer_copy(img.tobytes()),
            img.width,
            img.height,
            4
        )

    def set_overlay_position(self, overlay_handle, position, rotation=(0,0,0)):
        """设置覆盖层3D位置"""
        transform = openvr.HmdMatrix34_t()
        
        # 位置
        transform[0][3] = position[0]
        transform[1][3] = position[1]
        transform[2][3] = position[2]
        
        # 旋转（欧拉角转旋转矩阵）
        cos = [math.cos(r) for r in rotation]
        sin = [math.sin(r) for r in rotation]
        
        transform[0][0] = cos[1]*cos[2]
        transform[0][1] = cos[2]*sin[0]*sin[1] - cos[0]*sin[2]
        transform[0][2] = cos[0]*cos[2]*sin[1] + sin[0]*sin[2]
        
        transform[1][0] = cos[1]*sin[2]
        transform[1][1] = cos[0]*cos[2] + sin[0]*sin[1]*sin[2] 
        transform[1][2] = -cos[2]*sin[0] + cos[0]*sin[1]*sin[2]
        
        transform[2][0] = -sin[1]
        transform[2][1] = cos[1]*sin[0]
        transform[2][2] = cos[0]*cos[1]

        self.overlay.setOverlayTransformAbsolute(
            overlay_handle,
            openvr.TrackingUniverseStanding,
            transform
        )

    def _check_controller_input(self):
        """正确的控制器状态检测方法"""
        for device_idx in range(openvr.k_unMaxTrackedDeviceCount):
            if self.vr_system.getTrackedDeviceClass(device_idx) != openvr.TrackedDeviceClass_Controller:
                continue
            
            success,state = self.vr_system.getControllerState(device_idx)
            
            if success:
                # 检测扳机键（使用正确的按钮掩码）
                trigger_pressed = (state.ulButtonPressed & (1 << openvr.k_EButton_SteamVR_Trigger)) != 0
                
                # 状态变化检测
                if trigger_pressed and not self.last_trigger_state:
                    if self._check_button_intersection(device_idx):
                        self._handle_button_press()
                
                self.last_trigger_state = trigger_pressed
    def _check_button_intersection(self, controller_idx):
        """精确的按钮碰撞检测（修正版本）"""
        try:
            # 获取控制器状态和姿态（正确解包三元组）
            result, state, tracked_pose = self.vr_system.getControllerStateWithPose(
                openvr.TrackingUniverseStanding,
                controller_idx
            )
            
            # 检查是否成功获取数据
            if result != 0:  # 假设0表示成功
                return False
                
            # 获取控制器姿态矩阵
            if not tracked_pose.bPoseIsValid:
                return False
                
            matrix = tracked_pose.mDeviceToAbsoluteTracking
            controller_pos = [matrix[i][3] for i in range(3)]
            forward_dir = [matrix[i][2] for i in range(3)]  # Z轴方向

            # 获取按钮位置信息
            overlay_pose = openvr.HmdMatrix34_t()
            self.overlay.getOverlayTransformAbsolute(
                self.button_overlay,
                openvr.TrackingUniverseStanding,
                overlay_pose
            )
            btn_pos = [overlay_pose[i][3] for i in range(3)]
            
            # 计算射线方向（单位向量）
            ray_length = 2.0  # 最大检测距离2米
            ray_end = [
                controller_pos[0] + forward_dir[0] * ray_length,
                controller_pos[1] + forward_dir[1] * ray_length,
                controller_pos[2] + forward_dir[2] * ray_length
            ]

            # 定义按钮平面（使用按钮的变换矩阵）
            btn_normal = [overlay_pose[i][2] for i in range(3)]  # 使用按钮的Z轴方向作为法线
            btn_plane = (
                btn_pos[0], btn_pos[1], btn_pos[2],  # 平面点
                btn_normal[0], btn_normal[1], btn_normal[2]  # 法线方向
            )

            # 计算射线与平面的交点
            intersect = self._ray_plane_intersection(
                (controller_pos[0], controller_pos[1], controller_pos[2]),
                (ray_end[0], ray_end[1], ray_end[2]),
                btn_plane
            )
            
            if intersect is None:
                return False

            # 将交点转换到按钮的局部坐标系
            btn_matrix = overlay_pose
            local_x = sum((intersect[i] - btn_pos[i]) * btn_matrix[j][0] for i, j in enumerate([0,1,2]))
            local_y = sum((intersect[i] - btn_pos[i]) * btn_matrix[j][1] for i, j in enumerate([0,1,2]))
            
            # 按钮尺寸检测（假设0.3x0.15米）
            btn_width = 0.3
            btn_height = 0.15
            return (
                abs(local_x) < btn_width/2 and 
                abs(local_y) < btn_height/2
            )

        except Exception as e:
            print(f"碰撞检测错误: {str(e)}")
            return False

    def _ray_plane_intersection(self, ray_start, ray_end, plane):
        """
        计算射线与平面的交点
        plane格式：(px, py, pz, nx, ny, nz)
        """
        # 解包平面参数
        px, py, pz, nx, ny, nz = plane
        ray_dir = (
            ray_end[0] - ray_start[0],
            ray_end[1] - ray_start[1],
            ray_end[2] - ray_start[2]
        )
        
        denominator = nx * ray_dir[0] + ny * ray_dir[1] + nz * ray_dir[2]
        if abs(denominator) < 1e-6:
            return None  # 射线与平面平行
        
        t = (nx*(px - ray_start[0]) + ny*(py - ray_start[1]) + nz*(pz - ray_start[2])) / denominator
        if t < 0 or t > 1:
            return None  # 交点不在射线范围内
        
        return (
            ray_start[0] + ray_dir[0] * t,
            ray_start[1] + ray_dir[1] * t,
            ray_start[2] + ray_dir[2] * t
        )


    def set_button_callback(self, callback):
        self.button_callback = callback

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
        try:
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

        except Exception as e:
            self.logger.put({"text":f"Error setting overlay text {str(e)}","level":"error"})
            return False

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
            class DummyLogger:
                def put(self, msg):
                    print(f"[{msg['level'].upper()}] {msg['text']}")
            
            self.initialize(DummyLogger(), {}, hand=0)
            
            # 设置按钮位置（HMD正前方0.5米）
            self.set_overlay_position(
                self.button_overlay,
                position=(0, -0.1, -0.5),  # X, Y, Z
                rotation=(math.radians(-30), 0, 0)  # 轻微倾斜
            )
            
            # 设置按钮回调
            self.set_button_callback(lambda: self.update_text("按钮被点击!"))
            
            # 主循环
            while True:
                self._check_controller_input()
                time.sleep(0.05)
                
        except Exception as e:
            print(f"错误发生: {str(e)}")
        finally:
            self.overlay.destroyOverlay(self.overlay_handle)
            self.overlay.destroyOverlay(self.button_overlay)
            openvr.shutdown()

if __name__ == "__main__":
    vr_app = VRTextOverlay()
    vr_app.run()
