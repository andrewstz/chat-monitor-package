@echo off
setlocal enabledelayedexpansion

echo ========================================
echo ChatMonitor Windows Build Script (Fixed)
echo ========================================

:: Check UV environment
if not exist "..\.venv" (
    echo ERROR: UV environment not found!
    echo Please run: uv venv
    echo Then run: .venv\Scripts\activate
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

:: Install dependencies (using Python 3.12 compatible versions)
echo Installing dependencies...

:: Install setuptools FIRST (fix compatibility issues)
echo Installing setuptools (Python 3.12 compatible)...
uv pip install setuptools==68.2.2 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install setuptools==68.2.2

:: Install numpy FIRST (required by other packages)
echo Installing numpy (Python 3.12 compatible)...
uv pip install numpy==1.26.4 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install numpy==1.26.4

:: Try different mirror sources with updated versions
echo Installing opencv-python...
uv pip install opencv-python==4.8.1.78 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install opencv-python==4.8.1.78

echo Installing ultralytics...
uv pip install ultralytics==8.0.196 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install ultralytics==8.0.196

echo Installing Pillow...
uv pip install Pillow==10.1.0 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install Pillow==10.1.0

echo Installing requests...
uv pip install requests==2.31.0 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install requests==2.31.0

echo Installing PyYAML...
uv pip install PyYAML==6.0.1 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install PyYAML==6.0.1

echo Installing psutil...
uv pip install psutil==5.9.5 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install psutil==5.9.5

:: Skip lap package (not essential for basic functionality)
echo Skipping lap package (not essential)...

:: Install PyInstaller (use newer version)
echo Installing PyInstaller...
uv pip install pyinstaller==6.6.0 -i https://mirrors.aliyun.com/pypi/simple/ || uv pip install pyinstaller==6.6.0

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
    ..\main_monitor_gui_app.py

:: Check build result
if exist "dist\ChatMonitor.exe" (
    echo.
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo Generated file: dist\ChatMonitor.exe
    echo File size: 
    dir dist\ChatMonitor.exe | findstr "ChatMonitor.exe"
    echo.
    echo Creating portable package...
    
    :: Create portable directory
    if not exist "dist\ChatMonitor_Portable" mkdir "dist\ChatMonitor_Portable"
    
    :: Copy files
    copy "dist\ChatMonitor.exe" "dist\ChatMonitor_Portable\"
    if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor_Portable\sounds\" /E /I /Y
    if exist "..\models" xcopy "..\models" "dist\ChatMonitor_Portable\models\" /E /I /Y
    if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor_Portable\"
    if exist "..\daemon" xcopy "..\daemon" "dist\ChatMonitor_Portable\daemon\" /E /I /Y
    
    echo SUCCESS: Portable package created: dist\ChatMonitor_Portable\
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo Please check error messages and try again
)

echo.
echo Press any key to exit...
pause 