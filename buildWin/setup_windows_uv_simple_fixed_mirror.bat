@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo ChatMonitor Windows UV Simple Setup Script (Fixed Version with Mirror)
echo Current Directory: %cd%

:: Set mirror for UV
echo Setting up mirror for UV...
set UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/

:: Check uv environment
echo Checking uv environment...
uv --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: uv not found, please install uv first
    echo TIP: Download from https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo UV Version:
uv --version

:: Check if UV environment exists in parent directory
echo Checking UV environment in parent directory...
if exist "..\.venv" (
    echo OK: Found existing UV environment in parent directory
    echo Using existing environment: ..\.venv
) else (
    echo Creating UV environment in parent directory...
    cd ..
    uv init --no-readme
    cd buildWin
    echo OK: Created UV environment in parent directory
)

:: Check required files (look in parent directory)
echo Checking required files...
set REQUIRED_FILES=main_monitor_gui_app.py config_with_yolo.yaml fuzzy_matcher.py config_manager.py network_monitor.py

for %%f in (%REQUIRED_FILES%) do (
    if not exist "..\%%f" (
        echo ERROR: Missing required file: ..\%%f
        echo TIP: Make sure to run this script from buildWin directory
        echo TIP: Required files should be in the parent directory
        pause
        exit /b 1
    )
    echo   OK: ..\%%f
)

:: Install core dependencies using parent directory's UV environment with mirror
echo Installing core dependencies with uv (using parent environment with mirror)...
echo Using mirror: %UV_INDEX_URL%
cd ..
uv add pyinstaller
uv add ultralytics
uv add opencv-python
uv add numpy
uv add pillow
uv add psutil
uv add pyautogui
uv add requests
uv add pyyaml
uv add pytesseract
uv add watchdog
cd buildWin

echo OK: Core dependencies installed

:: Skip playsound installation completely
echo Skipping playsound installation (will use alternative audio)
echo The application will use PowerShell for audio playback
echo This works on Windows without additional dependencies

:: Check macOS icons (look in parent directory)
echo Checking macOS icons...
if exist "..\assets\icons\icon.png" (
    echo   OK: Found macOS icon files
) else (
    echo   WARNING: No icon files found
    echo   TIP: Run on macOS: python create_png_icon.py
    echo   TIP: Then copy the entire directory to Windows
)

:: Check Tesseract
echo Checking Tesseract OCR...
cd ..
uv run python -c "import pytesseract; print('Tesseract path:', pytesseract.get_tesseract_version())" 2>nul
if errorlevel 1 (
    echo WARNING: Tesseract not installed or configured
    echo TIP: Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
    echo TIP: Or download pre-compiled version
)
cd buildWin

:: Create test script
echo Creating test script...
echo @echo off > test_windows_uv_simple_fixed_mirror.bat
echo echo Testing Windows UV environment (Fixed Version with Mirror)... >> test_windows_uv_simple_fixed_mirror.bat
echo set UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/ >> test_windows_uv_simple_fixed_mirror.bat
echo cd .. >> test_windows_uv_simple_fixed_mirror.bat
echo uv run python -c "import cv2; import numpy; import psutil; import pyautogui; import requests; import yaml; import PIL; import pytesseract; import watchdog; import ultralytics; import tkinter; print('OK: Core dependencies imported successfully')" >> test_windows_uv_simple_fixed_mirror.bat
echo echo Audio will use PowerShell commands >> test_windows_uv_simple_fixed_mirror.bat
echo echo Testing alternative audio system... >> test_windows_uv_simple_fixed_mirror.bat
echo uv run python audio_alternative.py >> test_windows_uv_simple_fixed_mirror.bat
echo cd buildWin >> test_windows_uv_simple_fixed_mirror.bat

