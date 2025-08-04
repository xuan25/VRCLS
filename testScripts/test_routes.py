import os
import sys
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 检查构建后的文件
print("=== 检查前端构建文件 ===")

# 检查templates目录
templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
print(f"Templates路径: {templates_path}")

if os.path.exists(templates_path):
    files = os.listdir(templates_path)
    print(f"Templates目录文件: {files}")
    
    # 检查index.html
    index_path = os.path.join(templates_path, 'index.html')
    if os.path.exists(index_path):
        print("[OK] index.html 存在")
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'overlay' in content.lower():
                print("[OK] overlay相关内容在index.html中找到")
            else:
                print("[WARN] overlay内容未在index.html中找到")
    else:
        print("[ERROR] index.html 不存在")
else:
    print("[ERROR] templates目录不存在")

# 检查Vue Router配置
print("\n=== 检查Vue Router配置 ===")
router_path = os.path.join(os.path.dirname(__file__), '..', 'webUI', 'src', 'router', 'index.js')
if os.path.exists(router_path):
    print("[OK] router/index.js 存在")
    with open(router_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if '/overlay' in content:
            print("[OK] /overlay 路由已配置")
        else:
            print("[ERROR] /overlay 路由未找到")
else:
    print("[ERROR] router/index.js 不存在")

# 检查Overlay.vue组件
print("\n=== 检查Overlay组件 ===")
overlay_path = os.path.join(os.path.dirname(__file__), '..', 'webUI', 'src', 'views', 'Overlay.vue')
if os.path.exists(overlay_path):
    print("[OK] Overlay.vue 存在")
    with open(overlay_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'micResults' in content and 'capResults' in content:
            print("[OK] 麦克风/桌面音频结果显示组件已配置")
        else:
            print("[WARN] 组件内容可能不完整")
else:
    print("[ERROR] Overlay.vue 不存在")

print("\n=== 测试完成 ===")
print("要测试overlay功能，请:")
print("1. 启动主程序: python main.py")
print("2. 访问: http://127.0.0.1:8980/#/overlay")
print("3. 或在浏览器中测试: http://127.0.0.1:8980/#/overlay")