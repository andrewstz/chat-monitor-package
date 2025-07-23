@echo off
chcp 65001 >nul
echo ========================================
echo Windows App Build - No Playsound Version
echo ========================================

:: Check if in correct directory
if not exist "..\main_monitor_dynamic.py" (
    echo ERROR: Please run this script in buildWin directory
    echo Current directory: %CD%
    echo Please switch to buildWin directory and try again
    pause
    exit /b 1
)

:: Check UV environment in parent directory
echo Checking UV environment in parent directory...
if exist "..\.venv\Scripts\activate.bat" (
    echo SUCCESS: Found UV environment at ..\.venv
    set UV_PATH=..\.venv
) else if exist "..\uv\Scripts\activate.bat" (
    echo SUCCESS: Found UV environment at ..\uv
    set UV_PATH=..\uv
) else (
    echo ERROR: UV environment not found in parent directory
    echo Expected locations: ..\.venv or ..\uv
    echo Please run setup_windows_uv_no_playsound.bat first
    pause
    exit /b 1
)

:: Activate UV environment
echo Activating UV environment at %UV_PATH%...
call "%UV_PATH%\Scripts\activate.bat"

:: Install PyInstaller
echo Installing PyInstaller...
uv pip install pyinstaller

:: Create temporary requirements file (excluding playsound)
echo Creating temporary requirements file...
(
echo # Temporary requirements file - No playsound
echo opencv-python>=4.8.0
echo numpy>=1.24.0
echo psutil>=5.9.0
echo pyautogui>=0.9.54
echo requests>=2.31.0
echo PyYAML>=6.0
echo Pillow>=10.0.0
echo pytesseract>=0.3.10
echo watchdog>=3.0.0
) > temp_requirements_no_playsound.txt

:: Build application
echo Starting application build...
pyinstaller --onefile ^
    --add-data "..\sounds;sounds" ^
    --add-data "..\models;models" ^
    --add-data "..\config_with_yolo.yaml;." ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import psutil ^
    --hidden-import pyautogui ^
    --hidden-import requests ^
    --hidden-import yaml ^
    --hidden-import PIL ^
    --hidden-import pytesseract ^
    --hidden-import watchdog ^
    --exclude-module playsound ^
    --name "ChatMonitor_NoPlaysound" ^
    "..\main_monitor_dynamic.py"

:: Check build result
if exist "dist\ChatMonitor_NoPlaysound.exe" (
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo Executable location: dist\ChatMonitor_NoPlaysound.exe
    echo File size:
    dir "dist\ChatMonitor_NoPlaysound.exe" | find "ChatMonitor_NoPlaysound.exe"
    
    :: Create ZIP package
    echo Creating ZIP package...
    powershell -Command "Compress-Archive -Path 'dist\ChatMonitor_NoPlaysound.exe' -DestinationPath 'ChatMonitor_NoPlaysound.zip' -Force"
    
    if exist "ChatMonitor_NoPlaysound.zip" (
        echo SUCCESS: ZIP package created: ChatMonitor_NoPlaysound.zip
    ) else (
        echo ERROR: ZIP package creation failed
    )
) else (
    echo ========================================
    echo ERROR: Build failed
    echo ========================================
    echo Please check error messages
)

:: Clean up temporary files
del temp_requirements_no_playsound.txt 2>nul

echo.
echo Build completed!
pause 