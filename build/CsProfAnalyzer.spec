# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
import os

# Ensure the src directory is in the path
sys.path.append(os.path.abspath('../src'))

def get_requirements():
    try:
        with open('../src/cs_prof_analyzer/requirements.txt', 'r') as f:
            reqs = []
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                name = re.split(r'==|>=|<=', line)[0].strip()
                if name:
                    reqs.append(name)
            return reqs
    except FileNotFoundError:
        return []

reqs = get_requirements()
hidden = []
# Ensure locale and config are correctly referenced
datas = [('../src/cs_prof_analyzer/core/locale', 'core/locale'), ('../src/cs_prof_analyzer/config.json', '.')]

for r in reqs:
    hidden += collect_submodules(r)
    datas += collect_data_files(r)

a = Analysis(
    ['../src/cs_prof_analyzer/cs_prof_analyzer.py'],
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
