import time
import sys,os
import shutil
import zipfile
import requests
from pathlib import Path
from urllib.parse import urlparse
import concurrent.futures
import subprocess
import hashlib

class LoggerProgressBar:
    """使用日志系统显示下载进度的进度条类"""
    
    def __init__(self, total=None, unit='B', unit_scale=True, desc="下载进度", logger=None):
        self.total = total
        self.unit = unit
        self.unit_scale = unit_scale
        self.desc = desc
        self.logger = logger
        self.current = 0
        self.last_log_time = time.time()
        self.last_log_percentage = 0
        self.log_interval = 1.5  # 每1.5秒更新一次进度，更频繁的反馈
        self.start_time = time.time()
        
    def update(self, n=1):
        """更新进度"""
        self.current += n
        current_time = time.time()
        
        # 计算进度百分比
        if self.total and self.total > 0:
            percentage = (self.current / self.total) * 100
        else:
            percentage = 0
            
        # 计算下载速度
        elapsed_time = current_time - self.start_time
        if elapsed_time > 0:
            speed = self.current / elapsed_time
            speed_text = self._format_size(speed) + "/s"
        else:
            speed_text = "0B/s"
            
        # 格式化文件大小
        current_size = self._format_size(self.current)
        total_size = self._format_size(self.total) if self.total else "未知"
        
        # 控制日志频率，避免过于频繁的日志输出
        if (current_time - self.last_log_time >= self.log_interval or 
            percentage - self.last_log_percentage >= 10 or  # 每10%更新一次
            self.current == self.total):  # 完成时更新
            
            if self.total and self.total > 0:
                progress_text = f"{self.desc}: {current_size}/{total_size} ({percentage:.1f}%) - {speed_text}"
            else:
                progress_text = f"{self.desc}: {current_size} - {speed_text}"
                
            if self.logger:
                self.logger.put({"text": progress_text, "level": "info"})
            else:
                print(progress_text)
                
            self.last_log_time = current_time
            self.last_log_percentage = percentage
    
    def _format_size(self, size):
        """格式化文件大小显示"""
        if size is None:
            return "未知"
            
        if self.unit_scale:
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f}{unit}"
                size /= 1024.0
            return f"{size:.1f}TB"
        else:
            return f"{size}{self.unit}"
    
    def close(self):
        """关闭进度条"""
        if self.current > 0:
            final_size = self._format_size(self.current)
            total_time = time.time() - self.start_time
            if total_time > 0:
                avg_speed = self._format_size(self.current / total_time) + "/s"
                completion_text = f"{self.desc}完成: {final_size} (用时: {total_time:.1f}s, 平均速度: {avg_speed})"
            else:
                completion_text = f"{self.desc}完成: {final_size}"
                
            if self.logger:
                self.logger.put({"text": completion_text, "level": "info"})
            else:
                print(completion_text)

def validate_installer(exe_path: Path) -> bool:
    """验证下载的文件是否为有效的安装程序"""
    try:
        # 检查文件是否存在
        if not exe_path.exists():
            return False
        
        # 检查文件扩展名
        if exe_path.suffix.lower() != '.exe':
            return False
        
        # 检查文件大小（至少1MB）
        if exe_path.stat().st_size < 1024 * 1024:
            return False
        
        # 尝试获取文件版本信息（Windows）
        try:
            import win32api
            info = win32api.GetFileVersionInfo(str(exe_path), "\\")
            return True
        except:
            # 如果无法获取版本信息，至少检查文件头
            with open(exe_path, 'rb') as f:
                header = f.read(2)
                return header == b'MZ'  # PE文件头
                
    except Exception:
        return False

