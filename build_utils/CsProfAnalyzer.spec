# -*- mode: python ; coding: utf-8 -*-
import sys
import os

# Ensure the src directory is in the path for resolution
sys.path.append(os.path.abspath('../src'))

# PyInstaller automatically detects imports installed in the current environment
# We only need to specify data files that are not automatically detected
a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('../src/locale', 'locale'), ('../src/config.json', '.')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='CsProfAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
