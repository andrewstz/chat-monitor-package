@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo ChatMonitor Windows Environment Setup Script
echo Current Directory: %cd%

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

:: Check pip
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not installed or not available
    pause
    exit /b 1
)

echo pip is available

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing Python dependencies...
echo TIP: Using mirror source for faster download...

:: Set pip mirror source
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
set PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

:: Install core dependencies
echo Installing core dependencies...
python -m pip install -r requirements_windows.txt

if errorlevel 1 (
    echo ERROR: Dependency installation failed
    echo TIP: Trying with default source...
    python -m pip install -r requirements_windows.txt
)

:: Install PyInstaller
echo Installing PyInstaller...
python -m pip install pyinstaller

:: Check macOS icons
echo Checking macOS icons...
if exist "assets\icons\icon.png" (
    echo   OK: Found macOS icon files
) else (
    echo   WARNING: No icon files found
    echo   TIP: Run on macOS: python create_png_icon.py
    echo   TIP: Then copy the entire directory to Windows
)

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
echo @echo off > test_windows_setup.bat
echo echo Testing Windows environment... >> test_windows_setup.bat
echo python -c "import cv2; import numpy; import psutil; import pyautogui; import requests; import yaml; import PIL; import pytesseract; import playsound; import watchdog; import ultralytics; import tkinter; print('OK: All dependencies imported successfully')" >> test_windows_setup.bat
echo pause >> test_windows_setup.bat

echo.
echo Windows environment setup completed!
echo.
echo Next steps:
echo   1. Run test_windows_setup.bat to test environment
echo   2. Run build_windows_app.bat to build application
echo   3. Find portable application in release directory
echo.
echo TIPS:
echo   - If Tesseract not installed, OCR may not work
echo   - First run may need firewall access
echo   - Test in VM before production deployment
echo.
pause 