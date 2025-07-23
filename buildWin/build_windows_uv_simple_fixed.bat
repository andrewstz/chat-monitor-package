@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Building Windows application with UV (Fixed Version)...

:: Check if UV environment exists
if not exist ".venv" (
    echo ERROR: UV environment not found!
    echo Please run setup_windows_uv_simple.bat first
    pause
    exit /b 1
)

:: Activate UV environment
call .venv\Scripts\activate.bat

:: Create temporary pyproject without playsound for build
echo Creating temporary build configuration...
(
echo [project]
echo name = "chatmonitor"
echo version = "1.0.0"
echo description = "Chat Monitor with YOLO Detection"
echo requires-python = "^3.8"
echo dependencies = [
echo     "opencv-python",
echo     "ultralytics",
echo     "Pillow",
echo     "requests",
echo     "PyYAML",
echo     "psutil",
echo     "tkinter",
echo ]
echo.
echo [build-system]
echo requires = ["hatchling"]
echo build-backend = "hatchling.build"
) > pyproject_build.toml

:: Install dependencies without playsound
echo Installing core dependencies for build...
uv pip install -e . --config-file pyproject_build.toml

:: Install playsound separately with --frozen
echo Installing playsound with frozen flag...
uv pip install "playsound==1.2.2" --frozen

:: Create PyInstaller spec file
echo Creating PyInstaller configuration...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['main_monitor_gui_app.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[
echo         ('sounds', 'sounds'),
echo         ('models', 'models'),
echo         ('config_with_yolo.yaml', '.'),
echo         ('audio_alternative.py', '.'),
echo     ],
echo     hiddenimports=[
echo         'cv2',
echo         'ultralytics',
echo         'PIL',
echo         'requests',
echo         'yaml',
echo         'psutil',
echo         'tkinter',
echo         'playsound',
echo     ],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo )
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     [],
echo     exclude_binaries=True,
echo     name='ChatMonitor',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo     icon='icon.ico' if os.path.exists('icon.ico') else None,
echo )
echo.
echo coll = COLLECT(
echo     exe,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     name='ChatMonitor',
echo )
) > ChatMonitor.spec

:: Build with PyInstaller
echo Building application with PyInstaller...
uv run pyinstaller --clean ChatMonitor.spec

:: Check if build was successful
if exist "dist\ChatMonitor\ChatMonitor.exe" (
    echo.
    echo SUCCESS: Application built successfully!
    echo Location: dist\ChatMonitor\ChatMonitor.exe
    echo.
    echo Creating portable package...
    
    :: Create portable ZIP
    if exist "ChatMonitor_Windows_Portable.zip" del "ChatMonitor_Windows_Portable.zip"
    powershell -command "Compress-Archive -Path 'dist\ChatMonitor\*' -DestinationPath 'ChatMonitor_Windows_Portable.zip'"
    
    echo.
    echo SUCCESS: Portable package created!
    echo File: ChatMonitor_Windows_Portable.zip
    echo.
    echo You can now:
    echo 1. Run dist\ChatMonitor\ChatMonitor.exe
    echo 2. Extract ChatMonitor_Windows_Portable.zip to any location
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
)

:: Clean up temporary files
if exist "pyproject_build.toml" del "pyproject_build.toml"
if exist "ChatMonitor.spec" del "ChatMonitor.spec"

echo.
echo Build process completed!
pause 