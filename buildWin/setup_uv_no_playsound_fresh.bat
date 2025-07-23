@echo off
chcp 65001 >nul
echo ========================================
echo UV Environment Setup - No Playsound (Fresh)
echo ========================================

:: Clean existing environment first
echo Cleaning existing environment...
if exist "..\.venv" (
    echo Removing existing .venv directory...
    rmdir /s /q "..\.venv"
    echo SUCCESS: .venv directory removed
)

:: Clean UV cache
echo Cleaning UV cache...
uv cache clean

:: Set Chinese mirror sources
echo Setting up Chinese mirror sources...
set UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/

echo Using mirror: %UV_INDEX_URL%

:: Check if UV is installed
echo Checking UV installation...
uv --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: UV not found. Please install UV first.
    echo Download from: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo UV Version:
uv --version

:: Create UV environment using local Python
echo Creating UV environment using local Python...
cd ..

:: Try to find Python 3.9 specifically
echo Looking for Python 3.9...
python3.9 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python 3.9, using it...
    uv venv --python python3.9 --index-url %UV_INDEX_URL%
) else (
    echo Python 3.9 not found, checking available Python versions...
    python --version
    echo Using available Python version...
    uv venv --python python --index-url %UV_INDEX_URL%
)

cd buildWin

:: Check if environment was created
if exist "..\.venv\Scripts\activate.bat" (
    echo SUCCESS: UV environment created successfully!
    echo Location: ..\.venv
) else (
    echo ERROR: Failed to create UV environment
    pause
    exit /b 1
)

:: Activate environment
echo Activating UV environment...
call "..\.venv\Scripts\activate.bat"

:: Install dependencies with Chinese mirror (no playsound)
echo Installing dependencies with Chinese mirror (no playsound)...
uv pip install --index-url %UV_INDEX_URL% opencv-python>=4.8.0
uv pip install --index-url %UV_INDEX_URL% numpy>=1.24.0
uv pip install --index-url %UV_INDEX_URL% psutil>=5.9.0
uv pip install --index-url %UV_INDEX_URL% pyautogui>=0.9.54
uv pip install --index-url %UV_INDEX_URL% requests>=2.31.0
uv pip install --index-url %UV_INDEX_URL% PyYAML>=6.0
uv pip install --index-url %UV_INDEX_URL% Pillow>=10.0.0
uv pip install --index-url %UV_INDEX_URL% pytesseract>=0.3.10
uv pip install --index-url %UV_INDEX_URL% watchdog>=3.0.0

:: Verify installation
echo Verifying installation...
python -c "import cv2, numpy, psutil, pyautogui, requests, yaml, PIL, pytesseract, watchdog; print('SUCCESS: All dependencies installed successfully')"

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS: UV environment setup completed!
    echo ========================================
    echo Environment: ..\.venv
    echo Python: Local installation
    echo Mirror: %UV_INDEX_URL%
    echo Status: No playsound dependency
    echo.
    echo Now you can run the build script
    echo Run: build_windows_uv_simple_english.bat
) else (
    echo ========================================
    echo ERROR: Dependency installation failed
    echo ========================================
)

pause 