@echo off
chcp 65001 >nul

echo ========================================
echo Offline Conda Installation
echo ========================================

:: 检查是否有预下载的包
if exist "packages" (
    echo Found packages directory, installing from local files...
    cd packages
    for %%f in (*.whl) do (
        echo Installing %%f...
        pip install %%f
    )
    cd ..
    goto :test
)

:: 使用国内镜像源
echo Using Chinese mirrors to avoid network issues...

:: 方法1: 使用清华镜像
echo Trying Tsinghua mirror...
conda install -y -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ opencv pillow requests pyyaml psutil pygame pyinstaller

:: 方法2: 如果清华镜像失败，使用阿里云镜像
if errorlevel 1 (
    echo Tsinghua mirror failed, trying Aliyun...
    conda install -y -c https://mirrors.aliyun.com/anaconda/pkgs/main/ opencv pillow requests pyyaml psutil pygame pyinstaller
)

:: 安装ultralytics
echo Installing ultralytics...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics

:test
:: 测试安装
echo.
echo Testing installation...
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil missing"
python -c "import cv2; print('✓ cv2 OK')" 2>nul || echo "✗ cv2 missing"
python -c "import ultralytics; print('✓ ultralytics OK')" 2>nul || echo "✗ ultralytics missing"

echo.
echo Installation completed!
pause 