# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ["merger.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "pypdf",
        "pypdf._cmap",
        "pypdf._codecs",
        "pypdf._crypt_providers",
        "pypdf._encryption",
        "pypdf._merger",
        "pypdf._page",
        "pypdf._reader",
        "pypdf._utils",
        "pypdf._writer",
        "pypdf.annotations",
        "pypdf.constants",
        "pypdf.errors",
        "pypdf.filters",
        "pypdf.generic",
        "pypdf.pagerange",
        "pypdf.types",
        "pypdf.xmp",
    ],
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
    name="pdfmerge",
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
