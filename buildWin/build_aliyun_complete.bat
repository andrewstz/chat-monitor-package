@echo off
chcp 65001 >nul

echo ========================================
echo Complete Build for Aliyun Windows
echo ========================================

:: 检查环境
echo Checking environment...
python --version
pip list | findstr pyinstaller

:: 检查文件
echo.
echo Checking required files...
if not exist "..\main_monitor_gui_app.py" (
    echo ERROR: main_monitor_gui_app.py not found!
    pause
    exit /b 1
)
if not exist "..\sounds" (
    echo WARNING: sounds directory not found!
)
if not exist "..\models" (
    echo WARNING: models directory not found!
)
if not exist "..\config_with_yolo.yaml" (
    echo WARNING: config_with_yolo.yaml not found!
)

:: 清理
echo.
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: 测试依赖
echo.
echo Testing dependencies...
python -c "import cv2; print('✓ OpenCV OK')" 2>nul || echo "✗ OpenCV missing"
python -c "import ultralytics; print('✓ Ultralytics OK')" 2>nul || echo "✗ Ultralytics missing"
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import pygame; print('✓ pygame OK')" 2>nul || echo "✗ pygame missing"

:: 开始构建
echo.
echo ========================================
echo Starting build process...
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
    --exclude-module setuptools ^
    --exclude-module pkg_resources ^
    "..\main_monitor_gui_app.py"

:: 检查结果
if exist "dist\ChatMonitor.exe" (
    echo.
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo Generated file: dist\ChatMonitor.exe
    dir dist\ChatMonitor.exe | findstr "ChatMonitor.exe"
    
    echo.
    echo Creating portable package...
    if not exist "dist\ChatMonitor_Portable" mkdir "dist\ChatMonitor_Portable"
    copy "dist\ChatMonitor.exe" "dist\ChatMonitor_Portable\"
    if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor_Portable\sounds\" /E /I /Y
    if exist "..\models" xcopy "..\models" "dist\ChatMonitor_Portable\models\" /E /I /Y
    if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor_Portable\"
    if exist "..\daemon" xcopy "..\daemon" "dist\ChatMonitor_Portable\daemon\" /E /I /Y
    
    echo.
    echo Portable package created: dist\ChatMonitor_Portable\
    echo.
    echo To test the application:
    echo dist\ChatMonitor_Portable\ChatMonitor.exe
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo.
    echo Troubleshooting steps:
    echo 1. Check if pyinstaller is installed: pip install pyinstaller
    echo 2. Check if main_monitor_gui_app.py exists
    echo 3. Try running: python ..\main_monitor_gui_app.py
    echo 4. Check if all dependencies are installed
)

echo.
echo Press any key to exit...
pause 