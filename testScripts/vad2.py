import pyaudio
import audioop
import time
import math # 用于向上取整

# 音频参数 (可以根据需要调整)
FORMAT = pyaudio.paInt16  # 采样格式，16位整数
CHANNELS = 1              # 单声道
RATE = 16000              # 采样率 (Hz)，16kHz 是常见的语音采样率
CHUNK = 1024              # 每次读取的帧数 (缓冲区大小)
SAMPLE_WIDTH = pyaudio.get_sample_size(FORMAT) # 每个样本的字节数 (paInt16 为 2)

# 测量持续时间 (秒)
NOISE_DURATION_S = 3      # 测量背景噪音的持续时间
SPEAKING_DURATION_S = 5   # 测量说话音量的持续时间
DEMO_DURATION_S = 10      # VAD演示的持续时间 (秒)，可以设为更长或用Ctrl+C中断

def calibrate_vad_threshold():
    """
    测量背景噪音和说话音量，并计算VAD能量阈值。
    阈值 = 背景噪音能量 + (说话音量 - 背景噪音能量) / 5
    """
    p_cal = pyaudio.PyAudio() # 使用不同的PyAudio实例，避免潜在冲突
    stream_cal = None
    
    print(f"音频参数: 格式={FORMAT}, 通道数={CHANNELS}, 采样率={RATE}Hz, 块大小={CHUNK}帧")
    print(f"样本宽度: {SAMPLE_WIDTH} 字节")
    print("-" * 30)

    try:
        stream_cal = p_cal.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

        # 1. 测量背景噪音能量
        print(f"准备测量背景噪音，请保持安静 {NOISE_DURATION_S} 秒...")
        time.sleep(1) 
        
        noise_energies = []
        num_noise_chunks = math.ceil(RATE / CHUNK * NOISE_DURATION_S)
        
        print("开始测量噪音...")
        for i in range(num_noise_chunks):
            try:
                data = stream_cal.read(CHUNK, exception_on_overflow=False)
                rms = audioop.rms(data, SAMPLE_WIDTH)
                noise_energies.append(rms)
                print(f"\r噪音采样: {i+1}/{num_noise_chunks}, 当前RMS: {rms:<5}", end="")
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed: # paInputOverflowed value might differ based on pyaudio/portaudio version
                    print("\n警告: 输入溢出，忽略此块数据。")
                    continue 
                else:
                    raise 
        print("\n噪音测量完成。")

        if not noise_energies:
            print("错误：未能采集到背景噪音样本。请检查麦克风设置。")
            return None
        
        avg_noise_energy = sum(noise_energies) / len(noise_energies)
        print(f"平均背景噪音能量 (RMS): {avg_noise_energy:.2f}")
        print("-" * 30)

        # 2. 测量说话音量
        print(f"准备测量说话音量，请在提示后用正常音量说话，持续 {SPEAKING_DURATION_S} 秒...")
        time.sleep(2)
        
        speaking_energies = []
        num_speaking_chunks = math.ceil(RATE / CHUNK * SPEAKING_DURATION_S)
        
        print("请开始说话！")
        for i in range(num_speaking_chunks):
            try:
                data = stream_cal.read(CHUNK, exception_on_overflow=False)
                rms = audioop.rms(data, SAMPLE_WIDTH)
                speaking_energies.append(rms)
                print(f"\r说话采样: {i+1}/{num_speaking_chunks}, 当前RMS: {rms:<5}", end="")
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    print("\n警告: 输入溢出，忽略此块数据。")
                    continue
                else:
                    raise
        print("\n说话测量完成。")

        if not speaking_energies:
            print("错误：未能采集到说话样本。请确保在提示时说话。")
            return None

        valid_speaking_energies = [e for e in speaking_energies if e > avg_noise_energy * 1.2]
        
        if not valid_speaking_energies:
            print("警告：采集到的说话音量较低或与噪音难以区分。将使用所有采集到的说话样本进行计算。")
            avg_speaking_energy = sum(speaking_energies) / len(speaking_energies) if speaking_energies else avg_noise_energy * 2
        else:
            avg_speaking_energy = sum(valid_speaking_energies) / len(valid_speaking_energies)
            
        print(f"平均说话音量 (RMS, 过滤后): {avg_speaking_energy:.2f}")
        print("-" * 30)

        # 3. 计算VAD阈值
        if avg_speaking_energy <= avg_noise_energy:
            print("警告：说话音量低于或等于背景噪音。阈值可能不准确。")
            print("建议重新校准，确保说话时音量足够大且清晰。")
            vad_threshold = avg_noise_energy * 1.5 
        else:
            vad_threshold = avg_noise_energy + (avg_speaking_energy - avg_noise_energy) / 5.0
        
        print(f"计算得到的 VAD 能量阈值: {vad_threshold:.2f}")
        
        return vad_threshold

    except Exception as e:
        print(f"在校准过程中发生错误: {e}")
        return None
    finally:
        if stream_cal:
            stream_cal.stop_stream()
            stream_cal.close()
        p_cal.terminate()
        print("校准音频资源已释放。")

