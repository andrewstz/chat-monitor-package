@echo off
setlocal enabledelayedexpansion

echo ========================================
echo ChatMonitor Windows Build (Simple)
echo ========================================

:: Check UV environment
if not exist "..\.venv" (
    echo ERROR: UV environment not found!
    pause
    exit /b 1
)

:: Activate UV environment
echo Activating UV environment...
call ..\.venv\Scripts\activate.bat

:: Clean previous builds
echo Cleaning previous build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: Install minimal dependencies
echo Installing minimal dependencies...

:: Install core packages
uv pip install setuptools==68.2.2
uv pip install numpy==1.26.4
uv pip install opencv-python==4.8.1.78
uv pip install ultralytics==8.0.196
uv pip install Pillow==10.1.0
uv pip install requests==2.31.0
uv pip install PyYAML==6.0.1
uv pip install psutil==5.9.5
uv pip install pyinstaller==6.6.0

:: Start building
echo.
echo ========================================
echo Starting application build...
echo ========================================

pyinstaller ^
    --onefile ^
    --windowed ^
    --name ChatMonitor ^
    --add-data "..\sounds;sounds" ^
    --add-data "..\models;models" ^
    --add-data "..\config_with_yolo.yaml;." ^
    --add-data "..\gui;gui" ^
    --add-data "..\daemon;daemon" ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import ultralytics ^
    --hidden-import PIL ^
    --hidden-import requests ^
    --hidden-import yaml ^
    --hidden-import psutil ^
    --hidden-import tkinter ^
    --hidden-import threading ^
    --hidden-import subprocess ^
    ..\main_monitor_gui_app.py

:: Check build result
if exist "dist\ChatMonitor.exe" (
    echo.
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo Generated file: dist\ChatMonitor.exe
    dir dist\ChatMonitor.exe | findstr "ChatMonitor.exe"
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
)

echo.
echo Press any key to exit...
pause 