# -*- mode: python -*-

# ## usage: $ pyinstaller gator.spec

block_cipher = None

added_files = [
         ( '../../conf/', 'conf/' ),
         ( '../../img/', 'img/' )
         ]


a = Analysis(['../../app/appstart.py'],
             pathex=['../../../gator'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Gator',
          debug=False,
          strip=False,
          upx=True,
          console=True )
app = BUNDLE(exe,
             name='Gator.app',
             icon='../../conf/img/red256.icns',
             bundle_identifier='bhenk.gator')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Gator')
