@echo off
chcp 65001 >nul

echo ========================================
echo One-Click Conda Dependencies Installer
echo ========================================

:: 检查conda
conda --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: conda not found!
    echo Please install Anaconda or Miniconda first.
    pause
    exit /b 1
)

echo Installing all dependencies...

:: 使用conda安装主要包
echo Installing with conda...
conda install -y -c conda-forge opencv pillow requests pyyaml psutil pygame pyinstaller

:: 使用pip安装conda中没有的包
echo Installing with pip...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics

:: 测试主程序
echo.
echo Testing main program...
python ..\main_monitor_gui_app.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Main program test failed!
    echo ========================================
    echo.
    echo Manual installation commands:
    echo conda install -c conda-forge opencv pillow requests pyyaml psutil pygame pyinstaller
    echo pip install ultralytics
) else (
    echo.
    echo ========================================
    echo SUCCESS: All dependencies installed!
    echo ========================================
    echo.
    echo You can now build the application:
    echo buildWin/build_conda_simple.bat
)

pause 