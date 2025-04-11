import os
import sys
import shutil
import zipfile
import requests
from pathlib import Path
from urllib.parse import urlparse
import concurrent.futures
from tqdm import tqdm

def fast_download(url: str, save_path: Path, workers=8) -> None:
    """多线程分块下载"""
    try:
        # 获取文件大小
        with requests.head(url, timeout=10) as r:
            total_size = int(r.headers.get('content-length', 0))
            if not total_size:
                raise ValueError("服务器未返回文件大小")

        # 创建空文件
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.truncate(total_size)

        # 计算分块范围
        chunk_size = total_size // workers
        ranges = [(i * chunk_size, (i+1)*chunk_size -1) 
                for i in range(workers-1)]
        ranges.append(( (workers-1)*chunk_size, total_size-1 ))

        # 下载进度条
        progress = tqdm(total=total_size, unit='B', unit_scale=True)

        # 定义分块下载函数
        def download_chunk(start, end):
            headers = {'Range': f'bytes={start}-{end}'}
            with requests.get(url, headers=headers, stream=True) as r:
                with open(save_path, 'r+b') as f:
                    f.seek(start)
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(len(chunk))

        # 使用线程池下载
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = []
            for start, end in ranges:
                futures.append(executor.submit(download_chunk, start, end))
            
            # 等待所有线程完成
            for future in concurrent.futures.as_completed(futures):
                future.result()

        progress.close()
        print(f"\n下载完成 {save_path}")

    except Exception as e:
        print(f"多线程下载失败: {e}")
        sys.exit(1)


def unzip_and_replace(zip_path: Path, extract_to: Path) -> None:
    """解压并覆盖现有文件"""
    try:
        # 创建临时解压目录
        temp_dir = extract_to.parent / "temp_update"
        temp_dir.mkdir(exist_ok=True)

        # 解压到临时目录
        with zipfile.ZipFile(zip_path) as zip_ref:
            zip_ref.extractall(temp_dir)
        print("解压完成")

        # 覆盖文件（更安全的文件替换方式）
        for item in temp_dir.glob('*'):
            target = extract_to / item.name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            shutil.move(str(item), str(extract_to))

        # 清理临时文件和目录
        shutil.rmtree(temp_dir)
        zip_path.unlink()
        print("文件替换完成")

    except Exception as e:
        print(f"解压失败: {e}")
        sys.exit(1)

def restart_application() -> None:
    """重启应用程序"""
    print("准备重启...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main_update(url: str, install_dir: Path) -> None:
    # 创建下载目录
    download_dir = Path.home() / "updates"
    download_dir.mkdir(exist_ok=True)

    # 生成保存路径
    file_name = Path(urlparse(url).path).name
    zip_path = download_dir / file_name

    # 执行更新流程
    fast_download(url, zip_path)
    unzip_and_replace(zip_path, install_dir)
    restart_application()

if __name__ == "__main__":
    # 配置参数
    UPDATE_URL = "https://cloudflarestorage.boyqiu001.top/VRCLS-windwos-v0.5.0.zip"  # 替换为实际URL
    INSTALL_DIR = Path(__file__).parent.resolve()  # 安装目录为当前脚本所在目录

    # 启动更新
    main_update(UPDATE_URL, INSTALL_DIR)
