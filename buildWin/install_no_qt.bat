@echo off
chcp 65001 >nul

echo ========================================
echo Installation without Qt6 (Avoid Large Downloads)
echo ========================================

echo Qt6 is not needed for our application.
echo Installing dependencies without Qt6...

:: 使用pip安装，完全避免conda的Qt6包
echo Installing with pip (avoiding Qt6)...

:: 基础包
echo Installing basic packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyyaml

:: OpenCV (headless版本，不需要GUI)
echo Installing OpenCV (headless version)...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python-headless

:: 其他包
echo Installing other packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 测试安装
echo.
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"
python -c "import pygame; print('✓ pygame OK')" 2>nul || echo "✗ pygame missing"

echo.
echo Installation completed without Qt6!
echo.
echo If you need GUI features later, you can install:
echo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python

pause 