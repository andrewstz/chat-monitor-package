@echo off
chcp 65001 >nul
echo ========================================
echo Smart Offline Package Installation
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

:: 进入packages目录
cd packages

:: 显示所有可用的包
echo Available packages:
dir *.whl
echo.

:: 按依赖顺序安装
echo Installing packages in dependency order...

:: 1. 安装基础工具
echo Installing setuptools...
for %%f in (setuptools*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

echo Installing wheel...
for %%f in (wheel*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

:: 2. 安装numpy
echo Installing numpy...
for %%f in (numpy*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

:: 3. 安装核心包
echo Installing core packages...
for %%f in (opencv_python*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (ultralytics*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (pygame*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (pyinstaller*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (Pillow*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (requests*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (PyYAML*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

for %%f in (psutil*.whl) do (
    echo Installing %%f...
    pip install "%%f"
)

:: 4. 安装其他依赖
echo Installing other dependencies...
for %%f in (*.whl) do (
    echo Installing %%f...
    pip install "%%f"
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
    echo You can try installing individual packages manually:
    echo   cd packages
    echo   pip install [exact_filename].whl
) else (
    echo ========================================
    echo SUCCESS: All packages installed!
    echo ========================================
    echo.
    echo You can now run: .\build_quick.bat
)

echo.
pause 