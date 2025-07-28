@echo off
chcp 65001 >nul

echo ========================================
echo Ultra Minimal Installation
echo ========================================

echo Installing only absolutely necessary packages...

:: 只安装最基础的包，避免所有大型依赖
echo Installing minimal packages...

:: 1. psutil (必须)
echo Installing psutil...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil

:: 2. 轻量级OpenCV
echo Installing lightweight OpenCV...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python-headless

:: 3. 基础包
echo Installing basic packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyyaml

:: 4. ultralytics
echo Installing ultralytics...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics

:: 5. pyinstaller
echo Installing pyinstaller...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 测试
echo.
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"

echo.
echo Ultra minimal installation completed!
echo.
echo Note: pygame is not installed (not essential for core functionality)
echo If you need pygame later: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame

pause 