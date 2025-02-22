"""基于WASAPI环回设备的智能语音激活识别（内存流版）"""

import pyaudiowpatch as pyaudio
import numpy as np
import speech_recognition as sr
from src.module.ffmpegInit import import_ffmpeg
# 必须在所有音频操作之前调用
AudioSegment=import_ffmpeg()
from io import BytesIO
import threading,sys,os



def stream_to_text(audio_stream, sample_rate, channels, sample_width, engine="google", language="zh-CN"):
    """将音频流直接转换为文字"""
    r = sr.Recognizer()
    
    try:
        # 使用pydub处理内存中的音频数据
        audio = AudioSegment.from_raw(
            BytesIO(audio_stream),
            sample_width=sample_width,
            frame_rate=sample_rate,
            channels=channels
        )
        # 统一转换为单声道16kHz
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # 转换为speech_recognition需要的格式
        with BytesIO() as bio:
            audio.export(bio, format="wav")
            bio.seek(0)
            with sr.AudioFile(bio) as source:
                audio_data = r.record(source)

            if engine == "google":
                return r.recognize_google(audio_data, language=language)
            elif engine == "whisper":
                return r.recognize_whisper(audio_data, language=language)
            else:
                raise ValueError("不支持的识别引擎")
                
    except sr.UnknownValueError:
        return "无法识别音频内容"
    except sr.RequestError as e:
        return f"服务请求失败: {str(e)}"
    except Exception as e:
        return f"处理失败: {str(e)}"
def stream_to_audioData(audio_stream, sample_rate, channels, sample_width):
    """将音频流直接转换为文字"""
    r = sr.Recognizer()
    
    try:
        # 使用pydub处理内存中的音频数据
        audio = AudioSegment.from_raw(
            BytesIO(audio_stream),
            sample_width=sample_width,
            frame_rate=sample_rate,
            channels=channels
        )
        # 统一转换为单声道16kHz
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # 转换为speech_recognition需要的格式
        with BytesIO() as bio:
            audio.export(bio, format="wav")
            bio.seek(0)
            with sr.AudioFile(bio) as source:
                return r.record(source)

                

    except Exception as e:
        return f"处理失败: {str(e)}"
def voice_activation_stream(
    logger=None,
    micIndex=None,
    silence_threshold=500,
    silence_duration=1,
    pre_record_buffer=2,
    chunk=1024,
    format=pyaudio.paInt16,
    output="audio",  # audio,text
    timeout=5.0,
    maxAudioLen=30.0,
    **kwargs
) -> str | sr.AudioData:
    """语音激活识别（直接返回文本）"""
    if logger is None:
        printText = print
    else:
        printText = logger.put
    try:
        with pyaudio.PyAudio() as p:
            device_info = p.get_default_wasapi_loopback() if micIndex is None else p.get_device_info_by_index(micIndex)
            printText({"text": f"使用桌面音频{str(device_info)}秒，停止识别", "level": "debug"})
            rate = int(device_info["defaultSampleRate"])
            channels = device_info["maxInputChannels"]
            sample_width = p.get_sample_size(format)

            silence_limit = int(rate / chunk * silence_duration)
            pre_buffer_size = int(rate / chunk * pre_record_buffer)

            with p.open(
                format=format,
                channels=channels,
                rate=rate,
                input=True,
                input_device_index=device_info["index"],
            ) as stream:
                audio_buffer = bytearray()
                pre_record = bytearray()
                is_recording = False
                silence_count = 0
                timeout_event = threading.Event()  # 超时事件标志
                tooLong_event = threading.Event()  # 超时事件标志

                try:
                    # 创建超时定时器
                    def on_timeout():
                        timeout_event.set()
                        printText({"text": f"桌面音频{timeout}秒内未检测到有效声音", "level": "debug"})
                    def on_tooLong():
                        tooLong_event.set()
                        printText({"text": f"桌面音频长度超过{maxAudioLen}s,截断", "level": "info"})

                    timer = threading.Timer(timeout, on_timeout)
                    timer.start()

                    timer2 = threading.Timer(maxAudioLen, on_tooLong)
                    

                    while True:
                        # 检查超时事件
                        if timeout_event.is_set():
                            raise sr.WaitTimeoutError(f"{timeout}秒内未检测到有效声音")

                        data = stream.read(chunk, exception_on_overflow=False)
                        audio = np.frombuffer(data, dtype=np.int16)

                        # 静音检测逻辑
                        rms = np.sqrt(np.mean(audio.astype(np.float64)**2)) if len(audio) > 0 else 0

                        if rms > silence_threshold:
                            if not is_recording:
                                timer2.start()
                                # 检测到声音时取消定时器
                                timer.cancel()
                                printText({"text": "桌面音频检测到声音，开始录制...", "level": "info"})
                                is_recording = True
                                audio_buffer.extend(pre_record)
                                pre_record.clear()
                            else:
                                if tooLong_event.is_set():
                                    audio_buffer.extend(data)
                                    silence_count += 1
                                    break
                            silence_count = 0
                            audio_buffer.extend(data)
                        else:
                            if is_recording:
                                audio_buffer.extend(data)
                                silence_count += 1
                                if silence_count >= silence_limit:
                                    timer2.cancel()
                                    printText({"text": f"桌面音频静音持续{silence_duration}秒，停止识别", "level": "debug"})
                                    break
                            else:
                                pre_record.extend(data)
                                if len(pre_record) > pre_buffer_size * chunk:
                                    del pre_record[:len(data)]

                except KeyboardInterrupt:
                    printText({"text": "桌面音频用户中断识别", "level": "debug"})
                
                finally:
                    timer.cancel()  # 确保定时器总是被取消
                    timer2.cancel()
                    if len(audio_buffer) > 0:
                        if output == "audio":
                            return stream_to_audioData(
                                bytes(audio_buffer),
                                sample_rate=rate,
                                channels=channels,
                                sample_width=sample_width,
                            )
                        else:
                            printText({"text": "开始语音识别...", "level": "info"})    
                            result = stream_to_text(
                                bytes(audio_buffer),
                                sample_rate=rate,
                                channels=channels,
                                sample_width=sample_width,
                                **kwargs
                            )
                            printText({"text": "\n识别结果：\n" + "-" * 40 + result + '\n' + "-" * 40, "level": "info"})   
                            return result
                    else:
                        printText({"text": "桌面音频未检测到有效语音输入", "level": "debug"}) 
#TODO 这里需要初始化错误后就暂停进程
    except (OSError, LookupError) as e:
        printText({"text": f"设备初始化失败: {str(e)}", "level": "warning"}) 
    except sr.WaitTimeoutError as e:
        raise  # 重新抛出超时异常
    except Exception as e:
        printText({"text": f"发生未知错误: {str(e)}", "level": "warning"}) 


if __name__ == "__main__":
    # # 示例用法
    # voice_activation_stream(
    #     silence_threshold=800,  # 根据环境噪音调整
    #     pre_record_buffer=1.5,  # 保存录音前1.5秒的音频
    #     engine="google",
    #     language="zh-CN"
    # )
    print(f"当前ffmpeg路径：{AudioSegment.converter}")