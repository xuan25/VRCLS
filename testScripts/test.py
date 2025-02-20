import openvr
import time,os
from PIL import Image, ImageDraw, ImageFont

class VRTextOverlay:
    def __init__(self, text="Hello SteamVR", font_size=40):
        self.overlay = None
        self.text = text
        self.font_size = font_size
        self.vr_system = None
        self.overlay_handle = None
        self.texture_handle = None
        
    def initialize(self):
        # 初始化OpenVR
        self.vr_system = openvr.init(openvr.VRApplication_Overlay)
        self.overlay = openvr.IVROverlay()
        # 创建Overlay
        overlay_key = "python.vroverlay.example"+str(time.time())
        overlay_name = "Python VR Overlay"+str(time.time())
        self.overlay_handle = self.overlay.createOverlay(overlay_key, overlay_name)
        # 设置初始位置（HMD前方1米，高度0.5米）
        # self.set_overlay_position([0, 0.4, -1.5])
        self.set_overlay_to_hand(1)

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
        self.text = new_text
        self._create_text_texture()

    def _create_text_texture(self):
        # 使用PIL创建文字图像
        font = ImageFont.truetype("simhei.ttf", self.font_size)
        
        # 创建临时ImageDraw对象用于计算文本尺寸
        temp_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        draw = ImageDraw.Draw(temp_img)
        
        # 使用新的textbbox方法代替getsize
        bbox = draw.textbbox((0, 0), self.text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 创建带边距的实际图像
        img = Image.new("RGBA", (text_width + 20, text_height + 20), (0,0,0,0))
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
        path=os.path.join(os.path.dirname(__file__),'cache', 'debug_texture.png')
        img.save(path)  # 添加在tobytes()之前
        # # 转换为正确的纹理格式
        # img_bytes = img.tobytes()
        # width, height = img.size
        
        # # 创建ctypes缓冲区
        # from ctypes import c_ubyte, cast, POINTER
        # buffer_size = width * height * 4  # RGBA
        # c_buffer = (c_ubyte * buffer_size).from_buffer_copy(img_bytes)
        
        # # 设置纹理数据
        # error = openvr.VROverlay().setOverlayRaw(
        #     self.overlay_handle,
        #     cast(c_buffer, POINTER(c_ubyte)),  # 正确的指针传递方式
        #     width,
        #     height,
        #     4  # 每个像素的字节数（RGBA）
        # )
        openvr.VROverlay().setOverlayFromFile(self.overlay_handle,path)
        
        
        # 设置纹理
        # openvr.VROverlay().setOverlayTexture(self.overlay_handle, self.texture_handle)
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

        # 设置相对位置（控制器前方10cm）
        transform = openvr.HmdMatrix34_t()
        transform[0][3] = 0.0  # X
        transform[1][3] = 0.0  # Y
        transform[2][3] = 0.1  # Z（控制器前方）
        transform[0][0] = transform[1][1] = transform[2][2] = 1.0
        openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(
            self.overlay_handle,
            device_index,
            transform
        )
    # def update_position_with_keyboard(self, speed=0.05):
    #     # 使用WASD调整位置
    #     keys = self.vr_system.getKeyboardState()
        
    #     # 获取当前变换矩阵
    #     transform = openvr.HmdMatrix34_t()
    #     openvr.VROverlay().getOverlayTransformTrackedDeviceRelative(
    #         self.overlay_handle,
    #         openvr.k_unTrackedDeviceIndex_Hmd,
    #         transform
    #     )
        
    #     # 调整位置
    #     if keys[ord('W')]:
    #         transform[2][3] -= speed  # 向前
    #     if keys[ord('S')]:
    #         transform[2][3] += speed  # 向后
    #     if keys[ord('A')]:
    #         transform[0][3] -= speed  # 向左
    #     if keys[ord('D')]:
    #         transform[0][3] += speed  # 向右
    #     if keys[ord('Q')]:
    #         transform[1][3] += speed  # 向上
    #     if keys[ord('E')]:
    #         transform[1][3] -= speed  # 向下

    #     # 设置新位置
    #     openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(
    #         self.overlay_handle,
    #         openvr.k_unTrackedDeviceIndex_Hmd,
    #         transform
    #     )
    # def run(self):
    #     try:
    #         self.initialize()
    #         self._create_text_texture()
            
    #         # 显示Overlay
    #         openvr.VROverlay().showOverlay(self.overlay_handle)
    #                 # 初始化控制器绑定状态
    #         bound_to_hand = False
    #         current_hand = 1  # 0=右手，1=左手
    #         count=0
    #         # 保持程序运行
    #         while True:
    #             self.update_text(f"Python VR Overlay\nHello SteamVR! \n loop:{count}")
    #             count+=1
    #             time.sleep(1)
                
    #     except KeyboardInterrupt:
    #         openvr.VROverlay().destroyOverlay(self.overlay_handle)
    #         openvr.shutdown()
    def run(self):
        try:
            self.initialize()
            self._create_text_texture()
            self.overlay.setOverlayWidthInMeters(self.overlay_handle,0.1)
            self.overlay.showOverlay(self.overlay_handle)
            
            # 初始化控制器绑定状态
            bound_to_hand = False
            current_hand = 1  # 0=右手，1=左手
            count=0
            while True:
                # # 处理键盘输入
                # # self.update_position_with_keyboard()
                
                # # 处理控制器按钮事件
                # # if self.check_controller_input():
                #     # 按菜单键切换绑定状态
                # if not bound_to_hand:
                #     self.set_overlay_to_hand(current_hand)
                #     bound_to_hand = True
                # # else:
                # #     current_hand = 1 - current_hand  # 切换左右手
                # #     self.set_overlay_to_hand(current_hand)
                        
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


if __name__ == "__main__":

        overlay = VRTextOverlay("Python VR Overlay\nHello SteamVR!", 20)
        overlay.run()
