#!/bin/bash
# -*- coding: utf-8 -*-
"""
停止所有ChatMonitor相关进程
"""

echo "🛑 停止所有ChatMonitor进程..."

# 停止主程序
if pgrep -f "main_monitor_gui_app.py" > /dev/null; then
    echo "🛑 停止主程序..."
    pkill -f "main_monitor_gui_app.py"
    sleep 2
else
    echo "ℹ️ 主程序未运行"
fi

# 停止守护进程
if pgrep -f "daemon_monitor_latest.py" > /dev/null; then
    echo "🛑 停止守护进程..."
    pkill -f "daemon_monitor_latest.py"
    sleep 2
else
    echo "ℹ️ 守护进程未运行"
fi

# 检查是否还有进程在运行
if pgrep -f "main_monitor_gui_app.py" > /dev/null || pgrep -f "daemon_monitor_latest.py" > /dev/null; then
    echo "⚠️ 强制终止剩余进程..."
    pkill -9 -f "main_monitor_gui_app.py" 2>/dev/null
    pkill -9 -f "daemon_monitor_latest.py" 2>/dev/null
fi

echo "✅ 所有ChatMonitor进程已停止" 