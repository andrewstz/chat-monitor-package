#!/bin/bash

echo "========================================"
echo "Installing Offline Python Packages (macOS)"
echo "========================================"

# 检查packages目录是否存在
if [ ! -d "packages" ]; then
    echo "ERROR: packages directory not found!"
    echo
    echo "Please ensure the 'packages' folder is in the current directory."
    echo "This folder should contain .whl files downloaded from external network."
    echo
    exit 1
fi

echo "Found packages directory: packages/"
echo

# 检查Python版本
python3 --version
echo

# 安装所有.whl文件
echo "Installing packages from local files..."
cd packages

# 按依赖顺序安装
echo "Installing setuptools and wheel first..."
for file in setuptools*.whl; do
    if [ -f "$file" ]; then
        echo "Installing $file..."
        pip3 install "$file"
    fi
done

for file in wheel*.whl; do
    if [ -f "$file" ]; then
        echo "Installing $file..."
        pip3 install "$file"
    fi
done

echo "Installing numpy..."
for file in numpy*.whl; do
    if [ -f "$file" ]; then
        echo "Installing $file..."
        pip3 install "$file"
    fi
done

echo "Installing core packages..."
for file in *.whl; do
    if [ -f "$file" ]; then
        echo "Installing $file..."
        pip3 install "$file"
    fi
done

cd ..

# 验证安装
echo
echo "Verifying installation..."
python3 -c "import cv2; print('OpenCV: OK')" 2>/dev/null
python3 -c "import ultralytics; print('Ultralytics: OK')" 2>/dev/null
python3 -c "import pygame; print('Pygame: OK')" 2>/dev/null
python3 -c "import PyInstaller; print('PyInstaller: OK')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "WARNING: Some packages may not be installed correctly"
    echo
    echo "You can try installing individual packages:"
    echo "  pip3 install packages/opencv_python*.whl"
    echo "  pip3 install packages/ultralytics*.whl"
    echo "  pip3 install packages/pygame*.whl"
    echo "  pip3 install packages/pyinstaller*.whl"
else
    echo "========================================"
    echo "SUCCESS: All packages installed!"
    echo "========================================"
    echo
    echo "You can now run: ./build_quick_mac.sh"
fi

echo 