@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Creating Python 3.12 Compatible Environment
echo ========================================

:: Check if Python is available
echo Checking Python availability...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

:: Go to project root
cd ..

:: Remove old environment if exists
if exist .venv_compatible (
    echo Removing old compatible environment...
    rmdir /s /q .venv_compatible
)

:: Create environment
echo.
echo Creating UV environment...
uv venv .venv_compatible

:: Activate the environment
echo.
echo Activating environment...
call .venv_compatible\Scripts\activate.bat

:: Verify Python version
echo.
echo Verifying Python version in environment:
python --version

:: Install dependencies with Python 3.12 compatible versions
echo.
echo Installing Python 3.12 compatible dependencies...

:: Install setuptools first (newer version)
uv pip install setuptools==68.2.2

:: Install wheel
uv pip install wheel

:: Install numpy with newer version
uv pip install numpy==1.26.4

:: Install other dependencies
uv pip install opencv-python==4.8.1.78
uv pip install ultralytics==8.0.196
uv pip install Pillow==10.1.0
uv pip install requests==2.31.0
uv pip install PyYAML==6.0.1
uv pip install psutil==5.9.5
uv pip install pyinstaller==6.6.0

:: Test all imports
echo.
echo Testing all imports...
python -c "import psutil; print('✓ psutil OK')"
python -c "import cv2; print('✓ cv2 OK')"
python -c "import numpy; print('✓ numpy OK')"
python -c "import ultralytics; print('✓ ultralytics OK')"
python -c "import PIL; print('✓ PIL OK')"
python -c "import requests; print('✓ requests OK')"
python -c "import yaml; print('✓ yaml OK')"
python -c "import tkinter; print('✓ tkinter OK')"

echo.
echo ========================================
echo Environment setup completed!
echo ========================================
echo Python environment: .venv_compatible
echo.
echo To activate this environment:
echo call .venv_compatible\Scripts\activate.bat
echo.
echo To build the application:
echo cd buildWin
echo build_windows_compatible.bat
echo.
echo Press any key to exit...
pause 