@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Building Windows application (Compatible Version)...

:: Check if UV environment exists in parent directory
if not exist "..\.venv" (
    echo ERROR: UV environment not found in parent directory!
    echo Please run setup_windows_uv_simple_fixed.bat first
    pause
    exit /b 1
)

:: Activate UV environment from parent directory
call ..\.venv\Scripts\activate.bat

:: Install core dependencies using UV with mirror
echo Installing core dependencies using UV with mirror...
uv pip install opencv-python ultralytics Pillow requests PyYAML psutil lap>=0.5.12 -i https://pypi.tuna.tsinghua.edu.cn/simple/

:: Install PyInstaller using UV with mirror
echo Installing PyInstaller using UV with mirror...
uv pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/

:: Create PyInstaller command with compatibility options
echo Building application with PyInstaller (compatible version)...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name ChatMonitor ^
    --add-data "..\sounds;sounds" ^
    --add-data "..\models;models" ^
    --add-data "..\config_with_yolo.yaml;." ^
    --add-data "..\fuzzy_matcher.py;." ^
    --add-data "..\network_monitor.py;." ^
    --add-data "..\config_manager.py;." ^
    --hidden-import cv2 ^
    --hidden-import ultralytics ^
    --hidden-import PIL ^
    --hidden-import requests ^
    --hidden-import yaml ^
    --hidden-import psutil ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import threading ^
    --hidden-import subprocess ^
    --hidden-import platform ^
    --exclude-module playsound ^
    --collect-all ultralytics ^
    --collect-all torch ^
    --collect-all torchvision ^
    ..\main_monitor_gui_app.py

:: Check if build was successful
if exist "dist\ChatMonitor.exe" (
    echo.
    echo SUCCESS: Application built successfully!
    echo Location: dist\ChatMonitor.exe
    echo.
    echo Creating portable package...
    
    :: Create dist directory for portable package
    if not exist "dist\ChatMonitor" mkdir "dist\ChatMonitor"
    
    :: Copy executable and resources
    copy "dist\ChatMonitor.exe" "dist\ChatMonitor\"
    if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor\sounds\" /E /I /Y
    if exist "..\models" xcopy "..\models" "dist\ChatMonitor\models\" /E /I /Y
    if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor\"
    
    :: Create portable ZIP
    if exist "ChatMonitor_Windows_Compatible.zip" del "ChatMonitor_Windows_Compatible.zip"
    powershell -command "Compress-Archive -Path 'dist\ChatMonitor\*' -DestinationPath 'ChatMonitor_Windows_Compatible.zip'"
    
    echo.
    echo SUCCESS: Compatible portable package created!
    echo File: ChatMonitor_Windows_Compatible.zip
    echo.
    echo This version should be compatible with:
    echo - Windows 10 and later
    echo - Windows Server 2016 and later
    echo.
    echo You can now:
    echo 1. Run dist\ChatMonitor.exe (single file)
    echo 2. Run dist\ChatMonitor\ChatMonitor.exe (portable)
    echo 3. Extract ChatMonitor_Windows_Compatible.zip to any location
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
)

echo.
echo Build process completed!
pause 