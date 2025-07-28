@echo off
chcp 65001 >nul

echo ========================================
echo Step-by-Step Installation
echo ========================================

:: 步骤1: 安装基础包
echo Step 1: Installing basic packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil
echo.
echo Press any key to continue to next step...
pause

:: 步骤2: 安装OpenCV
echo Step 2: Installing OpenCV (headless version)...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python-headless
echo.
echo Press any key to continue to next step...
pause

:: 步骤3: 安装其他包
echo Step 3: Installing other packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow requests pyyaml pygame
echo.
echo Press any key to continue to next step...
pause

:: 步骤4: 安装ultralytics
echo Step 4: Installing ultralytics...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
echo.
echo Press any key to continue to next step...
pause

:: 步骤5: 安装pyinstaller
echo Step 5: Installing pyinstaller...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller
echo.
echo Press any key to test installation...
pause

:: 测试
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"

echo.
echo Installation completed!
pause 