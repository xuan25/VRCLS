import os
import sys

def import_ffmpeg(logger=None):
    # 在所有导入之前加载预配置

    sys.path.insert(0, os.path.dirname(__file__))  # 确保能正确导入core模块

    # 必须在所有pydub相关导入前调用！
    preconfigure_ffmpeg(logger)
    from pydub import AudioSegment
    return AudioSegment


# def set_ffmpeg_path():
#     """动态设置FFmpeg路径（兼容开发环境和PyInstaller打包）"""
#     # 判断是否在打包后的环境中运行
#     if getattr(sys, 'frozen', False):
#         # 打包后：资源在临时目录的根层级
#         base_dir = sys._MEIPASS
#     else:
#         # 开发环境：根据startup.py的位置推导项目根目录
#         # startup.py路径：项目目录/src/core/startup.py → 上溯3级到项目根目录
#         current_file_dir = os.path.dirname(os.path.abspath(__file__))
#         base_dir = os.path.dirname(os.path.dirname(current_file_dir))
    
#     # 构建FFmpeg完整路径
#     ffmpeg_bin_dir = os.path.join(base_dir, "ffmpeg", "bin")
#     ffmpeg_path = os.path.join(ffmpeg_bin_dir, "ffmpeg.exe")
#     ffprobe_path = os.path.join(ffmpeg_bin_dir, "ffprobe.exe")

#     # 验证路径有效性
#     if not os.path.isfile(ffmpeg_path):
#         raise FileNotFoundError(f"FFmpeg未找到于：{ffmpeg_path}")
#     if not os.path.isfile(ffprobe_path):
#         raise FileNotFoundError(f"FFprobe未找到于：{ffprobe_path}")

#     # 设置路径（关键步骤）
#     AudioSegment.converter = ffmpeg_path
#     AudioSegment.ffprobe = ffprobe_path

#     # 调试输出（完成后可删除）
#     # print(f"[DEBUG] FFmpeg路径已设置为：{AudioSegment.converter}")
def suppress_pydub_warnings():
    import warnings
    import pydub.utils
    """在导入pydub前预配置环境"""
    # 动态计算项目根目录
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))  # 适配 src/core 的层级
    
    # 添加ffmpeg到系统PATH（关键！）
    ffmpeg_bin = os.path.join(base_dir, "ffmpeg", "bin")
    os.environ['PATH'] = ffmpeg_bin + os.pathsep + os.environ.get('PATH', '')
    
    # 直接设置pydub配置变量（绕过后续检查）
    sys.modules['pydub.utils'].which = lambda _: ffmpeg_bin  # 猴子补丁
    
    # 过滤特定警告
    warnings.filterwarnings("ignore", 
        message="Couldn't find ffmpeg or avconv",
        category=RuntimeWarning,
        module='pydub.utils'
    )


def preconfigure_ffmpeg(logger=None):
    import warnings
    """终极前置配置（主进程和每个子进程都必须调用）"""
    # 1. 过滤警告（最外层防护）
    warnings.filterwarnings("ignore", 
        message="Couldn't find ffmpeg or avconv",
        category=RuntimeWarning,
        module='pydub.utils'
    )
    
    # 2. 动态路径注入（核心防护）
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))  # 适配 src/core 的层级
    
    ffmpeg_bin = os.path.join(base_dir, "ffmpeg", "bin")
    os.environ['PATH'] = ffmpeg_bin + os.pathsep + os.environ['PATH']
    
    # 3. 猴子补丁（最终防护）
    if 'pydub.utils' in sys.modules:
        import pydub.utils
        pydub.utils.which = lambda cmd: os.path.join(ffmpeg_bin, cmd + ('.exe' if sys.platform == 'win32' else ''))
    
    # 验证路径（可选）
    if logger:logger.put({"text":f"[配置检查] FFmpeg路径: {os.path.join(ffmpeg_bin, 'ffmpeg.exe')}",'level':'debug'})


