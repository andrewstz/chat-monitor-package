@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Creating Python 3.10.18 UV Environment
echo ========================================

:: Check if Python 3.10 is available
echo Checking Python 3.10 availability...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.10.18 first
    pause
    exit /b 1
)

:: Go to project root
cd ..

:: Remove old environment if exists
if exist .venv_py310 (
    echo Removing old Python 3.10 environment...
    rmdir /s /q .venv_py310
)

:: Create new UV environment with Python 3.10
echo.
echo Creating UV environment with Python 3.10...
uv venv --python 3.10 .venv_py310

:: Activate the environment
echo.
echo Activating environment...
call .venv_py310\Scripts\activate.bat

:: Verify Python version
echo.
echo Verifying Python version in environment:
python --version

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
echo Python 3.10 environment: .venv_py310
echo.
echo To activate this environment:
echo call .venv_py310\Scripts\activate.bat
echo.
echo To build the application:
echo cd buildWin
echo build_windows_py310.bat
echo.
echo Press any key to exit...
pause 