import pyaudio
import requests
from pydub import AudioSegment
from io import BytesIO

def stream_tts_audio():
    # 发起 TTS 请求
    response = requests.post(
        'https://tts-test.boyqiu001.top/v1/audio/speech',
        json={
            "model": "tts-1",
            "input": "这是一段开心的话！",
            "voice": "zh-CN-XiaoxiaoNeural", 
            "style": "cheerful",
            "speed": 1.2
        },
        headers={
            "Authorization": "Bearer 0G~m6)^q1FPvKsAq2ENkcH,l7rP#5ka8&bNwkf=!dV24UGwPF6%s9Co+luH6,hDemQ4lKMuc-vFaGKc~OaxyeKHNk+pYfwEWq_Nv7IwR+%O5^EodMKotA=F,^Jf*F,q#fE.Rzgn59uRAMblK@,4xrO+yB.z*-s%S0lgNqkZ#J&N9h%LGF5Tyi8OWEBGd7MY7AYJH$g*Z"
        },
        stream=True  # 启用流式传输
    )

    # 验证响应状态
    if response.status_code != 200:
        raise Exception(f"TTS request failed with status {response.status_code}")

    # 创建内存缓冲区
    audio_buffer = BytesIO()
    
    # 流式接收数据
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            audio_buffer.write(chunk)
    
    # 重置缓冲区指针到起始位置
    audio_buffer.seek(0)

    # 解码 MP3 数据
    audio = AudioSegment.from_mp3(audio_buffer)
    pcm_data = audio.raw_data

    # 初始化 PyAudio
    p = pyaudio.PyAudio()
    
    # 打开音频流
    stream = p.open(
        format=p.get_format_from_width(audio.sample_width),
        channels=audio.channels,
        rate=audio.frame_rate,
        output=True
    )

    # 分块播放
    chunk_size = 1024
    for i in range(0, len(pcm_data), chunk_size):
        stream.write(pcm_data[i:i+chunk_size])

    # 清理资源
    stream.stop_stream()
    stream.close()
    p.terminate()
    audio_buffer.close()

if __name__ == "__main__":
    stream_tts_audio()
