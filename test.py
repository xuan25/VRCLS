def format_to_8x16(s:str):

    lines = s.split('\n')  # 按换行符分割原始字符串
    # 处理每一行：截断到16字符并用空格补齐
    processed = [line[:16].ljust(16) for line in lines]
    # 确保最多取8行，不足则补全空行
    processed = processed[:8] + [' ' * 16] * (8 - len(processed[:8]))
    # 拼接所有行成一个字符串
    return ''.join(processed)

input_str = "abc12311312312312341231\n123\n3\n4\n5\n6\n7\n8\n9\n10"
output = format_to_8x16(input_str)
print(repr(output))  # 查看实际拼接结果（包含空格）