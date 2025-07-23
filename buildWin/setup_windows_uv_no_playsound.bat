@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo Windows UV Environment Setup - No Playsound
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
    echo Current directory: %CD%
    echo Parent directory contents:
    dir ".." | findstr "venv\|uv"
    pause
    exit /b 1
)

:: Activate UV environment
echo Activating UV environment at %UV_PATH%...
:: Try different activation methods
if exist "%UV_PATH%\Scripts\activate.bat" (
    echo Using activate.bat...
    call "%UV_PATH%\Scripts\activate.bat"
) else if exist "%UV_PATH%\Scripts\activate.ps1" (
    echo Using activate.ps1 with bypass...
    powershell -ExecutionPolicy Bypass -Command "& '%UV_PATH%\Scripts\activate.ps1'"
) else (
    echo ERROR: No activation script found
    pause
    exit /b 1
)

:: Install dependencies (excluding playsound)
echo Installing dependencies (excluding playsound)...
uv pip install opencv-python>=4.8.0
uv pip install numpy>=1.24.0
uv pip install psutil>=5.9.0
uv pip install pyautogui>=0.9.54
uv pip install requests>=2.31.0
uv pip install PyYAML>=6.0
uv pip install Pillow>=10.0.0
uv pip install pytesseract>=0.3.10
uv pip install watchdog>=3.0.0

:: Verify installation
echo Verifying installation...
python -c "import cv2, numpy, psutil, pyautogui, requests, yaml, PIL, pytesseract, watchdog; print('SUCCESS: All dependencies installed successfully')"

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS: UV environment setup completed!
    echo ========================================
    echo Now you can run the build script
    echo Run: build_windows_uv_no_playsound.bat
) else (
    echo ========================================
    echo ERROR: Dependency installation failed
    echo ========================================
)

pause 