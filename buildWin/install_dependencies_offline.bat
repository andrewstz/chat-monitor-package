@echo off
chcp 65001 >nul
echo ========================================
echo Offline Dependency Installation
echo ========================================

:: 检查是否有预下载的包
if exist "packages" (
    echo Found packages directory, installing from local files...
    goto :install_from_local
)

:: 尝试使用不同的镜像源安装
echo Installing dependencies with different mirrors...

:: 尝试清华镜像源
echo Trying Tsinghua mirror...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python --timeout 60
if errorlevel 1 (
    echo Tsinghua mirror failed, trying Aliyun...
    pip install -i https://mirrors.aliyun.com/pypi/simple/ opencv-python --timeout 60
)

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics --timeout 60
if errorlevel 1 (
    pip install -i https://mirrors.aliyun.com/pypi/simple/ ultralytics --timeout 60
)

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ Pillow --timeout 60
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests --timeout 60
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ PyYAML --timeout 60
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil --timeout 60
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame --timeout 60
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller --timeout 60

goto :verify_installation

:install_from_local
echo Installing from local packages...
cd packages
for %%f in (*.whl) do (
    echo Installing %%f...
    pip install %%f
)
cd ..

:verify_installation
:: 验证安装
echo.
echo Verifying installation...
python -c "import cv2; print('OpenCV: OK')" 2>nul
python -c "import ultralytics; print('Ultralytics: OK')" 2>nul
python -c "import pygame; print('Pygame: OK')" 2>nul

if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed correctly
    echo.
    echo Manual installation commands:
    echo pip install opencv-python
    echo pip install ultralytics
    echo pip install pygame
    echo pip install pyinstaller
) else (
    echo ========================================
    echo SUCCESS: Dependencies installed!
    echo ========================================
    echo.
    echo You can now run: .\build_quick.bat
)

pause 