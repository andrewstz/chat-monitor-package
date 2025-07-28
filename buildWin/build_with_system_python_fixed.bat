@echo off
chcp 65001 >nul
echo ========================================
echo Building with System Python 3.10.11
echo ========================================

:: 检查Python版本
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please ensure Python 3.10.11 is installed and in PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python version: %PYTHON_VERSION%

:: 检查是否为Python 3.10.x
echo %PYTHON_VERSION% | findstr "3.10" >nul
if errorlevel 1 (
    echo WARNING: Python version is not 3.10.x
    echo Current version: %PYTHON_VERSION%
    echo.
    echo Do you want to continue anyway? (Y/N)
    set /p choice=
    if /i "%choice%" neq "Y" (
        echo Build cancelled.
        pause
        exit /b 1
    )
)

:: 升级pip（带超时）
echo Upgrading pip...
timeout /t 5 /nobreak >nul
python -m pip install --upgrade pip --timeout 60

:: 检查依赖是否已安装
echo Checking existing dependencies...
python -c "import cv2, ultralytics, pygame" >nul 2>&1
if not errorlevel 1 (
    echo Dependencies already installed, skipping installation...
    goto :build_app
)

:: 安装核心依赖（逐个安装，带超时）
echo Installing core dependencies...
echo Installing opencv-python...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python --timeout 300
if errorlevel 1 (
    echo Trying alternative mirror for opencv-python...
    pip install -i https://mirrors.aliyun.com/pypi/simple/ opencv-python --timeout 300
)

echo Installing ultralytics...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics --timeout 300
if errorlevel 1 (
    echo Trying alternative mirror for ultralytics...
    pip install -i https://mirrors.aliyun.com/pypi/simple/ ultralytics --timeout 300
)

echo Installing Pillow...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ Pillow --timeout 300

echo Installing requests...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests --timeout 300

echo Installing PyYAML...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ PyYAML --timeout 300

echo Installing psutil...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil --timeout 300

:: 安装音频相关依赖
echo Installing audio dependencies...
echo Installing pygame...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame --timeout 300

:: 安装构建工具
echo Installing build tools...
echo Installing pyinstaller...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller --timeout 300

:: 验证依赖安装
echo Verifying dependencies...
python -c "import cv2; print('OpenCV: OK')" 2>nul
python -c "import ultralytics; print('Ultralytics: OK')" 2>nul
python -c "import pygame; print('Pygame: OK')" 2>nul

if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed correctly
    echo You can manually install missing packages using:
    echo   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ [package_name]
    echo.
    echo Do you want to continue with the build? (Y/N)
    set /p continue_build=
    if /i "%continue_build%" neq "Y" (
        echo Build cancelled.
        pause
        exit /b 1
    )
)

:build_app
:: 创建构建目录
echo Creating build directory...
if not exist "dist" mkdir dist
if not exist "build" mkdir build

:: 设置构建参数
set MAIN_SCRIPT=..\main_monitor_gui.py
set APP_NAME=ChatMonitor

:: 检查主脚本是否存在
if not exist "%MAIN_SCRIPT%" (
    echo ERROR: Main script not found: %MAIN_SCRIPT%
    echo Current directory: %CD%
    echo Parent directory contents:
    dir ".." | findstr "main"
    pause
    exit /b 1
)

:: 构建应用程序
echo Building application with PyInstaller...
echo Main script: %MAIN_SCRIPT%
echo This may take several minutes...

:: 使用PyInstaller构建（简化参数）
pyinstaller --onefile ^
    --windowed ^
    --name "%APP_NAME%" ^
    --distpath "dist" ^
    --workpath "build" ^
    --add-data "..\sounds;." ^
    --add-data "..\models;." ^
    --add-data "..\config_with_yolo.yaml;." ^
    "%MAIN_SCRIPT%"

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    echo.
    echo Troubleshooting tips:
    echo 1. Check if all dependencies are installed
    echo 2. Try running: pip install --upgrade pyinstaller
    echo 3. Check if main script exists and is valid
    echo 4. Try running the script directly: python ..\main_monitor_gui.py
    pause
    exit /b 1
)

:: 检查构建结果
if exist "dist\%APP_NAME%.exe" (
    echo ========================================
    echo SUCCESS: Application built successfully!
    echo ========================================
    echo.
    echo Build details:
    echo - Application: dist\%APP_NAME%.exe
    echo - Size: 
    dir "dist\%APP_NAME%.exe" | findstr "%APP_NAME%.exe"
    echo - Python version: %PYTHON_VERSION%
    echo.
    echo To run the application:
    echo   dist\%APP_NAME%.exe
    echo.
) else (
    echo ERROR: Build completed but executable not found
    echo Expected location: dist\%APP_NAME%.exe
    echo.
    echo Build directory contents:
    dir "dist"
    pause
    exit /b 1
)

:: 清理构建文件（可选）
echo.
echo Do you want to clean up build files? (Y/N)
set /p cleanup=
if /i "%cleanup%" equ "Y" (
    echo Cleaning up build files...
    rmdir /s /q "build"
    del "*.spec" >nul 2>&1
    echo Build files cleaned up.
)

echo ========================================
echo Build process completed!
echo ========================================
echo.
echo Final executable: dist\%APP_NAME%.exe
echo.
pause 