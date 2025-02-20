import psutil
import time

def is_steamvr_running():
    # 遍历所有正在运行的进程
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 检查进程名称是否为 'vrserver.exe'
            if proc.info['name'] == 'vrserver.exe':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def main():
    while True:
        if is_steamvr_running():
            print("SteamVR is running.")
        else:
            print("SteamVR is not running.")
        
        # 每隔5秒检查一次
        time.sleep(5)

if __name__ == "__main__":
    main()