import os
import hashlib
import shutil

def get_file_info(folder):
    """递归获取文件夹内所有文件的相对路径和哈希值"""
    file_dict = {}
    for root, _, files in os.walk(folder):
        rel_path = os.path.relpath(root, folder)
        for file in files:
            file_path = os.path.join(root, file)
            rel_file = os.path.join(rel_path, file).replace('\\', '/')
            # 计算文件哈希（可选）
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            file_dict[rel_file] = file_hash
    return file_dict

def copy_new_files(src_folder, dst_folder):
    """复制源文件夹中存在但目标文件夹缺失的文件"""
    src_files = get_file_info(src_folder)
    dst_files = get_file_info(dst_folder)

    for rel_file, file_hash in src_files.items():
        dst_file_path = os.path.join(dst_folder, rel_file)
        if rel_file not in dst_files:  # 新增文件
            src_file_path = os.path.join(src_folder, rel_file)
            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
            shutil.copy2(src_file_path, dst_file_path)
            print(f'Copied: {rel_file}')
        elif src_files[rel_file] != dst_files[rel_file]:  # 内容不同的文件
            print(f'Modified (not copied): {rel_file}')

# 使用示例
copy_new_files('D:\git\gitlab\VRCLS\dist\VRCLS-windwos-v0.5.3\VRCLS\_internal', 'D:\git\gitlab\VRCLS\dist\VRCLS\_internal')
