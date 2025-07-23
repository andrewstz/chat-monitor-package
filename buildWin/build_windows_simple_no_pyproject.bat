@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Building Windows application (Simple Version - No pyproject.toml)...

:: Check if UV environment exists in parent directory
if not exist "..\.venv" (
    echo ERROR: UV environment not found in parent directory!
    echo Please run setup_windows_uv_simple_fixed.bat first
    pause
    exit /b 1
)

:: Activate UV environment from parent directory
call ..\.venv\Scripts\activate.bat

:: Install dependencies directly
echo Installing dependencies...
pip install opencv-python ultralytics Pillow requests PyYAML psutil pyinstaller

:: Build with PyInstaller
echo Building application with PyInstaller...
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
    if exist "ChatMonitor_Windows_Portable.zip" del "ChatMonitor_Windows_Portable.zip"
    powershell -command "Compress-Archive -Path 'dist\ChatMonitor\*' -DestinationPath 'ChatMonitor_Windows_Portable.zip'"
    
    echo.
    echo SUCCESS: Portable package created!
    echo File: ChatMonitor_Windows_Portable.zip
    echo.
    echo You can now:
    echo 1. Run dist\ChatMonitor.exe (single file)
    echo 2. Run dist\ChatMonitor\ChatMonitor.exe (portable)
    echo 3. Extract ChatMonitor_Windows_Portable.zip to any location
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
)

echo.
echo Build process completed!
pause 