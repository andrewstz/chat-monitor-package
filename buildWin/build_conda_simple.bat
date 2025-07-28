@echo off
chcp 65001 >nul

echo ========================================
echo Simple Conda Build for ChatMonitor
echo ========================================

:: 检查conda环境
echo Current conda environment:
conda info --envs
echo.

:: 检查Python
echo Python version:
python --version
echo.

:: 安装依赖
echo Installing dependencies...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil pygame pyinstaller

:: 清理
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: 简单构建
echo Building application...
pyinstaller --onefile --windowed --name ChatMonitor --add-data "..\sounds;sounds" --add-data "..\models;models" --add-data "..\config_with_yolo.yaml;." "..\main_monitor_gui_app.py"

:: 检查结果
if exist "dist\ChatMonitor.exe" (
    echo ========================================
    echo SUCCESS: ChatMonitor.exe created!
    echo ========================================
    echo Location: dist\ChatMonitor.exe
    echo.
    echo To test: dist\ChatMonitor.exe
) else (
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo.
    echo Try these steps:
    echo 1. pip install --upgrade pyinstaller
    echo 2. Check if main_monitor_gui_app.py exists
    echo 3. Try running the script directly: python ..\main_monitor_gui_app.py
)

pause 