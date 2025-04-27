import subprocess
def get_udp_port_pid(port):
    cmd = f'netstat -ano -p UDP | findstr :{port}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if 'UDP' in line and f':{port}' in line:
            parts = line.split()
            return parts[-1]  # 返回PID
    return None


def get_process_name(pid):
    cmd = f'tasklist /FI "PID eq {pid}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    lines = result.stdout.split('\n')
    if len(lines) >= 3:
        process_info = lines[3].split()[0]
        return process_info  # 返回进程名
    return None



def check_port(prot,logger):
    pid = get_udp_port_pid(prot)
    if pid:
        process_name = get_process_name(pid)
        if process_name and 'VRChat' in process_name:
            logger.put({'text':f"进程 {process_name} (PID: {pid}) 占用了{prot} UDP端口，疑似 VRChat 相关程序‌:"})
            return 0
        else:
            print(f"占用{prot} UDP端口的进程是 {process_name} (PID: {pid})，请关闭占用的应用或修改VRC接收端口")
            return 1
    else:
        print("9000 UDP端口未被占用")
        return -1
