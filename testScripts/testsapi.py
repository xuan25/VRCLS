import speech_recognition as sr

def recognize_speech():
    # 创建识别器实例
    recognizer = sr.Recognizer()

    # 使用麦克风作为音频源
    with sr.Microphone() as source:
        print("请开始说话...（5秒超时）")
        recognizer.adjust_for_ambient_noise(source)  # 降噪
        
        try:
            # 监听并录制音频（超时时间为5秒）
            audio = recognizer.listen(source, timeout=5)
            print("识别中...")

            # 使用Windows SAPI进行识别
            text = recognizer.recognize_sapi(audio)
            print(f"识别结果: {text}")

        except sr.WaitTimeoutError:
            print("未检测到语音输入")
        except sr.UnknownValueError:
            print("无法识别语音内容")
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    recognize_speech()
