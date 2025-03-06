
from datetime import datetime, timedelta
import psutil
def check_vrserver_wmi():
    try:
        import win32com.client
        # 创建WMI连接（本地连接）
        wmi = win32com.client.GetObject('winmgmts:')
        
        # 构建精确查询（比遍历进程快10倍以上）
        query = "SELECT * FROM Win32_Process WHERE Name = 'vrserver.exe'"
        processes = wmi.ExecQuery(query)
        
        if not processes or len(processes)==0 : return False
        else : return True
    except Exception as e:
        print(f"WMI查询失败: {str(e)}")

if __name__ == "__main__":
    print(check_vrserver_wmi())
