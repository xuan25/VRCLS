import os

import winreg

def check_webview2_registry():
    reg_paths = [
        r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}",  # 64位系统
        r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"             # 32位系统
    ]
    try:
        for path in reg_paths:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            version, _ = winreg.QueryValueEx(key, "pv")
            if version > "0.0.0.0":
                return True
    except FileNotFoundError:
        pass
    return False

import platform

def get_system_arch():
    arch = platform.machine().lower()
    return "x64" if "64" in arch else "x86"

import requests

def download_webview2_runtime(arch):
    base_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
    download_url = f"{base_url}&arch={arch}"
    return download_url

import subprocess
import ctypes

def install_webview2_runtime(installer_path):
    # 以管理员权限运行安装程序
    ctypes.windll.shell32.ShellExecuteW(None, "runas", installer_path, "/install", None, 1)


if __name__ == "__main__":
    if not check_webview2_registry():
        arch = get_system_arch()
        installer_path = download_webview2_runtime(arch)
        install_webview2_runtime(installer_path)
    else:
        print("WebView2 runtime is already installed.")
