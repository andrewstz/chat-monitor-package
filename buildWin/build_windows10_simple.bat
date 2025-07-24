@echo off
echo 正在构建Windows 10兼容版本...

REM 激活虚拟环境
call ..\.venv\Scripts\activate.bat

REM 清理之前的构建
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM 安装兼容的依赖版本
echo 安装兼容的依赖包...
uv pip install opencv-python==4.8.1.78 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install numpy==1.24.3 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install ultralytics==8.0.196 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install Pillow==10.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install requests==2.31.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install PyYAML==6.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install psutil==5.9.5 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install lap==0.4.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/

REM 安装PyInstaller
uv pip install pyinstaller==5.13.2 -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo 开始打包...
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

echo 构建完成！
echo 生成的文件在 dist\ChatMonitor.exe
pause 