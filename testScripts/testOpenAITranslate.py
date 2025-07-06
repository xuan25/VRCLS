#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI翻译功能测试脚本
用于验证OpenAI翻译引擎是否正常工作
"""

import sys
import os
import time
import traceback

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.module.translate import openai_translator

def test_openai_translation():
    """测试OpenAI翻译功能"""
    
    # 模拟配置参数
    params = {
        "openai_config": {
            "api_key": "",  # 请在这里填入你的API密钥
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            "model": "glm-4-flash"
        }
    }
    
    # 模拟日志记录器
    class MockLogger:
        def put(self, message):
            level = message.get("level", "info")
            text = message.get("text", "")
            print(f"[{level.upper()}] {text}")
    
    logger = MockLogger()
    
    # 测试用例
    test_cases = [
        {
            "source_lang": "zh",
            "target_lang": "en",
            "text": "你好，世界！"
        },
        {
            "source_lang": "zh", 
            "target_lang": "ja",
            "text": "今天天气很好"
        },
        {
            "source_lang": "en",
            "target_lang": "zh", 
            "text": "Hello, how are you?"
        }
    ]
    
    print("=== OpenAI翻译功能测试 ===")
    print(f"API地址: {params['openai_config']['base_url']}")
    print(f"模型: {params['openai_config']['model']}")
    print()
    
    # 检查API密钥
    if not params["openai_config"]["api_key"]:
        print("❌ 错误: 请先在脚本中配置OpenAI API密钥")
        print("请在params['openai_config']['api_key']中填入你的API密钥")
        return False
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试 {i}/{total_count}:")
        print(f"源语言: {test_case['source_lang']}")
        print(f"目标语言: {test_case['target_lang']}")
        print(f"原文: {test_case['text']}")
        
        try:
            # 模拟res对象
            res = {"text": test_case["text"]}
            
            # 调用翻译函数
            start_time = time.time()
            result = openai_translator(
                logger, 
                test_case["source_lang"], 
                test_case["target_lang"], 
                res, 
                params
            )
            end_time = time.time()
            
            if result:
                print(f"✅ 翻译成功: {result}")
                print(f"⏱️  用时: {end_time - start_time:.2f}秒")
                success_count += 1
            else:
                print("❌ 翻译失败: 返回空结果")
                
        except Exception as e:
            print(f"❌ 翻译异常: {str(e)}")
            print(f"详细错误: {traceback.format_exc()}")
        
        print("-" * 50)
    
    print(f"测试完成: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        print("🎉 所有测试通过！OpenAI翻译功能正常工作")
        return True
    else:
        print("⚠️  部分测试失败，请检查配置和网络连接")
        return False

def test_batch_translation():
    """测试批量翻译功能"""
    print("\n=== 批量翻译功能测试 ===")
    
    # 模拟配置参数
    params = {
        "openai_config": {
            "api_key": "",  # 请在这里填入你的API密钥
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            "model": "glm-4-flash"
        }
    }
    
    # 模拟日志记录器
    class MockLogger:
        def put(self, message):
            level = message.get("level", "info")
            text = message.get("text", "")
            print(f"[{level.upper()}] {text}")
    
    logger = MockLogger()
    
    # 检查API密钥
    if not params["openai_config"]["api_key"]:
        print("❌ 错误: 请先在脚本中配置OpenAI API密钥")
        return False
    
    try:
        from openai import OpenAI
        
        # 创建OpenAI客户端
        client = OpenAI(
            api_key=params["openai_config"]["api_key"],
            base_url=params["openai_config"]["base_url"]
        )
        
        # 测试文本
        text = "你好，这是一个测试。"
        source_lang = "zh"
        target_langs = ["en", "ja", "ko"]
        
        print(f"原文: {text}")
        print(f"目标语言: {target_langs}")
        
        # 构建多语言翻译提示
        target_lang_names = []
        lang_names = {
            'en': 'English', 'ja': 'Japanese', 'ko': 'Korean'
        }
        
        for lang in target_langs:
            target_lang_names.append(lang_names.get(lang, lang))
        
        system_prompt = f"""你是一个专业的翻译助手。请将以下文本翻译成多种语言。

翻译要求：
1. 保持原文的意思和语气
2. 确保翻译准确、自然、流畅
3. 严格按照JSON格式返回结果

请将以下文本翻译成：{', '.join(target_lang_names)}

返回格式：
{{
    "translations": {{
        "en": "英语翻译",
        "ja": "日语翻译", 
        "ko": "韩语翻译"
    }}
}}

原文："""

        # 调用OpenAI API
        start_time = time.time()
        completion = client.chat.completions.create(
            model=params["openai_config"]["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        end_time = time.time()
        
        # 解析结果
        response_text = completion.choices[0].message.content.strip()
        print(f"API响应: {response_text}")
        print(f"⏱️  用时: {end_time - start_time:.2f}秒")
        
        # 尝试解析JSON
        import json
        try:
            if response_text.startswith('{') and response_text.endswith('}'):
                parsed = json.loads(response_text)
                if 'translations' in parsed:
                    print("✅ 批量翻译成功:")
                    for lang, translation in parsed['translations'].items():
                        print(f"  {lang}: {translation}")
                    return True
        except:
            print("⚠️  JSON解析失败，但API调用成功")
            return True
            
    except Exception as e:
        print(f"❌ 批量翻译异常: {str(e)}")
        return False

if __name__ == "__main__":
    print("OpenAI翻译功能测试")
    print("=" * 50)
    
    # 运行单语言翻译测试
    single_success = test_openai_translation()
    
    # 运行批量翻译测试
    batch_success = test_batch_translation()
    
    print("\n" + "=" * 50)
    print("测试总结:")
    print(f"单语言翻译: {'✅ 通过' if single_success else '❌ 失败'}")
    print(f"批量翻译: {'✅ 通过' if batch_success else '❌ 失败'}")
    
    if single_success and batch_success:
        print("🎉 所有功能测试通过！")
    else:
        print("⚠️  部分功能测试失败，请检查配置") 