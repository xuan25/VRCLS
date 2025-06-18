import cv2
import numpy as np
import os

def get_hsv_color_range_for_solid_color(bgr_color_tuple,
                                        h_tolerance=10,
                                        s_tolerance_for_color=70,  # 对彩色而言
                                        v_tolerance_for_color=70,  # 对彩色而言
                                        s_max_for_grayscale=50,    # 灰度色的最大饱和度
                                        v_tolerance_for_grayscale=70 # 灰度色的亮度容差
                                        ):
    """
    根据BGR颜色计算合适的HSV颜色范围。
    特别处理灰度色（如白色、灰色、黑色）。
    """
    b, g, r = bgr_color_tuple
    color_bgr_np = np.uint8([[[b, g, r]]]) # 转换为numpy数组格式
    hsv_color = cv2.cvtColor(color_bgr_np, cv2.COLOR_BGR2HSV)[0][0]
    h_orig, s_orig, v_orig = hsv_color[0], hsv_color[1], hsv_color[2]

    print(f"目标BGR: {bgr_color_tuple} -> 目标HSV: [{h_orig}, {s_orig}, {v_orig}]")

    # 判断是否为灰度色 (R, G, B分量非常接近，或者S值本身就很低)
    # 对于灰度色，H分量不重要，S分量很低
    is_grayscale = (abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20) or s_orig < 30 # s_orig < 30 是一个经验值

    if is_grayscale:
        print("识别为灰度色或接近灰度色。")
        # H (色调): 对于灰度色，H不敏感，可以取整个范围
        lower_h, upper_h = 0, 179
        # S (饱和度): 灰度色的饱和度很低
        lower_s, upper_s = 0, s_max_for_grayscale
        # V (亮度):
        lower_v = max(0, v_orig - v_tolerance_for_grayscale)
        upper_v = min(255, v_orig + v_tolerance_for_grayscale)
    else:
        print("识别为彩色。")
        # H (色调)
        lower_h = max(0, h_orig - h_tolerance)
        upper_h = min(179, h_orig + h_tolerance)
        # S (饱和度)
        lower_s = max(0, s_orig - s_tolerance_for_color)
        upper_s = min(255, s_orig + s_tolerance_for_color)
        # V (亮度)
        lower_v = max(0, v_orig - v_tolerance_for_color)
        upper_v = min(255, v_orig + v_tolerance_for_color)

        # 特殊处理H值环绕 (例如红色，H值接近0或179)
        # 如果 lower_h > upper_h, 说明原始h值接近0或179，且容差导致跨界
        # 例如: h_orig=5, h_tolerance=10 -> lower_h_calc = -5, upper_h_calc = 15
        # 此时，我们期望的范围是 [0, 15] 和 [170, 179]
        # cv2.inRange 不直接支持这种分离的范围，需要特殊处理
        # 为简化，这里如果发生环绕，我们会打印一个警告，用户可能需要手动调整或使用两个mask
        if h_orig - h_tolerance < 0 and h_orig + h_tolerance > 179: # 不太可能同时发生
             pass # 逻辑上不会出现
        elif h_orig - h_tolerance < 0: # 例如 H=5, tol=10, 期望 [0,15] U [175,179]
            # 这里简单处理为 [0, h_orig + h_tolerance]
            # 更精确的做法是创建两个mask
            print(f"警告: H值下限环绕 (原始H={h_orig}, 容差={h_tolerance})。 HSV范围可能不精确。考虑手动调整或使用两个mask。")
            # lower_h = 0 # 已经max(0,...)处理了
        elif h_orig + h_tolerance > 179: # 例如 H=175, tol=10, 期望 [0,5] U [165,179]
            print(f"警告: H值上限环绕 (原始H={h_orig}, 容差={h_tolerance})。 HSV范围可能不精确。考虑手动调整或使用两个mask。")
            # upper_h = 179 # 已经min(179,...)处理了


    lower_bound = np.array([lower_h, lower_s, lower_v])
    upper_bound = np.array([upper_h, upper_s, upper_v])

    print(f"计算得到的HSV范围: Lower={lower_bound}, Upper={upper_bound}")
    return lower_bound, upper_bound


