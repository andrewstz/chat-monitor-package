@echo off
chcp 65001 >nul
echo ========================================
echo Dependency Check Script
echo ========================================

:: Check UV environment
echo Checking UV environment...
if exist "..\.venv\Scripts\activate.bat" (
    echo SUCCESS: Found UV environment at ..\.venv
    set UV_PATH=..\.venv
) else if exist "..\uv\Scripts\activate.bat" (
    echo SUCCESS: Found UV environment at ..\uv
    set UV_PATH=..\uv
) else (
    echo ERROR: UV environment not found
    pause
    exit /b 1
)

:: Activate UV environment
echo Activating UV environment...
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

:: Check each dependency individually
echo.
echo Checking dependencies...
echo.

set MISSING_DEPS=0

echo Checking opencv-python...
python -c "import cv2; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: opencv-python
    set /a MISSING_DEPS+=1
) else (
    echo OK: opencv-python
)

echo Checking numpy...
python -c "import numpy; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: numpy
    set /a MISSING_DEPS+=1
) else (
    echo OK: numpy
)

echo Checking psutil...
python -c "import psutil; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: psutil
    set /a MISSING_DEPS+=1
) else (
    echo OK: psutil
)

echo Checking pyautogui...
python -c "import pyautogui; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: pyautogui
    set /a MISSING_DEPS+=1
) else (
    echo OK: pyautogui
)

echo Checking requests...
python -c "import requests; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: requests
    set /a MISSING_DEPS+=1
) else (
    echo OK: requests
)

echo Checking yaml...
python -c "import yaml; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: PyYAML
    set /a MISSING_DEPS+=1
) else (
    echo OK: PyYAML
)

echo Checking PIL...
python -c "import PIL; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: Pillow
    set /a MISSING_DEPS+=1
) else (
    echo OK: Pillow
)

echo Checking pytesseract...
python -c "import pytesseract; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: pytesseract
    set /a MISSING_DEPS+=1
) else (
    echo OK: pytesseract
)

echo Checking watchdog...
python -c "import watchdog; print('OK')" 2>nul
if errorlevel 1 (
    echo MISSING: watchdog
    set /a MISSING_DEPS+=1
) else (
    echo OK: watchdog
)

echo.
echo ========================================
if %MISSING_DEPS% EQU 0 (
    echo SUCCESS: All dependencies are installed!
    echo You can now run the build script.
) else (
    echo WARNING: %MISSING_DEPS% dependencies are missing.
    echo Please run setup script to install missing dependencies.
)
echo ========================================

pause 