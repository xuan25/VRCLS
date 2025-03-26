import requests
import pyaudio
import miniaudio



def libre_tts_audio(text,language='zh',deviceindex=None):
    response = requests.post(
        'https://tts-test.boyqiu001.top/v1/audio/speech',
        json={
            "model": "tts-1",
            "input": text,
            "voice": 'zh-CN-YunzeNeural',
            "style": "documentary-narration",
            "speed": 1.0
        },
        headers={
            "Authorization": "Bearer NfuWNpnr64KWB0KHyMRejWbS0wiMujyvJ9t4caaxPTKvPc5PSM"
        },
        stream=True
    )

    if response.status_code != 200:
        raise Exception(f"请求失败，状态码: {response.status_code}")

    # 直接将响应内容收集到字节对象
    mp3_bytes = b''.join(response.iter_content(chunk_size=8192))

    # 自动检测格式并解码（无需文件信息）
    decoded = miniaudio.decode(
        mp3_bytes,
        output_format=miniaudio.SampleFormat.SIGNED16
    )

    # 转换为 bytes 类型
    pcm_bytes = decoded.samples.tobytes()

    # 初始化 PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=decoded.nchannels,
        rate=decoded.sample_rate,
        output=True,
        output_device_index=deviceindex
    )

    # 分块播放（确保块大小是帧的整数倍）
    frame_size = decoded.nchannels * decoded.sample_width  # 每帧字节数
    chunk_size = 4096 * frame_size  # 动态计算块大小sa
    for i in range(0, len(pcm_bytes), chunk_size):
        stream.write(pcm_bytes[i:i+chunk_size])

    # 清理资源
    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == "__main__":
    # stream_tts_audio("这个是我的测试音频，能直接把文字转成语音",deviceindex=21)
    libre_tts_audio("愿我不在的日子里 ，祝你早上、中午、下午、晚上好",language='wuu',deviceindex=21)
