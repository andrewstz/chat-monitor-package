@echo off
chcp 65001 >nul
echo ========================================
echo System Python Dependency Check
echo ========================================

:: 检查Python版本
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo.
echo ========================================
echo Checking Python Dependencies
echo ========================================

:: 检查各个依赖包
echo Checking opencv-python...
python -c "import cv2; print('OpenCV version:', cv2.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ opencv-python NOT installed
) else (
    echo ✅ opencv-python installed
)

echo Checking ultralytics...
python -c "import ultralytics; print('Ultralytics version:', ultralytics.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ ultralytics NOT installed
) else (
    echo ✅ ultralytics installed
)

echo Checking Pillow...
python -c "import PIL; print('Pillow version:', PIL.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ Pillow NOT installed
) else (
    echo ✅ Pillow installed
)

echo Checking requests...
python -c "import requests; print('Requests version:', requests.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ requests NOT installed
) else (
    echo ✅ requests installed
)

echo Checking PyYAML...
python -c "import yaml; print('PyYAML installed')" 2>nul
if errorlevel 1 (
    echo ❌ PyYAML NOT installed
) else (
    echo ✅ PyYAML installed
)

echo Checking psutil...
python -c "import psutil; print('psutil version:', psutil.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ psutil NOT installed
) else (
    echo ✅ psutil installed
)

echo Checking pygame...
python -c "import pygame; print('Pygame version:', pygame.version.ver)" 2>nul
if errorlevel 1 (
    echo ❌ pygame NOT installed
) else (
    echo ✅ pygame installed
)

echo Checking pyinstaller...
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ pyinstaller NOT installed
) else (
    echo ✅ pyinstaller installed
)

echo.
echo ========================================
echo Dependency Check Complete
echo ========================================
echo.
echo If all dependencies are ✅ installed, you can run:
echo   .\build_quick.bat
echo.
echo If some dependencies are ❌ missing, you can install them manually:
echo   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ [package_name]
echo.
echo Or use the offline installer:
echo   .\install_dependencies_offline.bat
echo.
pause 