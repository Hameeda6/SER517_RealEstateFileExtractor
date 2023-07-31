# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['HomePage.py'],
    pathex=[],
    binaries=[],
    datas=[('/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/selenium', './selenium'), ('/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/chromedriver', '.'), ('/Users/sarfraz/Desktop/Projects/SER517_Team5_RealEstate_Spring2023/TenantCloud.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HomePage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='HomePage.app',
    icon=None,
    bundle_identifier=None,
)
