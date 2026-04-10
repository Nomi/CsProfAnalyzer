# -*- mode: python ; coding: utf-8 -*-
import sys
import os

# Ensure the src directory is in the path
sys.path.append(os.path.abspath('../src'))

# PyInstaller will automatically detect imports from the active venv/site-packages
a = Analysis(
    ['../src/cs_prof_analyzer/cs_prof_analyzer.py'],
    pathex=[],
    binaries=[],
    datas=[('../src/cs_prof_analyzer/core/locale', 'core/locale'), ('../src/cs_prof_analyzer/config.json', '.')],
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
