#!/bin/bash
# 启动发信人设置GUI脚本

echo "🚀 启动发信人设置GUI..."

# 激活conda环境
source ~/miniconda3/etc/profile.d/conda.sh
conda activate paddle

# 运行GUI
python3 contact_input_gui.py

echo "✅ GUI已关闭" 