def demonstrate_vad(threshold, duration_s=10):
    """
    使用给定的阈值演示VAD。
    :param threshold: VAD能量阈值
    :param duration_s: 演示的持续时间（秒）。如果为0或负数，则持续到Ctrl+C。
    """
    if threshold is None:
        print("错误：VAD阈值未提供，无法开始演示。")
        return

    p_demo = pyaudio.PyAudio()
    stream_demo = None

    print("\n" + "=" * 30)
    print("开始 VAD 演示...")
    print(f"使用的阈值: {threshold:.2f}")
    print(f"请说话或保持安静，观察检测结果。")
    if duration_s > 0:
        print(f"演示将持续 {duration_s} 秒。按 Ctrl+C 可提前结束。")
    else:
        print("演示将持续进行，按 Ctrl+C 结束。")
    print("=" * 30)
    time.sleep(1)


    try:
        stream_demo = p_demo.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        start_time = time.time()
        while True:
            if duration_s > 0 and (time.time() - start_time) > duration_s:
                break
            try:
                data = stream_demo.read(CHUNK, exception_on_overflow=False)
                rms = audioop.rms(data, SAMPLE_WIDTH)
                
                if rms > threshold:
                    status = "SPEECH"
                else:
                    status = "SILENCE"
                
                # 使用 \r 和空格填充来覆盖上一行，避免残留字符
                print(f"\r当前 RMS: {rms:<7.2f} | 阈值: {threshold:.2f} | 检测: {status:<8s}  ", end="")

            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    print("\n警告: (演示中) 输入溢出，忽略此块数据。")
                    continue
                else:
                    raise
            except KeyboardInterrupt:
                print("\n用户中断了演示。")
                break
        
        print("\n演示结束。")

    except Exception as e:
        print(f"\n在VAD演示过程中发生错误: {e}")
    finally:
        if stream_demo:
            stream_demo.stop_stream()
            stream_demo.close()
        p_demo.terminate()
        print("演示音频资源已释放。")


if __name__ == "__main__":
    print("开始 VAD 能量阈值校准与演示程序...")
    
    try:
        p_temp = pyaudio.PyAudio()
        print("\n可用输入设备:")
        default_input_device_index = p_temp.get_default_input_device_info()['index']
        for i in range(p_temp.get_device_count()):
            dev_info = p_temp.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                print(f"  设备 {i}: {dev_info['name']} {'(默认)' if i == default_input_device_index else ''}")
        p_temp.terminate()
        print("")
    except Exception as e:
        print(f"列出设备时出错: {e}")

    # 1. 校准阈值
    calibrated_threshold = calibrate_vad_threshold()

    if calibrated_threshold is not None:
        print(f"\n最终校准的 VAD 阈值: {calibrated_threshold:.2f}")
        
        # 2. 演示VAD
        try:
            # 给用户一个明确的提示，并等待确认，避免立即开始演示
            input("按 Enter 键开始VAD演示，或按 Ctrl+C 退出...") 
            demonstrate_vad(calibrated_threshold, duration_s=DEMO_DURATION_S) # 演示指定秒数
            # 或者演示直到用户按Ctrl+C:
            # demonstrate_vad(calibrated_threshold, duration_s=0) 
        except KeyboardInterrupt:
            print("\n程序已由用户退出。")
        
    else:
        print("\n未能成功校准 VAD 阈值，无法进行演示。")