#!/bin/bash
# 直接运行Python脚本进行调试

echo "🔧 直接运行Python脚本调试模式"

# 设置调试环境变量
export CHATMONITOR_DEBUG=1

# 检查是否在conda环境中
if ! command -v conda &> /dev/null; then
    echo "❌ 未找到conda，请先激活conda环境"
    exit 1
fi

# 激活conda环境
echo "🐍 激活conda paddle环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate paddle

# 直接运行Python脚本
echo "🚀 启动Python脚本调试..."
python main_monitor_gui_app.py 