@echo off
chcp 65001 >nul

echo ========================================
echo Installing All Dependencies
echo ========================================

echo Installing all required dependencies...

:: base packages
echo Installing basic packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ psutil
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyyaml

:: OpenCV
echo Installing OpenCV...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python-headless

:: other packages
echo Installing other packages...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygame
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller

:: pyautogui and its dependencies
echo Installing pyautogui and dependencies...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyautogui
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ mouseinfo
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pymsgbox
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pytweening
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyscreeze

:: test all dependencies
echo.
echo Testing all dependencies...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"
python -c "import pygame; print('✓ pygame OK')" 2>nul || echo "✗ pygame missing"
python -c "import pyautogui; print('✓ pyautogui OK')" 2>nul || echo "✗ pyautogui missing"
python -c "import PIL; print('✓ PIL OK')" 2>nul || echo "✗ PIL missing"

:: test main program
echo.
echo Testing main program...
python ..\main_monitor_gui_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Main program test failed!
    echo.
    echo Please check the error message above.
) else (
    echo.
    echo ========================================
    echo SUCCESS: All dependencies installed!
    echo ========================================
    echo.
    echo You can now run the build script:
    echo buildWin\build_aliyun_simple.bat
)

pause 