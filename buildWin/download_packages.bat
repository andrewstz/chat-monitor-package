@echo off
chcp 65001 >nul
echo ========================================
echo Downloading Python Packages for Offline Installation
echo ========================================

:: 创建下载目录
if not exist "packages" mkdir packages
cd packages

echo Downloading packages to: %CD%
echo.

:: 下载所有必需的包
echo Downloading opencv-python...
pip download opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading ultralytics...
pip download ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading Pillow...
pip download Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading requests...
pip download requests -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading PyYAML...
pip download PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading psutil...
pip download psutil -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading pygame...
pip download pygame -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo Downloading pyinstaller...
pip download pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/

:: 下载依赖的依赖包
echo Downloading additional dependencies...
pip download numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download wheel -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo.
echo ========================================
echo Download Complete!
echo ========================================
echo.
echo Files downloaded to: packages\
echo.
echo To transfer to internal network:
echo 1. Copy the entire 'packages' folder
echo 2. Transfer to internal network machine
echo 3. Run: .\install_offline_packages.bat
echo.
pause 