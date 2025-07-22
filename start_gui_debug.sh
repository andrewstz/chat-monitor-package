#!/bin/bash
# ChatMonitor GUI调试启动脚本 - 绕过YOLO初始化

echo "🚀 启动ChatMonitor GUI调试模式（绕过YOLO初始化）..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate paddle

# 设置环境变量，禁用YOLO
export CHATMONITOR_DISABLE_YOLO=1
export CHATMONITOR_DEBUG=1
export CHATMONITOR_VERBOSE=1

echo "✅ 环境已激活: $(conda info --envs | grep '*' | awk '{print $1}')"
echo "🐍 Python路径: $(which python3)"
echo "🔧 调试模式已启用"
echo "🚫 YOLO已禁用"

# 直接启动GUI，跳过复杂的初始化
python3 main_monitor_gui_app.py

echo "✅ 程序已退出" 