def launch_installer(exe_path: Path, silent_mode: bool = False) -> bool:
    """启动安装程序"""
    try:
        if silent_mode:
            # 静默安装模式
            subprocess.Popen([str(exe_path), "/S", "/D=" + str(Path.cwd())], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
            print("✅ 静默安装程序已启动")
        else:
            # 交互式安装模式
            subprocess.Popen([str(exe_path)], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
            print("✅ 安装程序已启动，请按照安装向导完成更新")
        
        return True
        
    except Exception as e:
        print(f"🚨 启动安装程序失败: {str(e)}")
        return False

def fast_download(url: str, save_path: Path, workers=8, logger=None) -> bool:
    """增强版多线程下载"""
    try:
        # 验证服务器支持分块下载
        with requests.head(url, timeout=10) as r:
            if r.headers.get('Accept-Ranges') != 'bytes':
                if logger:
                    logger.put({"text": str(r.headers), "level": "debug"})
                    logger.put({"text": "⚠️ 服务器不支持多线程下载，切换为单线程模式", "level": "warning"})
                else:
                    print(r.headers)
                    print("⚠️ 服务器不支持多线程下载，切换为单线程模式")
                return _single_download_optimized(url, save_path, logger)
                
            total_size = int(r.headers.get('content-length', 0))
            if not total_size:
                raise ValueError("无法获取文件大小")

        # 预创建文件
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.truncate(total_size)  # 预分配空间

        # 智能分块策略（自动减少worker数量）
        max_workers = min(workers, total_size // (1024*1024))  # 1MB以下不分块
        if max_workers < 1:
            return _single_download_optimized(url, save_path, logger)

        chunk_size = total_size // max_workers
        ranges = [(i*chunk_size, (i+1)*chunk_size-1) for i in range(max_workers-1)]
        ranges.append((ranges[-1][1]+1, total_size-1))  # 修正最后一块

        progress = LoggerProgressBar(total=total_size, unit='B', unit_scale=True, desc="模型下载进度", logger=logger)

        # 带校验的分块下载
        def download_chunk(start, end):
            headers = {'Range': f'bytes={start}-{end}'}
            with requests.get(url, headers=headers, stream=True) as r:
                if r.status_code != 206:
                    raise RuntimeError(f"分块请求失败（状态码 {r.status_code}）")
                
                actual_length = int(r.headers.get('content-length', 0))
                expected_length = end - start + 1
                if actual_length != expected_length:
                    raise RuntimeError(f"分块长度异常（预期 {expected_length}，实际 {actual_length}）")

                with open(save_path, 'r+b') as f:
                    f.seek(start)
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(len(chunk))

        # 弹性线程池管理
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(download_chunk, s, e) for s, e in ranges}
            while futures:
                done, futures = concurrent.futures.wait(
                    futures, 
                    timeout=5,
                    return_when=concurrent.futures.FIRST_EXCEPTION
                )
                for future in done:
                    if future.exception():
                        executor.shutdown(cancel_futures=True)
                        raise future.exception()

        # 最终校验
        if (actual_size := save_path.stat().st_size) != total_size:
            raise RuntimeError(f"文件大小不一致（预期 {total_size}，实际 {actual_size}）")

        progress.close()
        return True

    except Exception as e:
        if logger:
            logger.put({"text": f"🚨 下载失败: {str(e)}", "level": "error"})
        else:
            print(f"🚨 下载失败: {str(e)}")
        if save_path.exists():
            save_path.unlink()
        return False

def _single_download_optimized(url: str, save_path: Path, logger=None) -> bool:
    """修复进度条问题的单线程下载"""
    try:
        session = requests.Session()
        with session.get(url, stream=True, timeout=(10, 30)) as r:
            r.raise_for_status()
            
            # 获取文件大小（优先使用头信息，其次内容长度）
            total_size = int(r.headers.get('content-length', 0))
            if total_size == 0:
                # 当服务器未提供大小时采用动态更新模式
                progress = LoggerProgressBar(unit='B', unit_scale=True, desc="本地识别模型下载进度", logger=logger)
            else:
                progress = LoggerProgressBar(total=total_size, unit='B', unit_scale=True, desc="本地识别模型下载进度", logger=logger)

            buffer_size = 1024 * 1024 * 4  # 优化为4MB缓冲
            buffer = bytearray()
            
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*128):  # 128KB块
                    if chunk:
                        buffer.extend(chunk)
                        progress.update(len(chunk))  # 实时更新每个chunk
                        
                        # 缓冲写入优化
                        if len(buffer) >= buffer_size:
                            f.write(buffer)
                            buffer = bytearray()

                # 写入剩余缓冲
                if buffer:
                    f.write(buffer)
                    progress.update(len(buffer))

            # 最终大小校验（仅当已知总大小时）
            if total_size > 0:
                actual_size = save_path.stat().st_size
                if actual_size != total_size:
                    raise RuntimeError(f"文件不完整（{actual_size}/{total_size}字节）")

            progress.close()
            return True

    except Exception as e:
        if 'progress' in locals():
            progress.close()
        if logger:
            logger.put({"text": f"下载失败: {str(e)}", "level": "error"})
        else:
            print(f"下载失败: {str(e)}")
        if save_path.exists():
            save_path.unlink()
        return False



def get_file_info(folder):
    """递归获取文件夹内所有文件的相对路径和哈希值"""
    file_dict = {}
    for root, _, files in os.walk(folder):
        rel_path = os.path.relpath(root, folder)
        for file in files:
            file_path = os.path.join(root, file)
            rel_file = os.path.join(rel_path, file).replace('\\', '/')
            # 计算文件哈希（可选）
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            file_dict[rel_file] = file_hash
    return file_dict

def copy_new_files(src_folder, dst_folder, logger=None):
    """复制源文件夹中存在但目标文件夹缺失的文件"""
    src_files = get_file_info(src_folder)
    dst_files = get_file_info(dst_folder)

    for rel_file, file_hash in src_files.items():
        dst_file_path = os.path.join(dst_folder, rel_file)
        if rel_file not in dst_files:  # 新增文件
            src_file_path = os.path.join(src_folder, rel_file)
            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
            shutil.copy2(src_file_path, dst_file_path)
            if logger:
                logger.put({"text": f'Copied: {rel_file}', "level": "debug"})
            else:
                print(f'Copied: {rel_file}')
        elif src_files[rel_file] != dst_files[rel_file]:  # 内容不同的文件
            if logger:
                logger.put({"text": f'Modified (not copied): {rel_file}', "level": "debug"})
            else:
                print(f'Modified (not copied): {rel_file}')


def create_restarter(temp_dir: Path, install_dir: Path):
    """创建跨平台的启动脚本"""
    script = temp_dir / "update_launcher.bat"
    content = f"""@echo off
timeout /t 2 /nobreak >nul
taskkill /F /IM VRCLS.exe
timeout /t 3 /nobreak >nul
move /Y "{temp_dir / 'VRCLS' /'VRCLS.exe'}" "{install_dir /'VRCLS.exe'}"
rd /s /q "{temp_dir}"
del "%~f0"
"""

    script.write_text(content, encoding='utf-8')
    return script

def unzip_and_replace(zip_path: Path, install_dir: Path) -> None:
    """解压到临时目录并创建启动器"""
    try:
        temp_dir = install_dir / "cache" / "new_tmp"
        temp_dir.mkdir(exist_ok=True)

        # 清空临时目录
        for item in temp_dir.glob('*'):
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # 解压到临时目录
        with zipfile.ZipFile(zip_path) as zip_ref:
            zip_ref.extractall(temp_dir)
        copy_new_files(temp_dir/'VRCLS'/'_internal', install_dir /'_internal')
        # 创建平台特定的启动脚本
        restarter_script = create_restarter(temp_dir, install_dir)
        
        # 启动清理脚本并退出

        subprocess.Popen(['cmd', '/C', restarter_script], 
                       creationflags=subprocess.CREATE_NO_WINDOW
                        )

        # 清理旧版本文件
        zip_path.unlink()
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False



def main_update(url: str, install_dir: Path, silent_mode: bool = False) -> bool:
    """下载并启动安装exe文件"""
    # 创建下载目录
    download_dir = Path.cwd() / "cache"
    download_dir.mkdir(exist_ok=True)

    # 生成保存路径
    file_name = Path(urlparse(url).path).name
    exe_path = download_dir / file_name

    # 执行下载流程
    if not fast_download(url, exe_path):
        return False
    
    # 验证下载的安装程序
    if not validate_installer(exe_path):
        print("🚨 下载的文件不是有效的安装程序")
        if exe_path.exists():
            exe_path.unlink()
        return False
    
    if silent_mode:
        print(r'''
              
              >>>>> 新版本安装程序下载完成，即将启动静默安装 <<<<<
            
''')
    else:
        print(r'''
              
              >>>>> 新版本安装程序下载完成，即将启动安装程序 <<<<<
            
''')
    time.sleep(2)
    
    try:
        # 启动安装程序
        if not launch_installer(exe_path, silent_mode):
            return False
        
        print("✅ 安装程序已启动，请按照安装向导完成更新")
        print("📝 安装完成后，程序会在下次启动时自动清理安装包")
        
        return True
        
    except Exception as e:
        print(f"🚨 启动安装程序失败: {str(e)}")
        if exe_path.exists():
            exe_path.unlink()
        return False

def module_download(url: str, install_dir: Path, logger=None) -> bool:
    import os
    import shutil
    import py7zr
    download_dir = Path.cwd() / "cache"
    download_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        file_name = Path(urlparse(url).path).name
        zip_path = download_dir / file_name

        if not fast_download(url, zip_path, logger=logger):return False
        if logger:
            logger.put({"text": r'''
              
              >>>>> 模型包文件解压安装中，请勿关闭窗口 <<<<<
            
''', "level": "info"})
        else:
            print(r'''
              
              >>>>> 模型包文件解压安装中，请勿关闭窗口 <<<<<
            
''')
        extract_root = Path(os.path.dirname(sys._MEIPASS))/"temp_extract" if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"temp_extract")         # 临时解压目录
        final_output_dir = install_dir / "sherpa-onnx-models" # 最终输出目录

        try:
            # 创建临时解压目录
            os.makedirs(extract_root, exist_ok=True)

            # 解压整个压缩包
            if logger:
                logger.put({"text": "开始解压模型包文件...", "level": "info"})
            with py7zr.SevenZipFile(zip_path, mode='r') as z:
                z.extractall(path=extract_root)
            if logger:
                logger.put({"text": "模型包文件解压完成", "level": "info"})

            # 定位目标文件夹路径
            source_folder = os.path.join(
                extract_root,
                "VRCLS本地识别模型包",  # 解压后的一级目录名
                "sherpa-onnx-models"   # 需要保留的目标文件夹
            )

            if not os.path.exists(source_folder):
                raise FileNotFoundError(
                    f"目标文件夹不存在: {source_folder}\n"
                    "请检查压缩包目录结构是否符合预期"
                )

            # 如果目标文件夹已存在则删除
            if os.path.exists(final_output_dir):
                if logger:
                    logger.put({"text": "删除旧版本模型文件夹...", "level": "info"})
                shutil.rmtree(final_output_dir)

            # 移动目标文件夹到最终位置
            if logger:
                logger.put({"text": "移动模型文件到目标位置...", "level": "info"})
            shutil.move(source_folder, final_output_dir)

            if logger:
                logger.put({"text": f"成功提取文件夹到: {os.path.abspath(final_output_dir)}", "level": "info"})
            else:
                print(f"成功提取文件夹到: {os.path.abspath(final_output_dir)}")

        finally:
            # 清理临时文件
            if os.path.exists(extract_root):
                if logger:
                    logger.put({"text": "清理临时文件...", "level": "info"})
                shutil.rmtree(extract_root)

        # 验证结果
        if os.path.exists(final_output_dir):
            if logger:
                logger.put({"text": "操作成功完成！\n", "level": "info"})
            else:
                print("操作成功完成！\n")
        else:
            if logger:
                logger.put({"text": "操作失败，最终文件夹未生成\n", "level": "error"})
            else:
                print("操作失败，最终文件夹未生成\n")

        return True

    except Exception as e:
        if logger:
            logger.put({"text": f"🚨 模型下载失败: {str(e)}", "level": "error"})
        else:
            print(f"🚨 模型下载失败: {str(e)}")
        if 'zip_path' in locals() and zip_path.exists():
            zip_path.unlink()
        return False

    # restart_application()
