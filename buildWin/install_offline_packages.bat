@echo off
chcp 65001 >nul
echo ========================================
echo Installing Offline Python Packages
echo ========================================

:: 检查packages目录是否存在
if not exist "packages" (
    echo ERROR: packages directory not found!
    echo.
    echo Please ensure the 'packages' folder is in the current directory.
    echo This folder should contain .whl files downloaded from external network.
    echo.
    pause
    exit /b 1
)

echo Found packages directory: packages\
echo.

:: 检查Python版本
python --version
echo.

:: 安装所有.whl文件
echo Installing packages from local files...
cd packages

:: 按依赖顺序安装
echo Installing setuptools and wheel first...
for %%f in (setuptools*.whl) do (
    echo Installing %%f...
    pip install %%f
)

for %%f in (wheel*.whl) do (
    echo Installing %%f...
    pip install %%f
)

echo Installing numpy...
for %%f in (numpy*.whl) do (
    echo Installing %%f...
    pip install %%f
)

echo Installing core packages...
for %%f in (*.whl) do (
    echo Installing %%f...
    pip install %%f
)

cd ..

:: 验证安装
echo.
echo Verifying installation...
python -c "import cv2; print('OpenCV: OK')" 2>nul
python -c "import ultralytics; print('Ultralytics: OK')" 2>nul
python -c "import pygame; print('Pygame: OK')" 2>nul
python -c "import PyInstaller; print('PyInstaller: OK')" 2>nul

if errorlevel 1 (
    echo WARNING: Some packages may not be installed correctly
    echo.
    echo You can try installing individual packages:
    echo   pip install packages\opencv_python*.whl
    echo   pip install packages\ultralytics*.whl
    echo   pip install packages\pygame*.whl
    echo   pip install packages\pyinstaller*.whl
) else (
    echo ========================================
    echo SUCCESS: All packages installed!
    echo ========================================
    echo.
    echo You can now run: .\build_quick.bat
)

echo.
pause 