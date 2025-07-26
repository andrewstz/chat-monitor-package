#!/bin/bash

# ChatMonitor 启动脚本
# 展示如何使用修改后的 main_monitor_gui_app.py

set -e

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ 未找到python命令，请确保已激活conda环境"
    exit 1
fi

# 检查主程序文件
if [ ! -f "main_monitor_gui_app.py" ]; then
    echo "❌ 未找到main_monitor_gui_app.py文件"
    exit 1
fi

echo "🚀 ChatMonitor 启动选项："
echo ""
echo "1. 普通模式（无守护进程）"
echo "   python main_monitor_gui_app.py"
echo ""
echo "2. 守护进程模式"
echo "   python main_monitor_gui_app.py --daemon"
echo ""
echo "3. 禁用守护进程模式"
echo "   python main_monitor_gui_app.py --no-daemon"
echo ""

# 默认启动普通模式
echo "📝 启动普通模式..."
python main_monitor_gui_app.py 