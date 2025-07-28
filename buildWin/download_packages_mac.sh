#!/bin/bash

echo "========================================"
echo "Downloading Python Packages for Offline Installation (macOS)"
echo "========================================"

# 创建下载目录
if [ ! -d "packages" ]; then
    mkdir packages
fi
cd packages

echo "Downloading packages to: $(pwd)"
echo

# 下载所有必需的包
echo "Downloading opencv-python..."
pip3 download opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading ultralytics..."
pip3 download ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading Pillow..."
pip3 download Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading requests..."
pip3 download requests -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading PyYAML..."
pip3 download PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading psutil..."
pip3 download psutil -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading pygame..."
pip3 download pygame -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "Downloading pyinstaller..."
pip3 download pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 下载依赖的依赖包
echo "Downloading additional dependencies..."
pip3 download numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download wheel -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 下载macOS特定的依赖
echo "Downloading macOS specific dependencies..."
pip3 download pyobjc-core -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download pyobjc-framework-Cocoa -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo
echo "========================================"
echo "Download Complete!"
echo "========================================"
echo
echo "Files downloaded to: packages/"
echo
echo "To transfer to Windows internal network:"
echo "1. Copy the entire 'packages' folder"
echo "2. Transfer to Windows internal network machine"
echo "3. Run: .\\install_offline_packages.bat"
echo
echo "Package list:"
ls -la *.whl
echo
echo "Total size:"
du -sh .
echo 