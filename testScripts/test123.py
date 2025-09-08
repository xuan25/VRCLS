#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面音频实时VAD测试脚本 (智能适配最终版)
- 自动检测并使用设备支持的正确音频格式(format)和声道数(channels)。
- 正确地将捕获的音频数据标准化为 float32 格式。
- 正确地处理立体声到单声道的转换。
- 使用 librosa 进行高质量重采样。
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import time
from datetime import datetime
from pathlib import Path
from collections import deque

try:
    import pyaudiowpatch as pyaudio
except ImportError:
    print("[ERROR] 请先安装PyAudioWPatch: pip install pyaudiowpatch")
    sys.exit(1)

try:
    import librosa
except ImportError:
    print("[ERROR] 请先安装librosa: pip install librosa")
    sys.exit(1)

from src.core.onnx_vad import SileroVADONNX

# --- NEW: 用于数据标准化的辅助函数 ---
def get_format_info(p, audio_format):
    """根据PyAudio的格式常量，返回Numpy数据类型和标准化因子"""
    if audio_format == pyaudio.paFloat32:
        return np.float32, 1.0
    elif audio_format == pyaudio.paInt32:
        return np.int32, 2**31 - 1
    elif audio_format == pyaudio.paInt24:
        # paInt24 is technically 3 bytes, but often read into a 4-byte int
        # The max value is 2^23 - 1
        return np.int32, 2**23 - 1
    elif audio_format == pyaudio.paInt16:
        return np.int16, 2**15 - 1
    elif audio_format == pyaudio.paInt8 or audio_format == pyaudio.paUInt8:
        return np.int8, 2**7 - 1
    else:
        raise ValueError(f"不支持的音频格式: {audio_format}")


