@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Building Windows application (Final Version - No playsound dependency)...

:: Check if UV environment exists
if not exist ".venv" (
    echo ERROR: UV environment not found!
    echo Please run setup_windows_uv_simple.bat first
    pause
    exit /b 1
)

:: Activate UV environment
call .venv\Scripts\activate.bat

:: Create pyproject without playsound
echo Creating build configuration without playsound...
(
echo [project]
echo name = "chatmonitor"
echo version = "1.0.0"
echo description = "Chat Monitor with YOLO Detection"
echo requires-python = "^3.8"
echo dependencies = [
echo     "opencv-python",
echo     "ultralytics", 
echo     "Pillow",
echo     "requests",
echo     "PyYAML",
echo     "psutil",
echo ]
echo.
echo [build-system]
echo requires = ["hatchling"]
echo build-backend = "hatchling.build"
) > pyproject_build.toml

:: Install core dependencies
echo Installing core dependencies...
uv pip install -e . --config-file pyproject_build.toml

:: Install PyInstaller
echo Installing PyInstaller...
uv pip install pyinstaller

:: Create PyInstaller command directly
echo Building application with PyInstaller...
uv run pyinstaller ^
    --onefile ^
    --windowed ^
    --name ChatMonitor ^
    --add-data "sounds;sounds" ^
    --add-data "models;models" ^
    --add-data "config_with_yolo.yaml;." ^
    --add-data "audio_alternative.py;." ^
    --add-data "fuzzy_matcher.py;." ^
    --add-data "network_monitor.py;." ^
    --add-data "status_monitor.py;." ^
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
    main_monitor_gui_app.py

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
    if exist "sounds" xcopy "sounds" "dist\ChatMonitor\sounds\" /E /I /Y
    if exist "models" xcopy "models" "dist\ChatMonitor\models\" /E /I /Y
    if exist "config_with_yolo.yaml" copy "config_with_yolo.yaml" "dist\ChatMonitor\"
    if exist "audio_alternative.py" copy "audio_alternative.py" "dist\ChatMonitor\"
    
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
    echo.
    echo Note: Audio features will use system commands (PowerShell) for playback
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
)

:: Clean up temporary files
if exist "pyproject_build.toml" del "pyproject_build.toml"

echo.
echo Build process completed!
pause 