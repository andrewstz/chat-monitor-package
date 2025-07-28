@echo off
chcp 65001 >nul

echo ========================================
echo Minimal Installation (Avoid Large Packages)
echo ========================================

:: 只安装必要的包，避免大型包
echo Installing minimal dependencies...

:: 使用pip安装，避免conda的大型包
echo Installing with pip (avoiding large conda packages)...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python-headless
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyyaml
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: 测试
echo.
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"

echo.
echo Minimal installation completed!
echo.
echo If you need full OpenCV features, run:
echo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python

pause 