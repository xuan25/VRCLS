import pyaudio
import numpy as np
import time
import math
import collections # For deque, useful for pre-buffering if implementing full VAD

# --- 音频参数 ---
FORMAT = pyaudio.paInt16        # 音频格式：16位PCM
CHANNELS = 1                    # 声道数：单声道
RATE = 16000                    # 采样率：16kHz (语音识别常用)
CHUNK_SIZE = 1024               # 每次读取的帧数 (数据块大小)

# --- 阈值计算参数 ---
CALIBRATION_DURATION = 2.0      # 底噪校准时间（秒）
# 假设说话音量相对于底噪的倍数。
# 例如，6.0 表示我们假设说话音量是底噪能量的6倍。
# 这个值会影响最终的 energy_threshold。
# Threshold = NoiseLevel * (1 + (SPEECH_FACTOR - 1) / 5)
# 若 SPEECH_FACTOR = 6, Threshold = NoiseLevel * 2
# 若 SPEECH_FACTOR = 11, Threshold = NoiseLevel * 3
SPEECH_FACTOR = 6.0 # 您可以调整这个值

# --- VAD (Voice Activity Detection) 相关参数 (可选，用于演示) ---
# 如果实现完整的录制逻辑，这些参数会很有用
SILENCE_THRESHOLD_MULTIPLIER = 0.8 # 用于判断是否真正回到静音状态（相对于energy_threshold）
MIN_SPEECH_DURATION_S = 0.25       # 最短语音持续时间（秒）
PRE_BUFFER_DURATION_S = 0.3        # 语音开始前缓冲时长（秒）
POST_BUFFER_DURATION_S = 0.7       # 语音结束后继续录制的时长（秒）


def calculate_rms(data_chunk):
    """计算给定音频数据块的RMS值"""
    try:
        # 将字节数据转换为numpy数组 (int16)
        audio_data = np.frombuffer(data_chunk, dtype=np.int16)
        if len(audio_data) == 0:
            return 0
        # 计算RMS: sqrt(mean(amplitude^2))
        # 使用float64进行计算以避免溢出
        rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float64))))
        return rms
    except Exception as e:
        print(f"Error calculating RMS: {e}")
        return 0

def main():
    p = pyaudio.PyAudio()

    # --- 1. 校准底噪 ---
    print(f"[*] Calibrating noise level for {CALIBRATION_DURATION} seconds. Please be quiet...")
    
    noise_calibration_stream = p.open(format=FORMAT,
                                     channels=CHANNELS,
                                     rate=RATE,
                                     input=True,
                                     frames_per_buffer=CHUNK_SIZE)
    
    noise_rms_values = []
    num_calibration_chunks = int(RATE / CHUNK_SIZE * CALIBRATION_DURATION)
    
    for _ in range(num_calibration_chunks):
        try:
            data = noise_calibration_stream.read(CHUNK_SIZE, exception_on_overflow=False)
            rms = calculate_rms(data)
            noise_rms_values.append(rms)
        except IOError as e:
            print(f"IOError during noise calibration read: {e}")
            # 如果发生溢出，可以考虑跳过这个块或采取其他错误处理
            continue 
            
    noise_calibration_stream.stop_stream()
    noise_calibration_stream.close()

    if not noise_rms_values:
        print("[!] Error: No data collected during noise calibration. Using a default noise level.")
        noise_level = 50.0 # 设置一个默认的较低噪音水平
    else:
        noise_level = np.mean(noise_rms_values)
        if noise_level < 1.0: # 防止噪音过低导致阈值也过低
            print(f"[!] Warning: Calibrated noise level ({noise_level:.2f}) is very low. Adjusting to a minimum of 1.0.")
            noise_level = 1.0
            
    print(f"[*] Calibration complete. Average noise RMS: {noise_level:.2f}")

    # --- 2. 计算能量阈值 ---
    # Threshold = NoiseLevel * (1 + (SPEECH_FACTOR - 1) / 5)
    energy_threshold = noise_level * (1 + (SPEECH_FACTOR - 1) / 5)
    print(f"[*] Calculated dynamic energy_threshold: {energy_threshold:.2f}")
    print(f"    (Based on assumed speech energy being {SPEECH_FACTOR:.1f}x noise energy)")
    print(f"    (Threshold is noise + 1/5 of the difference between assumed speech and noise)")


    # --- 3. 实时监测和演示 ---
    print("\n[*] Starting to listen. Speak to test the threshold.")
    print("    You will see 'Speech detected!' when RMS exceeds the threshold.")
    print("    Press Ctrl+C to stop.")

    # 打开主音频流进行监听
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    # (可选) VAD状态变量，如果要实现完整的录音功能
    is_speaking = False
    # pre_buffer = collections.deque(maxlen=int(RATE / CHUNK_SIZE * PRE_BUFFER_DURATION_S))
    # recorded_frames = []
    # silence_chunks_after_speech = 0

    try:
        while True:
            try:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            except IOError as e:
                print(f"IOError during listening read: {e}")
                # 简单处理：如果读取失败，跳过这个周期
                if "Input overflowed" in str(e): # 常见错误
                     print("[Warning] Microphone input overflowed. System might be too slow or CHUNK_SIZE too small.")
                time.sleep(0.01) # 短暂暂停
                continue


            current_rms = calculate_rms(data)
            
            # (可选) 填充 pre_buffer
            # pre_buffer.append(data)

            if current_rms > energy_threshold:
                if not is_speaking:
                    print(f"Speech detected! (RMS: {current_rms:.2f} > Threshold: {energy_threshold:.2f})")
                    is_speaking = True
                    # (可选) 如果实现录音:
                    # recorded_frames.extend(list(pre_buffer)) # 将预缓冲数据加入
                # else: # 正在说话
                    # (可选) 如果实现录音:
                    # recorded_frames.append(data)
                # silence_chunks_after_speech = 0 # 重置静音计数
            else: # 低于阈值
                if is_speaking:
                    # (可选) 如果实现录音:
                    # recorded_frames.append(data) # 仍然记录一小段静音
                    # silence_chunks_after_speech += 1
                    # max_silence_chunks = int(RATE / CHUNK_SIZE * POST_BUFFER_DURATION_S)
                    # if silence_chunks_after_speech > max_silence_chunks:
                    print(f"Speech ended. (RMS: {current_rms:.2f} <= Threshold: {energy_threshold:.2f})")
                    is_speaking = False
                        # (可选) 保存录音: save_audio(recorded_frames)
                        # recorded_frames = []
                        # pre_buffer.clear()
                # else:
                    # print(f"Silence (RMS: {current_rms:.2f})") # 频繁打印会刷屏
                    pass
            
            # 短暂延时，避免CPU占用过高，但会增加延迟
            # time.sleep(0.001) 

    except KeyboardInterrupt:
        print("\n[*] Stopping listening.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
    finally:
        print("[*] Cleaning up resources...")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # (可选) 如果有未保存的录音
        # if recorded_frames:
        #    print("[*] Saving any remaining recorded audio...")
        #    # save_audio(recorded_frames)

if __name__ == "__main__":
    main()