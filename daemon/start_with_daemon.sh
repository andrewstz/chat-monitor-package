#!/bin/bash

# ChatMonitor 启动脚本（支持守护进程）
# 用法: ./start_with_daemon.sh [--daemon]

set -e

# 切换到上级目录（项目根目录）
cd "$(dirname "$0")/.."

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

# 检查守护进程文件
if [ ! -f "daemon/simple_daemon.py" ]; then
    echo "❌ 未找到daemon/simple_daemon.py文件"
    exit 1
fi

# 检查参数
if [ "$1" = "--daemon" ]; then
    echo "🚀 启动ChatMonitor（守护进程模式）"
    echo "📝 守护进程将监控应用状态，自动重启崩溃的应用"
    echo "📝 日志文件: /tmp/chatmonitor_daemon.log"
    echo ""
    
    # 启动守护进程
    python daemon/simple_daemon.py
else
    echo "🚀 启动ChatMonitor（普通模式）"
    echo "📝 直接启动应用，无守护进程"
    echo ""
    
    # 直接启动应用
    python main_monitor_gui_app.py
fi 