def extract_solid_color_chat_bubbles(image_path,
                                     chat_bg_bgr_color,
                                     output_dir="cropped_solid_bubbles",
                                     min_contour_area=500,
                                     padding=10,
                                     h_tol=10, s_tol_color=60, v_tol_color=60, # 彩色容差
                                     s_max_gray=60, v_tol_gray=60,         # 灰度色容差
                                     morph_kernel_size=(7,7),
                                     close_iterations=3,
                                     open_iterations=1):
    """
    从图片中提取具有指定纯色背景的聊天框。
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误: 无法加载图片 '{image_path}'")
        return

    # 1. 获取目标颜色的HSV范围
    lower_hsv, upper_hsv = get_hsv_color_range_for_solid_color(
        chat_bg_bgr_color,
        h_tolerance=h_tol,
        s_tolerance_for_color=s_tol_color, v_tolerance_for_color=v_tol_color,
        s_max_for_grayscale=s_max_gray, v_tolerance_for_grayscale=v_tol_gray
    )

    # 2. 转换到HSV并创建颜色掩码
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)

    # (可选，用于调试) 显示原始掩码
    cv2.imshow("Original Mask", mask)
    # cv2.waitKey(0)

    # 3. 形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_kernel_size)
    # 闭运算：填充聊天框内部因文字等造成的空洞
    mask_processed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=close_iterations)
    # 开运算：去除小的噪点区域（如果聊天框非常小，此步骤要谨慎或减少迭代）
    if open_iterations > 0:
        mask_processed = cv2.morphologyEx(mask_processed, cv2.MORPH_OPEN, kernel, iterations=open_iterations)

    # (可选，用于调试) 显示处理后的掩码
    cv2.imshow("Processed Mask", mask_processed)
    # cv2.waitKey(0)

    # 4. 查找轮廓
    contours, _ = cv2.findContours(mask_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 5. 筛选轮廓并截取
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cropped_count = 0
    img_with_boxes = img.copy() # 用于可视化

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > min_contour_area:
            x, y, w, h = cv2.boundingRect(contour)

            # (可选) 可以添加基于长宽比的过滤
            # aspect_ratio = w / float(h)
            # if aspect_ratio < 0.2 or aspect_ratio > 5: # 举例：过滤掉过于细长或扁平的区域
            #     continue

            # 应用padding
            x_padded = max(0, x - padding)
            y_padded = max(0, y - padding)
            # 确保宽度和高度加上padding后不超过图像边界
            w_padded = min(img.shape[1] - x_padded, w + 2 * padding)
            h_padded = min(img.shape[0] - y_padded, h + 2 * padding)

            # 从原始彩色图片中截取
            cropped_bubble = img[y_padded:y_padded + h_padded, x_padded:x_padded + w_padded]

            save_path = os.path.join(output_dir, f"bubble_{cropped_count}.png")
            cv2.imwrite(save_path, cropped_bubble)
            print(f"已保存: {save_path} (面积: {area})")

            # 在可视化图像上绘制边界框
            cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped_count += 1

    print(f"共找到并截取了 {cropped_count} 个潜在的聊天框。")

    # 显示带有边界框的原始图片 (调试用)
    if cropped_count > 0:
        cv2.imshow("Chat Image with Bounding Boxes", img_with_boxes)
    else:
        print("没有找到符合条件的聊天框。可以尝试调整颜色容差或形态学参数。")
        cv2.imshow("Original Chat Image (No Detections)", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # --- 请用户修改以下参数 ---
    image_file_path = "./testScripts/1223456.png"  # 替换为你的聊天图片路径

    # 指定聊天框的纯色背景 (BGR格式: Blue, Green, Red)
    # 你可以使用任何图像编辑软件的颜色拾取器来获取这个值。
    # 例如:
    # 白色: (255, 255, 255)
    # 浅灰色: (240, 240, 240)
    # 微信聊天气泡绿色 (近似): (149, 236, 105) # 这是发送方气泡
    # 微信聊天气泡白色 (近似): (255, 255, 255) # 这是接收方气泡
    # 某个应用的特定蓝色: (26, 115, 232)
    chat_bubble_background_bgr = (82, 65, 52) # 假设聊天框背景是这种浅灰色

    output_directory = "extracted_chat_bubbles"

    # --- 参数调整区 ---
    # HSV 颜色容差 (根据实际情况调整)
    h_tolerance = 10         # 色调容差 (0-179)。对于灰度色，此值影响不大。
    s_tolerance_color = 30   # 彩色的饱和度容差 (0-255)。
    v_tolerance_color = 30   # 彩色的亮度容差 (0-255)。
    s_max_for_grayscale = 60 # 识别为灰度色的最大饱和度。灰度色饱和度很低。
    v_tolerance_grayscale = 10# 灰度色的亮度容差。

    min_area = 500          # 识别为聊天框的最小轮廓面积 (像素)
    padding_pixels = 5      # 裁剪时向外扩展的像素数

    # 形态学操作参数 (非常重要，需要根据聊天框内文字/图标情况调整)
    kernel_sz = (7, 7)      # 核大小，影响填充和去噪的程度
    close_iter_count = 3    # 闭运算迭代次数，用于填充聊天框内部的空洞
    open_iter_count = 1     # 开运算迭代次数，用于去除外部的小噪点 (如果聊天框本身小，可以设为0或1)

    # 检查图片文件是否存在
    if not os.path.exists(image_file_path):
        print(f"错误: 图片 '{image_file_path}' 不存在。请创建或指定正确路径。")
        # 可以生成一个示例图片帮助测试
        # img_h, img_w = 600, 800
        # example_img = np.full((img_h, img_w, 3), (80, 70, 60), dtype=np.uint8) # 暗色背景
        # bubble_b, bubble_g, bubble_r = chat_bubble_background_bgr
        # cv2.rectangle(example_img, (50, 50), (300, 150), (bubble_b, bubble_g, bubble_r), -1)
        # cv2.putText(example_img, "Hello there!", (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        # cv2.rectangle(example_img, (img_w - 350, 200), (img_w - 50, 300), (bubble_b, bubble_g, bubble_r), -1)
        # cv2.putText(example_img, "This is a test.", (img_w - 340, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50,50,50), 2)
        # cv2.imwrite(image_file_path, example_img)
        # print(f"已创建示例图片: {image_file_path}，请用它测试或替换为你的图片。")
    else:
        extract_solid_color_chat_bubbles(
            image_path=image_file_path,
            chat_bg_bgr_color=chat_bubble_background_bgr,
            output_dir=output_directory,
            min_contour_area=min_area,
            padding=padding_pixels,
            h_tol=h_tolerance,
            s_tol_color=s_tolerance_color, v_tol_color=v_tolerance_color,
            s_max_gray=s_max_for_grayscale, v_tol_gray=v_tolerance_grayscale,
            morph_kernel_size=kernel_sz,
            close_iterations=close_iter_count,
            open_iterations=open_iter_count
        )