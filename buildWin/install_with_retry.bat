@echo off
chcp 65001 >nul

echo ========================================
echo Installation with Retry Mechanism
echo ========================================

:: 设置重试次数
set max_retries=3

:: 安装函数
:install_package
set package_name=%1
set retry_count=0

:retry_loop
echo Installing %package_name% (attempt %retry_count% of %max_retries%)...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout 600 %package_name%

if errorlevel 1 (
    set /a retry_count+=1
    if %retry_count% lss %max_retries% (
        echo Failed, retrying in 5 seconds...
        timeout /t 5 /nobreak >nul
        goto :retry_loop
    ) else (
        echo Failed to install %package_name% after %max_retries% attempts
        echo Please check your network connection
        pause
        exit /b 1
    )
) else (
    echo ✓ %package_name% installed successfully
)
goto :eof

:: 开始安装
echo Starting installation with retry mechanism...

:: 安装基础包
call :install_package psutil
call :install_package pillow
call :install_package requests
call :install_package pyyaml

:: 安装OpenCV
call :install_package opencv-python-headless

:: 安装其他包
call :install_package pygame
call :install_package ultralytics
call :install_package pyinstaller

:: 测试
echo.
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"

echo.
echo Installation completed with retry mechanism!
pause 