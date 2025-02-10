import pyttsx3

# 初始化 pyttsx3 引擎
engine = pyttsx3.init()

# 要转换的文本
text = "process started complete 音频进程启动完毕"

# 播放文本
engine.say(text)

# 等待语音播放完毕
engine.runAndWait()
