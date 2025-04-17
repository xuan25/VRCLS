import time
import sys
import shutil
import zipfile
import requests
from pathlib import Path
from urllib.parse import urlparse
import concurrent.futures
from tqdm import tqdm
import subprocess

def fast_download(url: str, save_path: Path, workers=8) -> bool:
    """增强版多线程下载"""
    try:
        # 验证服务器支持分块下载
        with requests.head(url, timeout=10) as r:
            if r.headers.get('Accept-Ranges') != 'bytes':
                print(r.headers)
                print("⚠️ 服务器不支持多线程下载，切换为单线程模式")
                return _single_download_optimized(url, save_path)
                
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
            return _single_download_optimized(url, save_path)

        chunk_size = total_size // max_workers
        ranges = [(i*chunk_size, (i+1)*chunk_size-1) for i in range(max_workers-1)]
        ranges.append((ranges[-1][1]+1, total_size-1))  # 修正最后一块

        progress = tqdm(total=total_size, unit='B', unit_scale=True)

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
        print(f"🚨 下载失败: {str(e)}")
        if save_path.exists():
            save_path.unlink()
        return False

def _single_download_optimized(url: str, save_path: Path) -> bool:
    """修复进度条问题的单线程下载"""
    try:
        session = requests.Session()
        with session.get(url, stream=True, timeout=(10, 30)) as r:
            r.raise_for_status()
            
            # 获取文件大小（优先使用头信息，其次内容长度）
            total_size = int(r.headers.get('content-length', 0))
            if total_size == 0:
                # 当服务器未提供大小时采用动态更新模式
                progress = tqdm(unit='B', unit_scale=True, desc="下载进度")
            else:
                progress = tqdm(total=total_size, unit='B', unit_scale=True, desc="下载进度")

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
        print(f"下载失败: {str(e)}")
        if save_path.exists():
            save_path.unlink()
        return False





def create_restarter(temp_dir: Path, install_dir: Path):
    """创建跨平台的启动脚本"""
    script = temp_dir / "update_launcher.bat"
    content = f"""@echo off
timeout /t 5 /nobreak >nul
taskkill /F /IM VRCLS.exe
robocopy "{temp_dir / 'VRCLS'}" "{install_dir}" /E /COPY:DATSO /MOVE
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
        print(f"更新失败: {e}\n")
        return False



def main_update(url: str, install_dir: Path) -> None:
    # 创建下载目录
    download_dir = Path.cwd() / "cache"
    download_dir.mkdir(exist_ok=True)

    # 生成保存路径
    file_name = Path(urlparse(url).path).name
    zip_path = download_dir / file_name

    # 执行更新流程
    if not fast_download(url, zip_path):return False
    print(r'''
              
              >>>>> 新版本文件解压安装中，窗户将自动关闭，请在窗口关闭10s后重新启动程序 <<<<<
            
''')
    time.sleep(3)
    return unzip_and_replace(zip_path, install_dir)
    # restart_application()
def module_download(url: str, install_dir: Path) -> bool:
    import os
    import shutil
    import py7zr
    download_dir = Path.cwd() / "cache"
    download_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        file_name = Path(urlparse(url).path).name
        zip_path = download_dir / file_name

        if not fast_download(url, zip_path):return False
        print(r'''
              
              >>>>> 模型包文件解压安装中，请勿关闭窗口 <<<<<
            
''')
        extract_root = Path(os.path.dirname(sys._MEIPASS))/"temp_extract" if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"temp_extract")         # 临时解压目录
        final_output_dir = install_dir / "sherpa-onnx-models" # 最终输出目录

        try:
            # 创建临时解压目录
            os.makedirs(extract_root, exist_ok=True)

            # 解压整个压缩包
            with py7zr.SevenZipFile(zip_path, mode='r') as z:
                z.extractall(path=extract_root)

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
                shutil.rmtree(final_output_dir)

            # 移动目标文件夹到最终位置
            shutil.move(source_folder, final_output_dir)

            print(f"成功提取文件夹到: {os.path.abspath(final_output_dir)}")

        finally:
            # 清理临时文件
            if os.path.exists(extract_root):
                shutil.rmtree(extract_root)

        # 验证结果
        if os.path.exists(final_output_dir):
            print("操作成功完成！\n")
        else:
            print("操作失败，最终文件夹未生成\n")

        return True

    except Exception as e:
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


    
