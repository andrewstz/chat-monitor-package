@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo ChatMonitor Windows Build (Conda Environment)
echo ========================================

:: 检查conda环境
echo Checking conda environment...
conda info --envs
echo.

:: 检查Python版本
echo Current Python version:
python --version
echo.

:: 检查pip
echo Checking pip...
pip --version
echo.

:: 安装/更新必要的依赖
echo Installing/updating dependencies...
pip install --upgrade pip
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ Pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ PyYAML
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 测试依赖
echo.
echo Testing dependencies...
python -c "import cv2; print('✓ OpenCV:', cv2.__version__)" 2>nul || echo "✗ OpenCV missing"
python -c "import ultralytics; print('✓ Ultralytics:', ultralytics.__version__)" 2>nul || echo "✗ Ultralytics missing"
python -c "import PIL; print('✓ Pillow:', PIL.__version__)" 2>nul || echo "✗ Pillow missing"
python -c "import psutil; print('✓ psutil:', psutil.__version__)" 2>nul || echo "✗ psutil missing"
python -c "import pygame; print('✓ pygame:', pygame.version.ver)" 2>nul || echo "✗ pygame missing"

:: 清理之前的构建
echo.
echo Cleaning previous build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: 开始构建
echo.
echo ========================================
echo Starting application build...
echo ========================================

:: 使用更简单的构建命令
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
    --exclude-module conda ^
    --exclude-module conda_package_handling ^
    "..\main_monitor_gui_app.py"

:: 检查构建结果
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
    echo 1. Check if all dependencies are installed
    echo 2. Try running: pip install --upgrade pyinstaller
    echo 3. Check if the main script exists: ..\main_monitor_gui_app.py
    echo.
    echo Manual dependency installation:
    echo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil pygame pyinstaller
)

echo.
echo Press any key to exit...
pause 