from openai import OpenAI 
import time
import base64
img_path = "./testScripts/1223456789.png"
with open(img_path, 'rb') as img_file:
    img_base = base64.b64encode(img_file.read()).decode('utf-8')

text="在本地部属一个大于模型，是个不合理的行为。"
client = OpenAI(
    api_key="4c3d963619884fc69e3a02c581925691.mgFDmvFyfDWmGvub",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
) 
# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key="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",
# )
st=time.time()
completion = client.chat.completions.create(
    # model="glm-4-flash-250414",  
    # model="glm-4-flashx",
    model="glm-4v-flash",
    # model="deepseek/deepseek-chat-v3-0324:free",
    messages=[    
            {"role": "system", "content":  """你是一个高级的语音识别文字后的翻译助手。你的任务是：
1. 修复收到的文字中存在的语音识别错误
2. 将修复后的文字翻译成英语。
3. 将修复后的文字翻译成日语。
3. 严格按照以下格式输出{"en":英语译文,"ja"：日语译文}
"""},    
        {"role": "user", "content": text} 
    ],    
#     messages=[    
            
#         {"role": "user","content": [
#           {
#             "type": "image_url",
#             "image_url": {
#                 "url": img_base
#             }
#           },
#           {
#             "type": "text",
            
#             "text": '''
# 你是一个图像分析AI。请分析我上传的图片。图片中有人物和相关的文本框。

# **框的类型和特征：**

# 1.  **ID框**：
#     *   单行文字。
#     *   位置：如果存在多个框，它在人物头顶框组的【最上方】。
#     *   内容：人物身份标识。
# 2.  **人称代词框**：
#     *   位置：通常在【ID框的右下方】。
#     *   内容：人称代词。
# 3.  **文本框**：
#     *   内容：主要对话或描述。
#     *   位置：框组的【最下方】（ID框和人称代词框之下），或【单独出现】在人物头上或前方。可以是单行或多行。

# **人物头顶框的可能组合：**
# *   只有【文本框】。
# *   【ID框】在【文本框】上方。
# *   【ID框】最上，【人称代词框】在ID框右下，【文本框】在最下方。

# **你需要执行的任务：**

# 1.  **识别所有文字**：
#     *   找出图片中的所有文字。
#     *   同一个框内的文字视为一段。

# 2.  **过滤内容**：
#     *   **严格去除**所有【ID框】和【人称代词框】内的文字。
#     *   **只保留**并处理【文本框】内的文字。

# 3.  **翻译文本框内容**：
#     *   将步骤2中保留的【文本框】内容，准确翻译成【简体中文】。

# 4.  **格式化输出**：
#     *   每段翻译后的文本输出为一行。
#     *   格式：`[标识符]: [翻译后的简体中文文本]`
#     *   **[标识符] 确定规则**：
#         *   **有ID框时**：如果该【文本框】上方明确关联着一个【ID框】，使用该【ID框】内的**原始文字**作为标识符。
#         *   **无ID框时**：如果【文本框】没有关联的【ID框】（例如只有文本框，或无法判断关联），则从图片最左边开始，按人物顺序编号，格式为 "人物1", "人物2", "人物3" 等。

# **重要提示：**
# *   请优先根据框的【相对位置】来判断其类型（ID框、人称代词框、文本框）。
# *   请确保输出格式的准确性。

# 请开始处理图片。
#             '''
# #  "text": '''
#              请执行以下任务：
#             1. 请识别出途中的所有文字，如果在一个框中的可以认为是一段
#             3. 将识别出的段翻译为中文
#             4. 将翻译后的文字的位置和内容描述出来
#             '''
            # "text": '''
            # 请执行以下任务：
            # 1. 请识别出图片中人物头上的聊天框中的文字
            # 2. 将识别到的文字翻译为英语
            
            # 请严格按照以下格式输出{"text":识别到的文字,"tranalted":英语译文}
            # '''
        #   }
        # ]} 
    # ],
    top_p=0.7,
    temperature=0.9
 ) 
et=time.time()
print(completion.choices[0].message)
print(completion.usage)
print(et-st)


st=time.time()
completion = client.chat.completions.create(
    model="glm-4-flash-250414",  
    messages=[    
            {"role": "system", "content":  """你是一个高级的语音识别文字后的翻译助手。你的任务是：
1. 修复收到的文字中存在的语音识别错误
2. 将修复后的文字翻译成ru。
3. 将修复后的文字翻译成ko。
3. 严格按照以下格式输出{"ru":英语译文,"ko"：日语译文}
"""},    
        {"role": "user", "content": text} 
    ],
    top_p=0.7,
    temperature=0.9
 ) 
et=time.time()
print(completion.choices[0].message)
print(et-st)
import os
os.environ["translators_default_region"] = "CN"
import translators,html
a=html.unescape(translators.translate_text(text,translator='bing',from_language='zh',to_language='en'))

st=time.time()
a=html.unescape(translators.translate_text(text,translator='youdao',from_language='zh',to_language='en'))
b=html.unescape(translators.translate_text(text,translator='youdao',from_language='zh',to_language='ja'))
et=time.time()
print(a)
print(b)
print(et-st)