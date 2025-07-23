@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo ChatMonitor Windows UV Simple Setup Script
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

:: Install core dependencies (avoid problematic ones)
echo Installing core dependencies with uv...
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

echo OK: Core dependencies installed

:: Try to install playsound separately (with fallback)
echo Installing audio dependencies...
uv add "playsound>=1.2.2" 2>nul
if errorlevel 1 (
    echo WARNING: playsound installation failed, trying alternative...
    uv add "playsound==1.2.2" 2>nul
    if errorlevel 1 (
        echo WARNING: playsound not installed, audio features may not work
        echo TIP: You can install it manually later if needed
    ) else (
        echo OK: playsound installed successfully
    )
) else (
    echo OK: playsound installed successfully
)

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
echo @echo off > test_windows_uv_simple.bat
echo echo Testing Windows UV environment... >> test_windows_uv_simple.bat
echo uv run python -c "import cv2; import numpy; import psutil; import pyautogui; import requests; import yaml; import PIL; import pytesseract; import watchdog; import ultralytics; import tkinter; print('OK: Core dependencies imported successfully')" >> test_windows_uv_simple.bat
echo uv run python -c "try: import playsound; print('OK: Audio dependency available'); except: print('WARNING: Audio dependency not available')" >> test_windows_uv_simple.bat
echo pause >> test_windows_uv_simple.bat

:: Create build script for uv
echo Creating UV build script...
echo @echo off > build_windows_uv_simple.bat
echo chcp 936 ^>nul >> build_windows_uv_simple.bat
echo setlocal enabledelayedexpansion >> build_windows_uv_simple.bat
echo. >> build_windows_uv_simple.bat
echo echo Building Windows application with UV... >> build_windows_uv_simple.bat
echo uv run pyinstaller --onedir --windowed --name=ChatMonitor --noconfirm --add-data=config_with_yolo.yaml;. --add-data=fuzzy_matcher.py;. --add-data=config_manager.py;. --add-data=network_monitor.py;. --hidden-import=cv2 --hidden-import=numpy --hidden-import=psutil --hidden-import=pyautogui --hidden-import=requests --hidden-import=urllib3 --hidden-import=charset_normalizer --hidden-import=idna --hidden-import=certifi --hidden-import=yaml --hidden-import=PIL --hidden-import=pytesseract --hidden-import=watchdog --hidden-import=ultralytics --hidden-import=cv2 --hidden-import=numpy --hidden-import=tkinter --exclude-module=PyQt5 --exclude-module=PyQt6 --exclude-module=IPython --exclude-module=jupyter --exclude-module=scikit-learn --exclude-module=tensorflow --exclude-module=transformers main_monitor_gui_app.py >> build_windows_uv_simple.bat
echo. >> build_windows_uv_simple.bat
echo if exist "dist\ChatMonitor\ChatMonitor.exe" ^( >> build_windows_uv_simple.bat
echo     echo OK: Build completed successfully >> build_windows_uv_simple.bat
echo     echo Application: dist\ChatMonitor\ChatMonitor.exe >> build_windows_uv_simple.bat
echo ^) else ^( >> build_windows_uv_simple.bat
echo     echo ERROR: Build failed >> build_windows_uv_simple.bat
echo ^) >> build_windows_uv_simple.bat
echo pause >> build_windows_uv_simple.bat

echo.
echo Windows UV simple setup completed!
echo.
echo Next steps:
echo   1. Run test_windows_uv_simple.bat to test environment
echo   2. Run build_windows_uv_simple.bat to build application
echo   3. Find application in dist\ChatMonitor\ directory
echo.
echo UV advantages:
echo   - Faster dependency installation
echo   - Better dependency resolution
echo   - Isolated environment management
echo   - Compatible with existing pip packages
echo.
echo Note: Audio features may be limited if playsound fails to install
echo.
pause 