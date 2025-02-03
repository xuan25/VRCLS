from hanziconv import HanziConv

simplified_text = "繁体中文。"
traditional_text = HanziConv.toTraditional(simplified_text)
print(traditional_text)  # 输出: 這是一個測試。