:: Create build script with mirror support
echo Creating build script with mirror support...
echo @echo off > build_windows_uv_simple_final_fixed_mirror.bat
echo chcp 936 ^>nul >> build_windows_uv_simple_final_fixed_mirror.bat
echo setlocal enabledelayedexpansion >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Set mirror for UV >> build_windows_uv_simple_final_fixed_mirror.bat
echo set UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/ >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo echo Building Windows application (Fixed Version - No playsound dependency with Mirror)... >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Check if UV environment exists in parent directory >> build_windows_uv_simple_final_fixed_mirror.bat
echo if not exist "..\.venv" ( >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo ERROR: UV environment not found in parent directory! >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo Please run setup_windows_uv_simple_fixed_mirror.bat first >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo TIP: UV environment should be in the parent directory >> build_windows_uv_simple_final_fixed_mirror.bat
echo     pause >> build_windows_uv_simple_final_fixed_mirror.bat
echo     exit /b 1 >> build_windows_uv_simple_final_fixed_mirror.bat
echo ) >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Activate UV environment from parent directory >> build_windows_uv_simple_final_fixed_mirror.bat
echo call ..\.venv\Scripts\activate.bat >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Install core dependencies directly without pyproject >> build_windows_uv_simple_final_fixed_mirror.bat
echo echo Installing core dependencies... >> build_windows_uv_simple_final_fixed_mirror.bat
echo uv pip install opencv-python ultralytics Pillow requests PyYAML psutil >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Install PyInstaller >> build_windows_uv_simple_final_fixed_mirror.bat
echo echo Installing PyInstaller... >> build_windows_uv_simple_final_fixed_mirror.bat
echo uv pip install pyinstaller >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Create PyInstaller command directly >> build_windows_uv_simple_final_fixed_mirror.bat
echo echo Building application with PyInstaller... >> build_windows_uv_simple_final_fixed_mirror.bat
echo uv run pyinstaller ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --onefile ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --windowed ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --name ChatMonitor ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\sounds;sounds" ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\models;models" ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\config_with_yolo.yaml;." ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\audio_alternative.py;." ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\fuzzy_matcher.py;." ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\network_monitor.py;." ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --add-data "..\status_monitor.py;." ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import cv2 ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import ultralytics ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import PIL ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import requests ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import yaml ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import psutil ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import tkinter ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import tkinter.ttk ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import tkinter.messagebox ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import tkinter.filedialog ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import threading ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import subprocess ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --hidden-import platform ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     --exclude-module playsound ^^ >> build_windows_uv_simple_final_fixed_mirror.bat
echo     ..\main_monitor_gui_app.py >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo :: Check if build was successful >> build_windows_uv_simple_final_fixed_mirror.bat
echo if exist "dist\ChatMonitor.exe" ( >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo SUCCESS: Application built successfully! >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo Location: dist\ChatMonitor.exe >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo Creating portable package... >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     :: Create dist directory for portable package >> build_windows_uv_simple_final_fixed_mirror.bat
echo     if not exist "dist\ChatMonitor" mkdir "dist\ChatMonitor" >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     :: Copy executable and resources >> build_windows_uv_simple_final_fixed_mirror.bat
echo     copy "dist\ChatMonitor.exe" "dist\ChatMonitor\" >> build_windows_uv_simple_final_fixed_mirror.bat
echo     if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor\sounds\" /E /I /Y >> build_windows_uv_simple_final_fixed_mirror.bat
echo     if exist "..\models" xcopy "..\models" "dist\ChatMonitor\models\" /E /I /Y >> build_windows_uv_simple_final_fixed_mirror.bat
echo     if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor\" >> build_windows_uv_simple_final_fixed_mirror.bat
echo     if exist "..\audio_alternative.py" copy "..\audio_alternative.py" "dist\ChatMonitor\" >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     :: Create portable ZIP >> build_windows_uv_simple_final_fixed_mirror.bat
echo     if exist "ChatMonitor_Windows_Portable.zip" del "ChatMonitor_Windows_Portable.zip" >> build_windows_uv_simple_final_fixed_mirror.bat
echo     powershell -command "Compress-Archive -Path 'dist\ChatMonitor\*' -DestinationPath 'ChatMonitor_Windows_Portable.zip'" >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo SUCCESS: Portable package created! >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo File: ChatMonitor_Windows_Portable.zip >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo You can now: >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo 1. Run dist\ChatMonitor.exe (single file) >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo 2. Run dist\ChatMonitor\ChatMonitor.exe (portable) >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo 3. Extract ChatMonitor_Windows_Portable.zip to any location >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo Note: Audio features will use system commands (PowerShell) for playback >> build_windows_uv_simple_final_fixed_mirror.bat
echo ) else ( >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo ERROR: Build failed! >> build_windows_uv_simple_final_fixed_mirror.bat
echo     echo Check the error messages above. >> build_windows_uv_simple_final_fixed_mirror.bat
echo ) >> build_windows_uv_simple_final_fixed_mirror.bat
echo. >> build_windows_uv_simple_final_fixed_mirror.bat
echo echo Build process completed! >> build_windows_uv_simple_final_fixed_mirror.bat
echo pause >> build_windows_uv_simple_final_fixed_mirror.bat

echo.
echo Windows UV simple setup completed (Fixed Version with Mirror)
echo.
echo Next steps:
echo 1. Run test_windows_uv_simple_fixed_mirror.bat to test environment
echo 2. Run build_windows_uv_simple_final_fixed_mirror.bat to build application
echo 3. Find application in dist\ChatMonitor\ directory
echo.
echo UV advantages:
echo - Faster dependency installation
echo - Better dependency resolution
echo - Isolated environment management
echo - Compatible with existing pip packages
echo.
echo Note: Audio features will use PowerShell commands (no playsound dependency)
echo.
echo TIP: Using existing UV environment from parent directory with mirror support
echo TIP: Mirror settings: %UV_INDEX_URL%
pause 