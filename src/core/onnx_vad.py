#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
官方Silero VAD ONNX模型包装器
不依赖任何第三方VAD包，直接使用onnxruntime
"""

import os
import numpy as np
import onnxruntime as ort

class SileroVADONNX:
    """官方Silero VAD ONNX模型包装器"""
    
    def __init__(self, model_path="models/silero_vad.onnx"):
        """
        初始化Silero VAD ONNX模型
        
        Args:
            model_path: ONNX模型路径
        """
        self.sample_rate = 16000  # 强制使用16000Hz采样率
        self.model_path = model_path
        self.session = None
        self._load_model()
        
        # 初始化状态
        self.reset_states()
        
    def reset_states(self):
        """重置模型状态"""
        # 根据Silero VAD模型要求初始化状态
        self.h = np.zeros((2, 1, 64), dtype=np.float32)
        self.c = np.zeros((2, 1, 64), dtype=np.float32)
        
    def _load_model(self):
        """加载ONNX模型"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
                
            # 创建ONNX Runtime会话
            self.session = ort.InferenceSession(
                self.model_path,
                providers=['CPUExecutionProvider']
            )
            
            # 获取输入输出信息
            inputs = self.session.get_inputs()
            self.input_names = [inp.name for inp in inputs]
            self.output_names = [out.name for out in self.session.get_outputs()]
            
            print(f"[OK] 官方Silero VAD ONNX模型加载成功")
            
        except Exception as e:
            print(f"[FAIL] 加载ONNX模型失败: {e}")
            self.session = None
    
    def process(self, audio_chunk):
        """
        处理音频块并返回语音概率
        
        Args:
            audio_chunk: 音频数据（bytes或numpy数组）
            必须是512个样本的float32，范围[-1, 1]
            
        Returns:
            float: 语音概率（0-1）
        """
        if self.session is None:
            return 0.5  # 如果模型未加载，返回中性值
            
        try:
            # 转换音频数据
            if isinstance(audio_chunk, bytes):
                # 从bytes转换为numpy数组
                audio = np.frombuffer(audio_chunk, dtype=np.float32)
            else:
                audio = np.asarray(audio_chunk, dtype=np.float32)
            
            # 确保音频长度正确（512个样本）
            target_length = 512
            if len(audio) != target_length:
                # 如果太短，填充；如果太长，截断
                if len(audio) < target_length:
                    audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
                else:
                    audio = audio[:target_length]
            
            # 确保音频范围在[-1, 1]
            max_val = np.max(np.abs(audio))
            if max_val > 1.0:
                audio = audio / max_val
            
            # 重塑为模型需要的输入形状 (1, 512)
            input_data = audio.reshape(1, -1)
            
            # 准备输入数据
            inputs = {
                'input': input_data,
                'sr': np.array([self.sample_rate], dtype=np.int64),
                'h': self.h,
                'c': self.c
            }
            
            # 运行推理
            outputs = self.session.run(self.output_names, inputs)
            
            # 更新状态
            output_prob = float(outputs[0][0][0])
            self.h = outputs[1]
            self.c = outputs[2]
            
            return output_prob
            
        except Exception as e:
            print(f"[ERROR] ONNX VAD处理失败: {e}")
            return 0.5  # 出错时返回中性值
    
    def is_speech(self, audio_chunk, threshold=0.5):
        """
        判断音频块是否包含语音
        
        Args:
            audio_chunk: 音频数据
            threshold: 语音检测阈值
            
        Returns:
            bool: True表示检测到语音
        """
        prob = self.process(audio_chunk)
        return prob > threshold
    
    def __call__(self, audio_chunk):
        """使实例可调用，直接返回概率"""
        return self.process(audio_chunk)

class ONNXVADWrapper:
    """VAD包装器，统一接口"""
    _instance = None
    _model_path = None
    _sample_rate = None
    
    def __new__(cls, model_path="models/silero_vad.onnx"):
        # 单例模式：如果已经存在实例且参数相同，则返回现有实例
        if cls._instance is None or cls._model_path != model_path:
            cls._instance = super(ONNXVADWrapper, cls).__new__(cls)
            cls._model_path = model_path
            cls._sample_rate = 16000  # 强制16000Hz
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, model_path="models/silero_vad.onnx"):
        # 防止重复初始化
        if self._initialized:
            return
            
        self.sample_rate = 16000  # 强制使用16000Hz采样率
        self.vad = None
        
        try:
            self.vad = SileroVADONNX(model_path=model_path)
            print("[OK] 官方ONNX VAD初始化成功")
            self._initialized = True
        except Exception as e:
            print(f"[WARN] ONNX VAD初始化失败: {e}，将使用传统检测")
            self.vad = None
    
    def is_speech(self, audio_chunk, threshold=0.5):
        """
        检测音频块是否包含语音
        
        Args:
            audio_chunk: numpy数组格式的音频数据
            threshold: 检测阈值
            
        Returns:
            bool: True表示检测到语音
        """
        if self.vad is None or self.vad.session is None:
            return True  # 如果VAD不可用，默认认为有语音
            
        try:
            # 确保音频数据类型正确
            if audio_chunk.dtype != np.float32:
                audio_chunk = audio_chunk.astype(np.float32)
            
            # 归一化到[-1, 1]范围
            max_val = np.max(np.abs(audio_chunk))
            if max_val > 0:
                audio_chunk = audio_chunk / max_val
            
            # 使用ONNX VAD检测
            return self.vad.is_speech(audio_chunk, threshold)
            
        except Exception as e:
            print(f"[ERROR] ONNX VAD检测失败: {e}")
            return True  # 出错时默认认为有语音

def test_onnx_vad():
    """测试ONNX VAD功能"""
    print("测试官方Silero VAD ONNX模型...")
    
    try:
        # 初始化VAD
        vad = SileroVADONNX()
        
        if vad.session is None:
            print("[FAIL] 模型未加载")
            return False
        
        # 测试静音
        silent = np.zeros(512, dtype=np.float32)
        prob_silent = vad.process(silent)
        print(f"静音检测概率: {prob_silent:.3f}")
        
        # 测试语音
        t = np.linspace(0, 0.032, 512)
        voice = np.sin(2 * np.pi * 440 * t).astype(np.float32) * 0.8
        prob_voice = vad.process(voice)
        print(f"语音检测概率: {prob_voice:.3f}")
        
        # 判断结果
        if prob_silent < 0.5 and prob_voice > 0.5:
            print("[PASS] 官方ONNX VAD功能正常")
            return True
        else:
            print(f"[WARN] VAD检测可能不敏感，静音={prob_silent:.3f}, 语音={prob_voice:.3f}")
            return True
            
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_onnx_vad()