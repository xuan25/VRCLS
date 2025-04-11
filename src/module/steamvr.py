import openvr
import time,os,math,sys,ctypes
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import win32com.client
class BoundedQueue:
    def __init__(self, max_size=5):
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
    def __init__(self, text="", font_size=40):
        self.wmi=win32com.client.GetObject('winmgmts:')
        self.overlay = None
        self.textList_L=BoundedQueue()
        self.textList_R=BoundedQueue()
        self.text = text
        self.text_L = "                 桌面音频\n----------------------------------------------\n"
        self.text_R = "                  麦克风\n----------------------------------------------\n"
        self.font_size = font_size
        self.vr_system = None
        self.overlay_handle = None#右手
        self.overlay_handle_1 = None
        self.texture_handle = None
        self.logger=None
        self.fontPath=os.path.join(sys._MEIPASS,"font","gnuunifontfull-pm9p.ttf") if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"font","gnuunifontfull-pm9p.ttf")
    def is_steamvr_running(self):

        # 构建精确查询（比遍历进程快10倍以上）
        query = "SELECT * FROM Win32_Process WHERE Name = 'vrserver.exe'"
        processes = self.wmi.ExecQuery(query)
        if not processes or len(processes)==0 : return False
        else : return True

    # 等待手柄检测（最长等待180秒）
    def check_Controller(self,logger,hand):
        target_role = openvr.TrackedControllerRole_LeftHand if hand == 1 else openvr.TrackedControllerRole_RightHand
        HAND_CHECK_INTERVAL = 3  # 秒
        MAX_RETRIES = 180
        once=True
        for _ in range(MAX_RETRIES):
            hand_index = self.vr_system.getTrackedDeviceIndexForControllerRole(target_role)
            if hand_index != openvr.k_unTrackedDeviceIndexInvalid: 
                time.sleep(3)
                return True
            if once:
                logger.put({"text":f"等待{'左手柄' if hand ==1 else '右手柄'}连接...","level":"info"})
                once=False
            time.sleep(HAND_CHECK_INTERVAL)
        else:
            logger.put({"text":"手柄检测超时，请确认手柄已连接并激活,SteamVR线程退出",'level':'warning'})
            return False
        
        
    def initialize(self,logger,params):
        self.params=params
        # 等待SteamVR启动
        hand=params["config"].get("SteamVRHad")
        ready=False
        once=True
        self.logger=logger
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
        
        if params["config"].get("SteamVRHad") ==2:
            ready=self.check_Controller(logger,0) and self.check_Controller(logger,0)
            if ready:
                # 创建Overlay（带时间戳保证唯一性）
                overlay_key = f"python.vroverlay.example.{time.time()}"
                overlay_name = f"Python VR Overlay.{time.time()}"
                overlay_key_1 = f"python.vroverlay.example1.{time.time()}"
                overlay_name_1 = f"Python VR Overlay1.{time.time()}"
                self.overlay_handle = self.overlay.createOverlay(overlay_key, overlay_name)
                self.overlay_handle_1 = self.overlay.createOverlay(overlay_key_1, overlay_name_1)
            
                self.set_overlay_to_hand(0)
                self.set_overlay_to_hand(1,True)
                params["steamReady"] = True
                return True
            return False
        else:
        
            ready=self.check_Controller(logger,hand)
            if ready:
                # 创建Overlay（带时间戳保证唯一性）
                overlay_key = f"python.vroverlay.example.{time.time()}"
                overlay_name = f"Python VR Overlay.{time.time()}"
                self.overlay_handle = self.overlay.createOverlay(overlay_key, overlay_name)
            
            # 设置到指定手柄
            
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
            # self.textList.enqueue('\n'.join(result))
            if s.startswith("麦克风"):
                self.textList_R.enqueue('\n'.join(result))
                self.text_R =  f'                    麦克风\n----------------------------------------------\n'+'\n----------------------------------\n'.join(list(self.textList_R.queue))
            else : 
                self.textList_L.enqueue('\n'.join(result))
                self.text_L =  f'                   桌面音频\n----------------------------------------------\n'+'\n----------------------------------\n'.join(list(self.textList_L.queue))

            

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

    def _draw_one_texture(self,text):
        font = ImageFont.truetype(self.fontPath, self.font_size)
        # font = ImageFont.truetype("simhei.ttf", self.font_size)

        # 创建临时ImageDraw对象用于计算文本尺寸 
        temp_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        draw = ImageDraw.Draw(temp_img)
        
        # 使用新的textbbox方法代替getsize
        bbox = draw.textbbox((0, 0), text, font=font,stroke_width=2)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 创建带边距的实际图像
        img = Image.new("RGBA", (text_width + 20, text_height + 20), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        # 绘制文字（考虑新的坐标系）
        draw.text(
            (10-bbox[0], 10-bbox[1]),  # 补偿文本起始偏移
            text,
            font=font,
            fill=(255,255,255,255),
            stroke_width=2,
            stroke_fill=(0,0,0,255)
        )
        return img

    def _create_text_texture(self,alignment='top'):
            onlyMic = self.params["config"].get("Separate_Self_Game_Mic")==0
            mode=self.params["config"].get("SteamVRHad")==2
            img_R=self._draw_one_texture(self.text_R)
            _img_data = img_R.tobytes()
            _buffer = (ctypes.c_char * len(_img_data)).from_buffer_copy(_img_data)
            path=os.path.join(sys._MEIPASS, 'tmp_texture.png') if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(__file__), 'tmp_texture.png')
            img_R.save(path)
            width, height = img_R.size
            openvr.VROverlay().setOverlayRaw(self.overlay_handle, _buffer, width, height, 4)
            if mode and not onlyMic:
                
                img_L=self._draw_one_texture(self.text_L)
                _img_data_L = img_L.tobytes()
                _buffer_L = (ctypes.c_char * len(_img_data_L)).from_buffer_copy(_img_data_L)
                path=os.path.join(sys._MEIPASS, 'tmp_texture_1.png') if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(__file__), 'tmp_texture_1.png')
                img_L.save(path)
                width, height = img_L.size
                openvr.VROverlay().setOverlayRaw(self.overlay_handle_1, _buffer_L, width, height, 4)
                return

            if onlyMic:return
            img_L=self._draw_one_texture(self.text_L)

             # 获取图片尺寸
            w1, h1 = img_L.size
            w2, h2 = img_R.size

            # 计算新图片尺寸
            total_width = w1 + w2
            max_height = max(h1, h2)

            # 创建新画布（白色背景）
            combined = Image.new('RGBA', (total_width, max_height), (0,0,0,0))

            # 粘贴第一张图片（左侧固定）
            combined.paste(img_R, (0, 0))

            # 计算第二张图片垂直位置
            if alignment == 'top':
                y = 0
            elif alignment == 'bottom':
                y = max_height - h2
            else:  # 默认居中
                y = (max_height - h2) // 2

            # 粘贴第二张图片（右侧）
            combined.paste(img_L, (w1, y))

            _img_data = combined.tobytes()
            _buffer = (ctypes.c_char * len(_img_data)).from_buffer_copy(_img_data)
            path=os.path.join(sys._MEIPASS, 'tmp_texture.png') if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(__file__), 'tmp_texture.png')
            combined.save(path)  # 添加在tobytes()之前

            # openvr.VROverlay().setOverlayFromFile(self.overlay_handle,path)
            openvr.VROverlay().setOverlayRaw(self.overlay_handle, _buffer, total_width, max_height, 4)

        # except Exception as e:
        #     self.logger.put({"text":f"Error setting overlay text {str(e)}","level":"error"})
        #     return False
    

    def get_controller_index(self):
        """更可靠的控制器索引获取方法"""
        try:
            system = openvr.VRSystem()
            for i in range(openvr.k_unMaxTrackedDeviceCount):
                if system.getTrackedDeviceClass(i) == openvr.TrackedDeviceClass_Controller:
                    role = system.getControllerRoleForTrackedDeviceIndex(i)
                    if (self.hand == 0 and role == openvr.TrackedControllerRole_RightHand) or \
                       (self.hand == 1 and role == openvr.TrackedControllerRole_LeftHand):
                        return i
            return openvr.k_unTrackedDeviceIndexInvalid
        except:
            return openvr.k_unTrackedDeviceIndexInvalid
    def set_overlay_to_hand(self, hand=0,is_1=False):
        """设置Overlay到手上
        hand: 0-右手，1-左手"""
        self.hand = hand  # 记录当前手柄类型
        device_index = self.get_controller_index()
        
        if device_index == openvr.k_unTrackedDeviceIndexInvalid:
            return False  # 明确返回状态

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
        # openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(
        #     self.overlay_handle,
        #     device_index,
        #     transform
        # )
        try:
            self.overlay.setOverlayTransformTrackedDeviceRelative(
                self.overlay_handle_1 if is_1 else self.overlay_handle,
                device_index,
                transform
            )
            return True
        except:
            return False
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
    # 在现有代码基础上添加
    def refresh_overlay(self):
        """强制刷新Overlay属性"""
        if self.overlay_handle:
            self.overlay.setOverlayWidthInMeters(self.overlay_handle, 0.15)
            self.overlay.setOverlayAlpha(self.overlay_handle, 1.0)
            self.overlay.setOverlayColor(self.overlay_handle, 1.0, 1.0, 1.0)
            
    def health_check(self):
        """系统健康检查"""
        try:
            return self.vr_system.isTrackedDeviceConnected(
                self.vr_system.getTrackedDeviceIndexForControllerRole(
                    openvr.TrackedControllerRole_LeftHand if self.hand == 1 
                    else openvr.TrackedControllerRole_RightHand
                )
            )
        except:
            return False

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
