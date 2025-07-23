@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Building Windows application without playsound dependency...

:: Check if UV environment exists
if not exist ".venv" (
    echo ERROR: UV environment not found!
    echo Please run setup_windows_uv_simple.bat first
    pause
    exit /b 1
)

:: Activate UV environment
call .venv\Scripts\activate.bat

:: Create pyproject without playsound
echo Creating build configuration without playsound...
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
echo ]
echo.
echo [build-system]
echo requires = ["hatchling"]
echo build-backend = "hatchling.build"
) > pyproject_build.toml

:: Install core dependencies
echo Installing core dependencies...
uv pip install -e . --config-file pyproject_build.toml

:: Try to install playsound with different methods
echo Attempting to install playsound...
uv pip install "playsound==1.2.2" --frozen 2>nul
if errorlevel 1 (
    echo WARNING: playsound installation failed, using alternative audio
    echo The app will use system commands for audio playback
)

:: Create modified main file without playsound import
echo Creating modified main file...
(
echo import sys
echo import os
echo.
echo # Add current directory to path
echo sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
echo.
echo # Try to import playsound, fallback to alternative
echo try:
echo     import playsound
echo     AUDIO_AVAILABLE = True
echo     print("Using playsound for audio")
echo except ImportError:
echo     AUDIO_AVAILABLE = False
echo     print("Using alternative audio system")
echo.
echo # Import the main application
echo from main_monitor_gui_app import *
echo.
echo if __name__ == "__main__":
echo     main()
) > main_build.py

:: Create PyInstaller spec file
echo Creating PyInstaller configuration...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['main_build.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[
echo         ('sounds', 'sounds'),
echo         ('models', 'models'),
echo         ('config_with_yolo.yaml', '.'),
echo         ('audio_alternative.py', '.'),
echo         ('main_monitor_gui_app.py', '.'),
echo         ('fuzzy_matcher.py', '.'),
echo         ('network_monitor.py', '.'),
echo         ('status_monitor.py', '.'),
echo     ],
echo     hiddenimports=[
echo         'cv2',
echo         'ultralytics',
echo         'PIL',
echo         'requests',
echo         'yaml',
echo         'psutil',
echo         'tkinter',
echo         'tkinter.ttk',
echo         'tkinter.messagebox',
echo         'tkinter.filedialog',
echo         'threading',
echo         'subprocess',
echo         'platform',
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
    echo.
    echo Note: Audio features will use alternative system if playsound is not available
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
)

:: Clean up temporary files
if exist "pyproject_build.toml" del "pyproject_build.toml"
if exist "ChatMonitor.spec" del "ChatMonitor.spec"
if exist "main_build.py" del "main_build.py"

echo.
echo Build process completed!
pause 