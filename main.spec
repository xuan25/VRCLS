# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os  # 新增导入

# ======================= 正确收集模型文件的函数 =======================
def collect_models(root_dir):
    models = []
    for root, _, files in os.walk(root_dir):
        rel_path = os.path.relpath(root, root_dir)
        for file in files:
            src_file = os.path.join(root, file)
            dest_dir = os.path.join('sherpa-onnx-models', rel_path)
            models.append( (src_file, dest_dir) )  # 正确路径格式
    return models

datas = []
binaries = []
hiddenimports = []

tmp_ret = collect_all('requests')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('zeroconf')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('openvr')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('py7zr')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
datas.append(('templates','templates'))
datas.append(('ffmpeg/bin/*', 'ffmpeg/bin'))
datas += collect_models('sherpa-onnx-models')  # 递归打包整个目录树
datas.append(('font/*', 'font'))
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VRCLS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VRCLS',
)
