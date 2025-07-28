@echo off
chcp 65001 >nul
echo ========================================
echo Setting up UV environment with local Python 3.10.11
echo ========================================

:: 检查本地Python安装
echo Checking local Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please ensure Python 3.10.11 is installed and in PATH
    pause
    exit /b 1
)

:: 显示Python版本
echo Found Python version:
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

:: 检查是否已存在UV环境
if exist "..\.venv\Scripts\activate.bat" (
    echo Found existing UV environment at ..\.venv
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

:: 使用本地Python创建UV环境
echo Creating UV environment with local Python 3.10.11...
uv venv --python 3.10.11

if errorlevel 1 (
    echo Trying alternative method with local Python...
    uv venv --python python
)

if errorlevel 1 (
    echo ERROR: Failed to create UV environment
    echo Trying to use system Python directly...
    python -m venv "..\.venv"
    if errorlevel 1 (
        echo ERROR: All methods failed
        pause
        exit /b 1
    )
)

:activate_env
:: 激活环境
echo Activating environment...
if exist "..\.venv\Scripts\activate.bat" (
    call "..\.venv\Scripts\activate.bat"
) else (
    echo ERROR: Environment not found!
    echo Expected location: ..\.venv
    echo Current directory: %CD%
    pause
    exit /b 1
)

:: 验证Python版本
echo Verifying Python version in environment...
python --version

:: 安装核心依赖（使用镜像源）
echo Installing core dependencies with mirror...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil

:: 安装音频相关依赖
echo Installing audio dependencies...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame

:: 安装构建工具
echo Installing build tools...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 验证安装
echo Verifying installation...
python -c "import cv2, ultralytics, pygame; print('SUCCESS: All dependencies installed successfully!')"

if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed correctly
    echo You can manually install missing packages using:
    echo   uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ [package_name]
) else (
    echo ========================================
    echo SUCCESS: UV environment setup completed!
    echo ========================================
)

echo.
echo Environment location: ..\.venv
echo Python version: 3.10.11
echo To activate manually: call ..\.venv\Scripts\activate.bat
echo.
echo To verify environment:
echo   python -c "import cv2, ultralytics, pygame; print('Environment ready!')"
echo.
pause 