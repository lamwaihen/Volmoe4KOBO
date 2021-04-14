# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Volmoe4KOBO.py'],
             pathex=['M:\\Documents\\GitHub\\Volmoe4KOBO'],
             binaries=[],
             datas=
             [
             ('Res\\mimetype', 'Res'),
             ('Res\\container.xml', 'Res'),
             ('Res\\style', 'Res\\style'),
             ('Res\\standard.opf', 'Res'),
             ('Res\\toc.ncx', 'Res'),
             ('Res\\page.xhtml', 'Res'),
             ('Res\\navigation-documents.html', 'Res')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Manga4KOBO',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='Res\\icon-256.ico')
