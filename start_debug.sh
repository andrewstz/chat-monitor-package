#!/bin/bash
# ChatMonitor GUI 调试启动脚本

echo "🚀 启动ChatMonitor GUI调试模式..."

# 激活conda环境
source ~/miniconda3/etc/profile.d/conda.sh
conda activate paddle

# 设置调试环境变量
export CHATMONITOR_DEBUG=1
export CHATMONITOR_VERBOSE=1

# 运行程序
echo "✅ 环境已激活: $(conda info --envs | grep '*' | awk '{print $1}')"
echo "🐍 Python路径: $(which python3)"
echo "🔧 调试模式已启用"

python3 main_monitor_gui_app.py

echo "✅ 程序已退出" 