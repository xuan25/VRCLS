import baiduAPI as fanyi




result_ru = fanyi.translate_text('Hello',from_=fanyi.Lang.EN, to=fanyi.Lang.ZH)
print(result_ru)
# # 你好，世界！ Здравствуйте, Мир!

lang = fanyi.detect_language(' Здравствуйте Hello')
print(lang)
# # True

# result = fanyi.translate_text('我们是中国人，我们爱自己的祖国！')
# print(result)
# # We are Chinese, we love our motherland!

# # result_common = fanyi.translate_text('年化收益率')
# # result_domain = fanyi.translate_text('年化收益率', domain=fanyi.Domain.FINANCE) # 金融
# # print(result_common, '&', result_domain)
# # Annualized rate of return & Annualized yield


