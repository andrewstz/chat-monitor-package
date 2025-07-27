@echo off
setlocal enabledelayedexpansion

echo ========================================
echo ChatMonitor Windows Build (Python 3.10)
echo ========================================

:: Check if Python 3.10 environment exists
if not exist "..\.venv_py310" (
    echo ERROR: Python 3.10 environment not found!
    echo Please run create_py310_env.bat first
    pause
    exit /b 1
)

:: Activate Python 3.10 environment
echo Activating Python 3.10 environment...
call ..\.venv_py310\Scripts\activate.bat

:: Verify Python version
echo.
echo Python version in environment:
python --version

:: Clean previous builds
echo.
echo Cleaning previous build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: Test dependencies
echo.
echo Testing dependencies...
python -c "import psutil; print('✓ psutil OK')"
python -c "import cv2; print('✓ cv2 OK')"
python -c "import ultralytics; print('✓ ultralytics OK')"

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
)

echo.
echo Press any key to exit...
pause 