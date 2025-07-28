@echo off
chcp 65001 >nul

echo ========================================
echo Pip-Only Installation (Avoid Conda Network Issues)
echo ========================================

echo Avoiding conda network issues by using pip only...

:: 清理可能的缓存问题
echo Cleaning potential cache issues...
pip cache purge

:: 使用pip安装所有依赖，完全避免conda
echo Installing all dependencies with pip...

:: 基础包
echo Installing basic packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 psutil
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 pyyaml

:: OpenCV (headless版本，避免Qt6)
echo Installing OpenCV (headless version)...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 opencv-python-headless

:: 其他包
echo Installing other packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 pygame
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 300 pyinstaller

:: 测试安装
echo.
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"
python -c "import pygame; print('✓ pygame OK')" 2>nul || echo "✗ pygame missing"

echo.
echo Pip-only installation completed!
echo.
echo If you still have issues, try:
echo 1. Check your network connection
echo 2. Try a different network
echo 3. Use a VPN if available

pause 