if __name__ == "__main__":
    import py7zr
    # 配置参数
    UPDATE_URL = "https://cloudflarestorage.boyqiu001.top/VRCLS本地识别模型包.7z"  # 替换为实际URL
    INSTALL_DIR = Path(__file__).parent.resolve()  # 安装目录为当前脚本所在目录
    # zip_path=Path.home() / "VRCLS" / 'VRCLS本地识别模型包.7z'
    # with py7zr.SevenZipFile(zip_path, mode='r') as archive:
    #     archive.extractall(path=INSTALL_DIR)
    # # 启动更新
    # module_download(UPDATE_URL, INSTALL_DIR)


    # 假设这是您的压缩文件和安装目录路径
    # zip_path=
    # INSTALL_DIR = "您的安装路径"

    # 压缩包内目标文件夹的路径（注意末尾斜杠）
    target_in_zip = "VRCLS本地识别模型包/sherpa-onnx-models/"

def check_for_updates(update_url: str, current_version: str = "1.0.0") -> bool:
    """检查是否有可用更新"""
    try:
        # 这里可以添加版本检查逻辑
        # 例如从服务器获取最新版本信息
        print(f"当前版本: {current_version}")
        print("正在检查更新...")
        
        # 模拟检查更新（实际使用时应该从服务器获取版本信息）
        return True
        
    except Exception as e:
        print(f"检查更新失败: {str(e)}")
        return False

