@echo off
chcp 65001 >nul

echo ========================================
echo Fixed Encoding Installation Script
echo ========================================

echo Installing dependencies with fixed encoding...

:: Install basic packages
echo Installing basic packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyyaml

:: Install OpenCV
echo Installing OpenCV...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python-headless

:: Install other packages
echo Installing other packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: Test installation
echo.
echo Testing installation...
python -c "import psutil; print('psutil OK')" 2>nul || echo "psutil missing"
python -c "import cv2; print('cv2 OK')" 2>nul || echo "cv2 missing"
python -c "import ultralytics; print('ultralytics OK')" 2>nul || echo "ultralytics missing"
python -c "import pygame; print('pygame OK')" 2>nul || echo "pygame missing"

echo.
echo Installation completed!
pause 