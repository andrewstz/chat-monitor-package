#!/bin/bash
# -*- coding: utf-8 -*-
"""
启动ChatMonitor应用和守护进程
"""

echo "🚀 启动ChatMonitor应用和守护进程..."

# 检查conda环境
if command -v conda &> /dev/null; then
    echo "📦 检测到conda环境，激活paddle环境..."
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate paddle
fi

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到python命令"
    exit 1
fi

# 检查必要文件
if [ ! -f "main_monitor_gui_app.py" ]; then
    echo "❌ 错误: 未找到main_monitor_gui_app.py"
    exit 1
fi

if [ ! -f "daemon/daemon_monitor_latest.py" ]; then
    echo "❌ 错误: 未找到daemon/daemon_monitor_latest.py"
    exit 1
fi

# 检查是否已有守护进程在运行
if pgrep -f "daemon_monitor_latest.py" > /dev/null; then
    echo "⚠️ 检测到守护进程已在运行"
    DAEMON_PID=$(pgrep -f "daemon_monitor_latest.py")
    echo "守护进程PID: $DAEMON_PID"
else
    echo "🛡️ 启动守护进程..."
    python daemon/daemon_monitor_latest.py &
    DAEMON_PID=$!
    echo "守护进程PID: $DAEMON_PID"
fi

# 等待守护进程启动
sleep 2

# 检查主程序是否在运行
if pgrep -f "main_monitor_gui_app.py" > /dev/null; then
    echo "✅ 主程序已在运行"
    MAIN_PID=$(pgrep -f "main_monitor_gui_app.py")
    echo "主程序PID: $MAIN_PID"
else
    echo "🚀 启动主程序..."
    python main_monitor_gui_app.py &
    MAIN_PID=$!
    echo "主程序PID: $MAIN_PID"
fi

echo ""
echo "✅ ChatMonitor已启动"
echo "📊 进程信息:"
echo "  守护进程: PID $DAEMON_PID"
echo "  主程序: PID $MAIN_PID"
echo ""
echo "💡 提示:"
echo "  - 关闭主程序窗口后，守护进程会自动重启"
echo "  - 查看守护进程日志: tail -f /tmp/chatmonitor_daemon.log"
echo "  - 停止所有进程: ./daemon/stop_all_latest.sh"
echo "" 