def auto_update(update_url: str, install_dir: Path = None, silent_mode: bool = False) -> bool:
    """自动更新主函数"""
    if install_dir is None:
        install_dir = Path.cwd()
    
    print("🔄 开始自动更新...")
    
    # 检查更新
    if not check_for_updates(update_url):
        print("❌ 无法检查更新或无需更新")
        return False
    
    # 执行更新
    success = main_update(update_url, install_dir, silent_mode)
    
    if success:
        print("✅ 更新流程已启动")
    else:
        print("❌ 更新失败")
    
    return success

def cleanup_installer_files(logger=None):
    """清理下载的安装包文件"""
    try:
        cache_dir = Path.cwd() / "cache"
        if cache_dir.exists():
            # 查找并删除exe安装包文件
            for exe_file in cache_dir.glob("*.exe"):
                try:
                    exe_file.unlink()
                    if logger:
                        logger.put({"text": f"🗑️ 已清理安装包: {exe_file.name}", "level": "info"})
                    else:
                        print(f"🗑️ 已清理安装包: {exe_file.name}")
                except Exception as e:
                    if logger:
                        logger.put({"text": f"清理文件失败 {exe_file.name}: {str(e)}", "level": "error"})
                    else:
                        print(f"清理文件失败 {exe_file.name}: {str(e)}")
        
        if logger:
            logger.put({"text": "✅ 安装包清理完成", "level": "info"})
        else:
            print("✅ 安装包清理完成")
        return True
        
    except Exception as e:
        if logger:
            logger.put({"text": f"清理安装包失败: {str(e)}", "level": "error"})
        else:
            print(f"清理安装包失败: {str(e)}")
        return False


    
