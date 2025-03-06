import openxr as xr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from OpenGL import GL as gl
import glfw

# 初始化glfw（仅用于OpenGL上下文）
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(1, 1, "hidden", None, None)
glfw.make_context_current(window)

# OpenXR初始化
instance = xr.create_instance(
    xr.InstanceCreateInfo(
        enabled_extension_names=[
            xr.KHR_OPENGL_ENABLE_EXTENSION_NAME,
            xr.KHR_COMPOSITION_LAYER_QUAD_EXTENSION_NAME
        ]
    )
)

system_id = instance.get_system(xr.SystemGetInfo(xr.FormFactor.HEAD_MOUNTED_DISPLAY))
session = instance.create_session(
    xr.SessionCreateInfo(
        system_id=system_id,
        graphics_binding=xr.GraphicsBindingOpenGLWin32KHR()
    )
)

# 创建参考空间
view_space = session.create_reference_space(xr.ReferenceSpaceCreateInfo(
    reference_space_type=xr.ReferenceSpaceType.LOCAL,
    pose_in_reference_space=xr.Posef()
))

# 创建交换链
swapchain = session.create_swapchain(
    xr.SwapchainCreateInfo(
        width=1024,
        height=1024,
        format=gl.GL_RGBA8,
        array_size=1,
        mip_count=1,
        sample_count=1,
        usage_flags=xr.SwapchainUsageFlag.SAMPLED_BIT
    )
)

# 生成文字纹理
def create_text_texture(text):
    image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 120)
    draw.text((100, 100), text, fill=(255, 255, 255, 255), font=font)
    return np.array(image)

# 创建OpenGL纹理
texture_id = gl.glGenTextures(1)
gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
text_data = create_text_texture("Hello SteamVR!")
gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, 1024, 1024, 0, 
                gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, text_data)

# 主渲染循环
while True:
    session.wait_frame()
    frame_state = session.begin_frame()
    
    # 获取右手手柄位置
    hand_pose = xr.SpaceLocations()
    view_space.locate_space(session.get_action_poses([xr.Path("/user/hand/right")])[0].pose, 
                           frame_state.predicted_display_time, hand_pose)
    
    # 创建Quad图层
    quad_layer = xr.CompositionLayerQuad(
        space=view_space,
        sub_image=xr.SwapchainSubImage(swapchain=swapchain),
        eye_visibility=xr.EyeVisibility.BOTH,
        pose=hand_pose.pose,
        size=(0.3, 0.3)  # 30cm x 30cm
    )
    
    session.end_frame(xr.FrameEndInfo(
        layers=[quad_layer]
    ))
