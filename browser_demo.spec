# -*- mode: python ; coding: utf-8 -*-
import os

# 获取 Playwright 浏览器缓存路径 (通常是 %LOCALAPPDATA%\\ms-playwright)
# 注意：如果浏览器安装在其他位置，需要修改此路径
playwright_browser_cache = os.path.join(os.getenv('LOCALAPPDATA'), 'ms-playwright')
# 从错误信息中获取浏览器版本和目标路径结构
chromium_version_folder = 'chromium-1105' # 根据错误信息确定
chromium_src_path = os.path.join(playwright_browser_cache, chromium_version_folder)
chromium_dest_path = os.path.join('playwright', 'driver', 'package', '.local-browsers', chromium_version_folder)


a = Analysis(
    ['browser_demo.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('venv/Lib/site-packages/playwright/driver', 'playwright/driver'),
        (chromium_src_path, chromium_dest_path)
        ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='browser_demo',
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
    name='browser_demo',
)
