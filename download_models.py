#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载官方Silero VAD ONNX模型
"""
import os
import urllib.request
import zipfile

# 创建models目录
os.makedirs('models', exist_ok=True)

# 官方Silero VAD模型URL
MODEL_URL = "https://github.com/snakers4/silero-vad/raw/v4.0/files/silero_vad.onnx"
MODEL_PATH = "models/silero_vad.onnx"

def download_model():
    """下载Silero VAD ONNX模型"""
    print("下载官方Silero VAD ONNX模型...")
    
    if os.path.exists(MODEL_PATH):
        print("[OK] 模型已存在")
        return True
    
    try:
        print(f"正在下载: {MODEL_URL}")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        
        if os.path.exists(MODEL_PATH):
            size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
            print(f"[OK] 模型下载成功，大小: {size:.2f}MB")
            return True
        else:
            print("[FAIL] 模型下载失败")
            return False
    except Exception as e:
        print(f"[FAIL] 下载失败: {e}")
        return False

if __name__ == "__main__":
    download_model()