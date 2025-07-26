@echo off
echo Building Windows 10 compatible version...

REM Activate virtual environment
call ..\.venv\Scripts\activate.bat

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install compatible dependencies
echo Installing compatible dependencies...

echo Installing opencv-python...
uv pip install opencv-python==4.8.1.78 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying opencv-python-headless...
    uv pip install opencv-python-headless==4.8.1.78 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing numpy...
uv pip install numpy==1.24.3 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying numpy 1.23.5...
    uv pip install numpy==1.23.5 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing ultralytics...
uv pip install ultralytics==8.0.196 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying ultralytics 8.0.0...
    uv pip install ultralytics==8.0.0 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing Pillow...
uv pip install Pillow==10.0.1 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying Pillow 9.5.0...
    uv pip install Pillow==9.5.0 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing requests...
uv pip install requests==2.31.0 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying requests 2.30.0...
    uv pip install requests==2.30.0 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing PyYAML...
uv pip install PyYAML==6.0.1 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying PyYAML 6.0...
    uv pip install PyYAML==6.0 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing psutil...
uv pip install psutil==5.9.5 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying psutil 5.9.0...
    uv pip install psutil==5.9.0 -i https://mirrors.aliyun.com/pypi/simple/
)

echo Installing lap...
uv pip install lap==0.4.0 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying lap 0.3.0...
    uv pip install lap==0.3.0 -i https://mirrors.aliyun.com/pypi/simple/
)

REM Install PyInstaller
echo Installing PyInstaller...
uv pip install pyinstaller==5.13.2 -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo Trying PyInstaller 5.12.0...
    uv pip install pyinstaller==5.12.0 -i https://mirrors.aliyun.com/pypi/simple/
    if errorlevel 1 (
        echo Trying PyInstaller 5.11.0...
        uv pip install pyinstaller==5.11.0 -i https://mirrors.aliyun.com/pypi/simple/
        if errorlevel 1 (
            echo Trying latest PyInstaller...
            uv pip install pyinstaller -i https://mirrors.aliyun.com/pypi/simple/
        )
    )
)

REM Check if PyInstaller installed successfully
pyinstaller --version
if errorlevel 1 (
    echo ERROR: PyInstaller installation failed
    echo Please check network connection or install manually
    pause
    exit /b 1
)

echo OK: PyInstaller installed successfully, starting build...

REM Start building
pyinstaller ^
    --onefile ^
    --windowed ^
    --name ChatMonitor ^
    --add-data "..\sounds;sounds" ^
    --add-data "..\models;models" ^
    --add-data "..\config_with_yolo.yaml;." ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import ultralytics ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageTk ^
    --hidden-import requests ^
    --hidden-import yaml ^
    --hidden-import psutil ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import threading ^
    --hidden-import queue ^
    --hidden-import time ^
    --hidden-import os ^
    --hidden-import sys ^
    --hidden-import json ^
    --hidden-import re ^
    --hidden-import subprocess ^
    --hidden-import platform ^
    --hidden-import socket ^
    --hidden-import urllib3 ^
    --hidden-import charset_normalizer ^
    --hidden-import idna ^
    --hidden-import certifi ^
    --collect-all numpy ^
    --collect-all cv2 ^
    --collect-all ultralytics ^
    --collect-all PIL ^
    --collect-all requests ^
    --collect-all yaml ^
    --collect-all psutil ^
    --collect-all tkinter ^
    --collect-all lap ^
    ..\main_monitor_gui_app.py

if errorlevel 1 (
    echo ERROR: Build failed, check error messages
    pause
    exit /b 1
)

echo SUCCESS: Build completed!
echo Output file: dist\ChatMonitor.exe
echo Mirror used: https://mirrors.aliyun.com/pypi/simple/
pause 