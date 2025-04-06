import translators as ts
import time
import traceback
traceback.format_exc()
q_text = '测试一下'
q_html = '''<!DOCTYPE html><html><head><title>《季姬击鸡记》</title></head><body><p>还有另一篇文章《施氏食狮史》。</p></body></html>'''

### usage
# _ = ts.preaccelerate_and_speedtest()  # Optional. Caching sessions in advance, which can help improve access speed.

print(ts.translators_pool)
st=time.time()
print(ts.translate_text(q_text,translator='google'))
et=time.time()
print(et-st)
# print(ts.translate_html(q_html, translator='alibaba'))

### parameters
# help(ts.translate_text)