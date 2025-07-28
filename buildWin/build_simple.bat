@echo off
chcp 65001 >nul
echo ========================================
echo Simple Build with System Python
echo ========================================

:: 检查Python
python --version
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

:: 安装依赖（如果未安装）
echo Installing dependencies...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil pygame pyinstaller

:: 构建应用
echo Building application...
pyinstaller --onefile --windowed --name ChatMonitor --add-data "..\sounds;." --add-data "..\models;." --add-data "..\config_with_yolo.yaml;." "..\main_monitor_gui.py"

:: 检查结果
if exist "dist\ChatMonitor.exe" (
    echo ========================================
    echo SUCCESS: ChatMonitor.exe created!
    echo ========================================
    echo Location: dist\ChatMonitor.exe
    echo.
    echo To run: dist\ChatMonitor.exe
) else (
    echo ERROR: Build failed
)

pause 