class DesktopAudioVADTester:
    VAD_TARGET_SAMPLE_RATE = 16000
    VAD_WINDOW_SIZE = 1536

    def __init__(self, vad_threshold=0.5, debug_mode=False):
        self.vad = SileroVADONNX()
        self.threshold = vad_threshold
        self.debug_mode = debug_mode
        self._audio_buffer = np.array([], dtype=np.float32)
        # ... (其他初始化变量保持不变)
        self.speech_start_time = 0; self.is_currently_speaking = False
        self.silence_frames_after_speech = 0; self.silence_trigger_threshold = 10
        self.speech_buffer = deque(maxlen=5); self.start_time = None; self.running = False
        self.debug_audio_buffer = []; self.debug_dir = Path("debug_audio")
        self.debug_dir.mkdir(exist_ok=True); self.debug_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def process_audio_stream(self, audio_chunk_float32, original_sample_rate):
        """接收已标准化为float32的单声道音频流"""
        resampled_audio = librosa.resample(
            y=audio_chunk_float32, 
            orig_sr=original_sample_rate, 
            target_sr=self.VAD_TARGET_SAMPLE_RATE
        )
        self._audio_buffer = np.concatenate([self._audio_buffer, resampled_audio])

        while len(self._audio_buffer) >= self.VAD_WINDOW_SIZE:
            vad_chunk = self._audio_buffer[:self.VAD_WINDOW_SIZE]
            self._audio_buffer = self._audio_buffer[self.VAD_WINDOW_SIZE:]

            peak_volume = np.max(np.abs(vad_chunk))
            prob = self.vad(vad_chunk)
            
            print(f"[VAD Chunk] Peak: {peak_volume:.4f}, VAD Prob: {prob:.3f}")

            self.update_speech_state(prob >= self.threshold, prob)
            
            if self.debug_mode:
                self.debug_audio_buffer.extend(vad_chunk)

    def update_speech_state(self, is_speech, probability):
        # ... (此方法保持不变)
        self.speech_buffer.append(is_speech)
        if not self.is_currently_speaking and sum(self.speech_buffer) >= 3:
            self.is_currently_speaking = True; self.speech_start_time = time.time(); self.silence_frames_after_speech = 0
            print(f"🎤 [语音进入] 检测到语音开始! 概率: {probability:.3f}")
        elif self.is_currently_speaking and not is_speech:
            self.silence_frames_after_speech += 1
            if self.silence_frames_after_speech >= self.silence_trigger_threshold:
                speech_duration = time.time() - self.speech_start_time
                print(f"🔇 [语音退出] 语音结束! 持续时间: {speech_duration:.2f}秒")
                self.is_currently_speaking = False; self.speech_buffer.clear()
        elif self.is_currently_speaking and is_speech:
            self.silence_frames_after_speech = 0
            
    def start_realtime_testing(self, duration=None):
        print("[INFO] 正在初始化桌面音频监听...")
        
        p = pyaudio.PyAudio()
        try:
            device_info = p.get_default_wasapi_loopback()
            rate = int(device_info["defaultSampleRate"])
            channels = device_info["maxInputChannels"]
            
            # --- 关键: 智能格式发现 ---
            # 我们优先尝试float32，如果不支持，则尝试int16，这是最常见的组合
            supported_formats = [pyaudio.paFloat32, pyaudio.paInt16, pyaudio.paInt32, pyaudio.paInt24]
            audio_format = None
            for f in supported_formats:
                if p.is_format_supported(rate, input_device=device_info['index'], input_channels=channels, input_format=f):
                    audio_format = f
                    break
            
            if not audio_format:
                raise RuntimeError("设备不支持任何可用的音频格式 (Float32, Int16, Int32, Int24)")

            numpy_dtype, norm_factor = get_format_info(p, audio_format)
            
            print(f"[OK] 使用设备: {device_info['name']}")
            print(f"[OK] 动态参数: 采样率={rate}Hz, 声道={channels}, 格式={audio_format} (Numpy: {numpy_dtype.__name__})")
            print(f"[OK] VAD阈值: {self.threshold}")
            print("\n[INFO] 开始监听... (按 Ctrl+C 停止)")
            print("-" * 60)
            
            self.vad.reset_states()

            stream = p.open(
                format=audio_format,
                channels=channels,
                rate=rate,
                input=True,
                input_device_index=device_info["index"],
            )

            self.running = True
            while self.running:
                if duration and (time.time() - (self.start_time or time.time())) > duration: break
                if not self.start_time: self.start_time = time.time()

                chunk_size = int(rate * 0.1) # 每次读取100ms
                data = stream.read(chunk_size, exception_on_overflow=False)
                
                # 1. 字节流 -> Numpy数组
                audio_np = np.frombuffer(data, dtype=numpy_dtype)
                
                # 2. 标准化 -> Float32
                if audio_format != pyaudio.paFloat32:
                    audio_np = audio_np.astype(np.float32) / norm_factor
                
                # 3. 多声道 -> 单声道
                if channels > 1:
                    # 将形状从 (N*channels,) 变为 (N, channels)
                    audio_np = audio_np.reshape(-1, channels)
                    # 取平均值变为单声道
                    audio_np = audio_np.mean(axis=1)

                # 4. 将干净的音频送入处理流水线
                self.process_audio_stream(audio_np, rate)

        except KeyboardInterrupt:
            print("\n\n[INFO] 用户中断")
        except Exception as e:
            print(f"\n[ERROR] 发生致命错误: {e}")
            import traceback; traceback.print_exc()
        finally:
            self.running = False
            if 'stream' in locals() and stream.is_active():
                stream.stop_stream(); stream.close()
            p.terminate()
            print("\n[INFO] 测试结束。")

# ... (main 函数保持不变)
def main():
    print("=" * 60); print("桌面音频实时VAD测试 (智能适配最终版)"); print("=" * 60)
    vad_threshold = float(input("VAD阈值(0.0-1.0, 默认0.5): ").strip() or 0.5)
    tester = DesktopAudioVADTester(vad_threshold=vad_threshold)
    tester.start_realtime_testing()

if __name__ == "__main__":
    main()