# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\Proiecte\\Python\\School Library Database\\src\\main\\python\\main.py'],
             pathex=['D:\\Proiecte\\Python\\School Library Database\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['e:\\anaconda3\\envs\\pyqt_database\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['D:\\Proiecte\\Python\\School Library Database\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Biblioteca',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='D:\\Proiecte\\Python\\School Library Database\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Biblioteca')
