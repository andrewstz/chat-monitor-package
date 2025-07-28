@echo off
chcp 65001 >nul
echo ========================================
echo Smart UV Environment Setup
echo ========================================

:: 检查本地Python安装
echo Checking local Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please ensure Python is installed and in PATH
    pause
    exit /b 1
)

:: 获取Python版本信息
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python version: %PYTHON_VERSION%

:: 解析版本号
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

echo Python Major: %PYTHON_MAJOR%, Minor: %PYTHON_MINOR%

:: 检查版本兼容性
if %PYTHON_MAJOR% neq 3 (
    echo ERROR: Python 3.x is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

:: 版本兼容性检查
if %PYTHON_MINOR% lss 8 (
    echo WARNING: Python 3.8+ is recommended for best compatibility
    echo Current version: %PYTHON_VERSION%
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

:: 使用当前Python版本创建UV环境
echo Creating UV environment with Python %PYTHON_VERSION%...
uv venv --python python

if errorlevel 1 (
    echo Trying alternative method...
    python -m venv "..\.venv"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
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
    pause
    exit /b 1
)

:: 验证Python版本
echo Verifying Python version in environment...
python --version

:: 根据Python版本调整依赖安装
echo Installing dependencies for Python %PYTHON_VERSION%...

:: 核心依赖（所有版本通用）
echo Installing core dependencies...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python Pillow requests PyYAML psutil pygame

:: 根据Python版本安装ultralytics
if %PYTHON_MINOR% geq 8 (
    echo Installing ultralytics for Python 3.%PYTHON_MINOR%...
    uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
) else (
    echo WARNING: ultralytics may not be compatible with Python 3.%PYTHON_MINOR%
    echo Skipping ultralytics installation
)

:: 安装构建工具
echo Installing build tools...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 验证安装
echo Verifying installation...
python -c "import cv2, pygame; print('Core dependencies: OK')"

if %PYTHON_MINOR% geq 8 (
    python -c "import ultralytics; print('Ultralytics: OK')"
) else (
    echo Ultralytics: Skipped (Python 3.%PYTHON_MINOR% compatibility)
)

echo ========================================
echo SUCCESS: UV environment setup completed!
echo ========================================
echo.
echo Environment details:
echo - Python version: %PYTHON_VERSION%
echo - Environment location: ..\.venv
echo - Ultralytics: %PYTHON_MINOR% geq 8 ? "Installed" : "Skipped"
echo.
echo To activate manually: call ..\.venv\Scripts\activate.bat
echo.
echo To test the environment:
echo   python -c "import cv2, pygame; print('Environment ready!')"
echo.
pause 