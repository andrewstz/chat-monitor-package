@echo off
chcp 65001 >nul
echo ========================================
echo Setting up UV environment with mirror
echo ========================================

:: 检查是否已存在UV环境
if exist "..\.venv\Scripts\activate.bat" (
    echo Found existing UV environment at ..\.venv
    goto :activate_env
)

:: 创建新的UV环境，使用国内镜像源
echo Creating new UV environment with Python 3.10.18...
uv venv --python 3.10.18 --index-url https://pypi.tuna.tsinghua.edu.cn/simple/

if errorlevel 1 (
    echo Failed to create UV environment with mirror, trying alternative mirror...
    uv venv --python 3.10.18 --index-url https://mirrors.aliyun.com/pypi/simple/
)

if errorlevel 1 (
    echo Failed to create UV environment with Aliyun mirror, trying Douban mirror...
    uv venv --python 3.10.18 --index-url https://pypi.douban.com/simple/
)

:activate_env
:: 激活环境
if exist "..\.venv\Scripts\activate.bat" (
    echo Activating UV environment...
    call "..\.venv\Scripts\activate.bat"
) else (
    echo ERROR: UV environment not found!
    echo Expected location: ..\.venv
    echo Current directory: %CD%
    echo Parent directory contents:
    dir ".." | findstr "venv"
    pause
    exit /b 1
)

:: 验证Python版本
echo Verifying Python version...
python --version

:: 安装核心依赖（使用镜像源）
echo Installing core dependencies with mirror...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil

:: 安装音频相关依赖（使用镜像源）
echo Installing audio dependencies with mirror...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame

:: 安装构建工具（使用镜像源）
echo Installing build tools with mirror...
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

echo ========================================
echo UV environment setup completed!
echo ========================================
echo.
echo To activate the environment manually:
echo   call ..\.venv\Scripts\activate.bat
echo.
echo To verify installation:
echo   python -c "import cv2, ultralytics, pygame; print('All dependencies installed successfully!')"
echo.
pause 