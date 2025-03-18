import pyaudio
import numpy as np

# 音频参数设置
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# 创建PyAudio实例
p = pyaudio.PyAudio()

# 打开输出流（扬声器）
output_stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True
)

# 打开输入流（麦克风）
input_stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# 音频重定向（将输出直接送入输入）
while True:
    data = output_stream.read(CHUNK)
    input_stream.write(data)

# 注意：此方法需要同时具有音频输出和输入设备
