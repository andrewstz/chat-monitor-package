@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🪟 ChatMonitor Windows 环境安装脚本
echo 📁 当前目录: %cd%

:: 检查Python环境
echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python版本:
python --version

:: 检查pip
echo 🔍 检查pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip未安装或不可用
    pause
    exit /b 1
)

echo ✅ pip可用

:: 升级pip
echo 📦 升级pip...
python -m pip install --upgrade pip

:: 安装依赖包
echo 📦 安装Python依赖包...
echo 💡 使用国内镜像源加速下载...

:: 设置pip镜像源
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
set PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

:: 安装核心依赖
echo 📦 安装核心依赖...
python -m pip install -r requirements_windows.txt

if errorlevel 1 (
    echo ❌ 依赖安装失败
    echo 💡 尝试使用默认源安装...
    python -m pip install -r requirements_windows.txt
)

:: 安装PyInstaller
echo 📦 安装PyInstaller...
python -m pip install pyinstaller

:: 检查macOS图标
echo 🎨 检查macOS图标...
if exist "assets\icons\icon.png" (
    echo   ✅ 找到macOS图标文件
) else (
    echo   ⚠️  未找到图标文件
    echo   💡 建议在macOS上运行: python create_png_icon.py
    echo   💡 然后将整个目录复制到Windows环境
)

:: 检查必要文件
echo 🔍 检查必要文件...
set REQUIRED_FILES=main_monitor_gui_app.py config_with_yolo.yaml fuzzy_matcher.py config_manager.py network_monitor.py

for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo ❌ 缺少必要文件: %%f
        echo 💡 请确保在正确的目录中运行此脚本
        pause
        exit /b 1
    )
    echo   ✅ %%f
)

:: 检查Tesseract
echo 🔍 检查Tesseract OCR...
python -c "import pytesseract; print('Tesseract路径:', pytesseract.get_tesseract_version())" 2>nul
if errorlevel 1 (
    echo ⚠️  Tesseract未安装或配置
    echo 💡 请安装Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
    echo 💡 或者下载预编译版本
)

:: 创建测试脚本
echo 🔧 创建测试脚本...
echo @echo off > test_windows_setup.bat
echo echo 🧪 测试Windows环境... >> test_windows_setup.bat
echo python -c "import cv2; import numpy; import psutil; import pyautogui; import requests; import yaml; import PIL; import pytesseract; import playsound; import watchdog; import ultralytics; import tkinter; print('✅ 所有依赖包导入成功')" >> test_windows_setup.bat
echo pause >> test_windows_setup.bat

echo.
echo 🎉 Windows环境安装完成！
echo.
echo 📋 下一步操作:
echo   1. 运行 test_windows_setup.bat 测试环境
echo   2. 运行 build_windows_app.bat 构建应用程序
echo   3. 在release目录找到绿色版应用程序
echo.
echo 💡 提示:
echo   - 如果Tesseract未安装，OCR功能可能不可用
echo   - 首次运行可能需要允许防火墙访问
echo   - 建议在虚拟机中测试后再部署到生产环境
echo.
pause 