@echo off
echo 正在构建Windows 10兼容版本（动态镜像源）...

REM 激活虚拟环境
call ..\.venv\Scripts\activate.bat

REM 清理之前的构建
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 定义镜像源列表（按优先级排序）
set MIRROR1=https://mirrors.aliyun.com/pypi/simple
set MIRROR2=https://pypi.tuna.tsinghua.edu.cn/simple
set MIRROR3=https://pypi.mirrors.ustc.edu.cn/simple
set MIRROR4=https://pypi.douban.com/simple
set MIRROR5=https://mirrors.huaweicloud.com/repository/pypi/simple
set MIRROR6=https://mirrors.cloud.tencent.com/pypi/simple
set MIRROR7=https://mirrors.163.com/pypi/simple
set MIRROR8=https://pypi.org/simple

REM 测试镜像源函数
:test_mirror
set MIRROR_URL=%1
echo 测试镜像源: %MIRROR_URL%
python -c "import urllib.request; urllib.request.urlopen('%MIRROR_URL%/simple/', timeout=5)" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 镜像源可用: %MIRROR_URL%
    goto :install_packages
) else (
    echo ❌ 镜像源不可用: %MIRROR_URL%
    shift
    if not "%1"=="" goto :test_mirror
    echo ❌ 所有镜像源都不可用，尝试使用默认源
    set MIRROR_URL=https://pypi.org/simple
)

:install_packages
echo 使用镜像源: %MIRROR_URL%

REM 安装兼容的依赖版本
echo 安装兼容的依赖包...
echo 正在安装opencv-python...
uv pip install opencv-python==4.8.1.78 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装opencv-python-headless...
    uv pip install opencv-python-headless==4.8.1.78 -i %MIRROR_URL%
)

echo 正在安装numpy...
uv pip install numpy==1.24.3 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装numpy 1.23.5...
    uv pip install numpy==1.23.5 -i %MIRROR_URL%
)

echo 正在安装ultralytics...
uv pip install ultralytics==8.0.196 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装ultralytics 8.0.0...
    uv pip install ultralytics==8.0.0 -i %MIRROR_URL%
)

echo 正在安装Pillow...
uv pip install Pillow==10.0.1 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装Pillow 9.5.0...
    uv pip install Pillow==9.5.0 -i %MIRROR_URL%
)

echo 正在安装requests...
uv pip install requests==2.31.0 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装requests 2.30.0...
    uv pip install requests==2.30.0 -i %MIRROR_URL%
)

echo 正在安装PyYAML...
uv pip install PyYAML==6.0.1 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装PyYAML 6.0...
    uv pip install PyYAML==6.0 -i %MIRROR_URL%
)

echo 正在安装psutil...
uv pip install psutil==5.9.5 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装psutil 5.9.0...
    uv pip install psutil==5.9.0 -i %MIRROR_URL%
)

echo 正在安装lap...
uv pip install lap==0.4.0 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装lap 0.3.0...
    uv pip install lap==0.3.0 -i %MIRROR_URL%
)

REM 安装PyInstaller（尝试多个版本）
echo 正在安装PyInstaller...
uv pip install pyinstaller==5.13.2 -i %MIRROR_URL%
if errorlevel 1 (
    echo 尝试安装PyInstaller 5.12.0...
    uv pip install pyinstaller==5.12.0 -i %MIRROR_URL%
    if errorlevel 1 (
        echo 尝试安装PyInstaller 5.11.0...
        uv pip install pyinstaller==5.11.0 -i %MIRROR_URL%
        if errorlevel 1 (
            echo 尝试安装最新版本PyInstaller...
            uv pip install pyinstaller -i %MIRROR_URL%
        )
    )
)

REM 检查PyInstaller是否安装成功
pyinstaller --version
if errorlevel 1 (
    echo ❌ PyInstaller安装失败，请检查网络连接或手动安装
    pause
    exit /b 1
)

echo ✅ PyInstaller安装成功，开始打包...

REM 开始打包
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
    echo ❌ 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo ✅ 构建完成！
echo 📁 生成的文件在 dist\ChatMonitor.exe
echo 🔗 使用的镜像源: %MIRROR_URL%
pause 