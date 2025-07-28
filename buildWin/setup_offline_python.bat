@echo off
chcp 65001 >nul
echo ========================================
echo Offline Python 3.10.18 Environment Setup
echo ========================================

:: 检查Python是否已安装
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.10.18 first
    echo Download from: https://www.python.org/downloads/release/python-31018/
    pause
    exit /b 1
)

:: 显示Python版本
echo Python version:
python --version

:: 检查是否为Python 3.10.x
python -c "import sys; version = sys.version_info; exit(0 if version.major == 3 and version.minor == 10 else 1)" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python version is not 3.10.x
    echo Current version:
    python --version
    echo.
    echo Do you want to continue anyway? (Y/N)
    set /p choice=
    if /i "%choice%" neq "Y" (
        echo Setup cancelled.
        pause
        exit /b 1
    )
)

:: 检查是否已存在虚拟环境
if exist "..\.venv\Scripts\activate.bat" (
    echo Found existing virtual environment at ..\.venv
    echo Do you want to recreate it? (Y/N)
    set /p recreate=
    if /i "%recreate%" equ "Y" (
        echo Removing existing environment...
        rmdir /s /q "..\.venv"
    ) else (
        echo Using existing environment...
        goto :activate_env
    )
)

:: 创建虚拟环境
echo Creating virtual environment...
python -m venv "..\.venv"

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Please check Python installation and permissions
    pause
    exit /b 1
)

:activate_env
:: 激活虚拟环境
echo Activating virtual environment...
call "..\.venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Expected location: ..\.venv\Scripts\activate.bat
    echo Current directory: %CD%
    pause
    exit /b 1
)

:: 升级pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: 安装核心依赖（使用国内镜像源）
echo Installing core dependencies...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ Pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ PyYAML
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil

:: 安装音频相关依赖
echo Installing audio dependencies...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame

:: 安装构建工具
echo Installing build tools...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 验证安装
echo Verifying installation...
python -c "import cv2, ultralytics, pygame; print('SUCCESS: All dependencies installed successfully!')"

if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed correctly
    echo You can manually install missing packages using:
    echo   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ [package_name]
) else (
    echo ========================================
    echo SUCCESS: Offline Python environment setup completed!
    echo ========================================
)

echo.
echo Environment location: ..\.venv
echo To activate manually: call ..\.venv\Scripts\activate.bat
echo.
echo To run the application:
echo   call ..\.venv\Scripts\activate.bat
echo   python ..\main_monitor_gui.py
echo.
pause 