@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo ChatMonitor Windows UV Environment Setup Script
echo Current Directory: %cd%

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

:: Check Python environment
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found, please install Python 3.8+
    echo TIP: Download from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python Version:
python --version

:: Check required files
echo Checking required files...
set REQUIRED_FILES=main_monitor_gui_app.py config_with_yolo.yaml fuzzy_matcher.py config_manager.py network_monitor.py

for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo ERROR: Missing required file: %%f
        echo TIP: Make sure to run this script in the correct directory
        pause
        exit /b 1
    )
    echo   OK: %%f
)

:: Create uv project if not exists
if not exist "pyproject.toml" (
    echo Creating uv project...
    uv init --no-readme
    echo OK: Created uv project
) else (
    echo OK: UV project already exists
)

:: Install dependencies using uv
echo Installing dependencies with uv...
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
uv add "playsound>=1.2.2"
uv add watchdog

echo OK: Dependencies installed with uv

:: Check macOS icons
echo Checking macOS icons...
if exist "assets\icons\icon.png" (
    echo   OK: Found macOS icon files
) else (
    echo   WARNING: No icon files found
    echo   TIP: Run on macOS: python create_png_icon.py
    echo   TIP: Then copy the entire directory to Windows
)

:: Check Tesseract
echo Checking Tesseract OCR...
python -c "import pytesseract; print('Tesseract path:', pytesseract.get_tesseract_version())" 2>nul
if errorlevel 1 (
    echo WARNING: Tesseract not installed or configured
    echo TIP: Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
    echo TIP: Or download pre-compiled version
)

:: Create test script
echo Creating test script...
echo @echo off > test_windows_uv_setup.bat
echo echo Testing Windows UV environment... >> test_windows_uv_setup.bat
echo uv run python -c "import cv2; import numpy; import psutil; import pyautogui; import requests; import yaml; import PIL; import pytesseract; import playsound; import watchdog; import ultralytics; import tkinter; print('OK: All dependencies imported successfully')" >> test_windows_uv_setup.bat
echo pause >> test_windows_uv_setup.bat

:: Create build script for uv
echo Creating UV build script...
echo @echo off > build_windows_uv.bat
echo chcp 936 ^>nul >> build_windows_uv.bat
echo setlocal enabledelayedexpansion >> build_windows_uv.bat
echo. >> build_windows_uv.bat
echo echo Building Windows application with UV... >> build_windows_uv.bat
echo uv run pyinstaller --onedir --windowed --name=ChatMonitor --noconfirm --add-data=config_with_yolo.yaml;. --add-data=fuzzy_matcher.py;. --add-data=config_manager.py;. --add-data=network_monitor.py;. --hidden-import=cv2 --hidden-import=numpy --hidden-import=psutil --hidden-import=pyautogui --hidden-import=requests --hidden-import=urllib3 --hidden-import=charset_normalizer --hidden-import=idna --hidden-import=certifi --hidden-import=yaml --hidden-import=PIL --hidden-import=pytesseract --hidden-import=playsound --hidden-import=watchdog --hidden-import=ultralytics --hidden-import=cv2 --hidden-import=numpy --hidden-import=tkinter --exclude-module=PyQt5 --exclude-module=PyQt6 --exclude-module=IPython --exclude-module=jupyter --exclude-module=scikit-learn --exclude-module=tensorflow --exclude-module=transformers main_monitor_gui_app.py >> build_windows_uv.bat
echo. >> build_windows_uv.bat
echo if exist "dist\ChatMonitor\ChatMonitor.exe" ^( >> build_windows_uv.bat
echo     echo OK: Build completed successfully >> build_windows_uv.bat
echo     echo Application: dist\ChatMonitor\ChatMonitor.exe >> build_windows_uv.bat
echo ^) else ^( >> build_windows_uv.bat
echo     echo ERROR: Build failed >> build_windows_uv.bat
echo ^) >> build_windows_uv.bat
echo pause >> build_windows_uv.bat

echo.
echo Windows UV environment setup completed!
echo.
echo Next steps:
echo   1. Run test_windows_uv_setup.bat to test environment
echo   2. Run build_windows_uv.bat to build application
echo   3. Find application in dist\ChatMonitor\ directory
echo.
echo UV advantages:
echo   - Faster dependency installation
echo   - Better dependency resolution
echo   - Isolated environment management
echo   - Compatible with existing pip packages
echo.
pause 