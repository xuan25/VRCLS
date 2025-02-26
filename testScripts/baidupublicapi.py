import baidu_translate as fanyi
from flask import Flask,request,jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wVddL213dsdddN6XL_QmP.DjkKsV'

@app.route('/api/login', methods=['POST'])
def aa():
    data = request.get_json()

    result = fanyi.translate_text('Hello, World!')
    result_ru = fanyi.translate_text('Hello, World!', from_=fanyi.Lang.ZH,to=fanyi.Lang.RU)
# print(result, result_ru)
# # 你好，世界！ Здравствуйте, Мир!

# lang = fanyi.detect_language('Vue rapide')
# print(lang == fanyi.Lang.FRA)
# # True

# result = fanyi.translate_text('我们是中国人，我们爱自己的祖国！')
# print(result)
# # We are Chinese, we love our motherland!

# # result_common = fanyi.translate_text('年化收益率')
# # result_domain = fanyi.translate_text('年化收益率', domain=fanyi.Domain.FINANCE) # 金融
# # print(result_common, '&', result_domain)
# # Annualized rate of return & Annualized yield


