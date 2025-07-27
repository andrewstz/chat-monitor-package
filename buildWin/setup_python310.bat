@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Setup Python 3.10.18 Environment
echo ========================================

:: Check if Python 3.10 is installed
echo Checking Python 3.10 installation...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.10.18 first
    echo Download from: https://www.python.org/downloads/release/python-31018/
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python version: %PYTHON_VERSION%

:: Install uv if not present
echo.
echo Installing uv...
if not exist "%USERPROFILE%\.cargo\bin\uv.exe" (
    echo Installing uv via pip...
    python -m pip install uv
) else (
    echo uv already installed
)

:: Create new UV environment with Python 3.10
echo.
echo Creating UV environment with Python 3.10...
cd ..
if exist .venv_py310 rmdir /s /q .venv_py310
uv venv --python 3.10 .venv_py310

:: Activate environment
echo.
echo Activating environment...
call .venv_py310\Scripts\activate.bat

:: Install dependencies
echo.
echo Installing dependencies...
uv pip install wheel
uv pip install setuptools==68.2.2
uv pip install numpy==1.24.3
uv pip install opencv-python==4.8.1.78
uv pip install ultralytics==8.0.196
uv pip install Pillow==10.0.1
uv pip install requests==2.31.0
uv pip install PyYAML==6.0.1
uv pip install psutil==5.9.5
uv pip install pyinstaller==5.13.2

:: Test imports
echo.
echo Testing imports...
python -c "import psutil; print('psutil OK')"
python -c "import cv2; print('cv2 OK')"
python -c "import numpy; print('numpy OK')"
python -c "import ultralytics; print('ultralytics OK')"
python -c "import PIL; print('PIL OK')"
python -c "import requests; print('requests OK')"
python -c "import yaml; print('yaml OK')"
python -c "import tkinter; print('tkinter OK')"

echo.
echo ========================================
echo Environment setup completed!
echo ========================================
echo Python 3.10 environment: .venv_py310
echo To activate: call .venv_py310\Scripts\activate.bat
echo.
echo Press any key to exit...
pause 