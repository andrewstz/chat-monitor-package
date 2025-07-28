@echo off
chcp 65001 >nul

echo ========================================
echo Installing Dependencies in Conda Environment
echo ========================================

:: 检查conda环境
echo Current conda environment:
conda info --envs
echo.

:: 检查Python版本
echo Python version:
python --version
echo.

:: 方法1: 使用conda安装主要依赖
echo Installing dependencies with conda...
conda install -y -c conda-forge opencv
conda install -y -c conda-forge pillow
conda install -y -c conda-forge requests
conda install -y -c conda-forge pyyaml
conda install -y -c conda-forge psutil
conda install -y -c conda-forge pygame
conda install -y -c conda-forge pyinstaller

:: 方法2: 使用pip安装conda中没有的包
echo Installing additional packages with pip...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ultralytics

:: 验证安装
echo.
echo ========================================
echo Verifying installations...
echo ========================================

python -c "import cv2; print('✓ OpenCV:', cv2.__version__)" 2>nul || echo "✗ OpenCV missing"
python -c "import ultralytics; print('✓ Ultralytics:', ultralytics.__version__)" 2>nul || echo "✗ Ultralytics missing"
python -c "import PIL; print('✓ Pillow:', PIL.__version__)" 2>nul || echo "✗ Pillow missing"
python -c "import requests; print('✓ Requests:', requests.__version__)" 2>nul || echo "✗ Requests missing"
python -c "import yaml; print('✓ PyYAML: OK')" 2>nul || echo "✗ PyYAML missing"
python -c "import psutil; print('✓ psutil:', psutil.__version__)" 2>nul || echo "✗ psutil missing"
python -c "import pygame; print('✓ pygame:', pygame.version.ver)" 2>nul || echo "✗ pygame missing"
python -c "import PyInstaller; print('✓ PyInstaller:', PyInstaller.__version__)" 2>nul || echo "✗ PyInstaller missing"

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
echo You can now run:
echo buildWin/build_conda_simple.bat
echo.

pause 