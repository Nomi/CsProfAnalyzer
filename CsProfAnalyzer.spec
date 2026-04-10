# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

def get_requirements():
    try:
        with open('requirements.txt', 'r') as f:
            return [line.strip().split('==')[0] for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

reqs = get_requirements()
hidden = []
datas = [('core/locale', 'core/locale'), ('config.json', '.')]

for r in reqs:
    hidden += collect_submodules(r)
    datas += collect_data_files(r)

a = Analysis(
    ['cs_prof_analyzer.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
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
