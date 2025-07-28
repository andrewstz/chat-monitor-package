#!/bin/bash

echo "========================================"
echo "Quick Build with System Python (macOS)"
echo "========================================"

# 检查Python
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found"
    exit 1
fi

# 直接构建（假设依赖已安装）
echo "Building application..."
echo "This may take several minutes..."

# 使用PyInstaller构建macOS应用
pyinstaller --onefile \
    --windowed \
    --name ChatMonitor \
    --add-data "../sounds:." \
    --add-data "../models:." \
    --add-data "../config_with_yolo.yaml:." \
    "../main_monitor_gui.py"

# 检查结果
if [ -f "dist/ChatMonitor" ]; then
    echo "========================================"
    echo "SUCCESS: ChatMonitor created!"
    echo "========================================"
    echo "Location: dist/ChatMonitor"
    echo
    echo "To run: ./dist/ChatMonitor"
    echo
    echo "File size:"
    ls -lh dist/ChatMonitor
else
    echo "ERROR: Build failed"
    echo
    echo "If dependencies are missing, run:"
    echo "  pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil pygame pyinstaller"
fi 