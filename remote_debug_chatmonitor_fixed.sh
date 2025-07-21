#!/bin/bash
# ChatMonitor远程调试启动脚本（修复版）

echo "🔧 ChatMonitor远程调试模式启动"

# 设置远程调试环境变量
export CHATMONITOR_REMOTE_DEBUG=1
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 检查开发环境文件
if [ -f "main_monitor_dynamic.py" ]; then
    echo "📱 启动开发环境应用程序（远程调试模式）..."
    echo "🔗 远程调试端口: 5678"
    echo "📋 在VS Code中连接: localhost:5678"
    echo "💡 提示: 在VS Code中按 F5 或使用调试面板连接"
    
    # 启动远程调试服务器
    python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client main_monitor_dynamic.py
    
elif [ -f "main_monitor_gui_app.py" ]; then
    echo "📱 启动GUI应用程序（远程调试模式）..."
    echo "🔗 远程调试端口: 5678"
    echo "📋 在VS Code中连接: localhost:5678"
    echo "💡 提示: 在VS Code中按 F5 或使用调试面板连接"
    
    # 启动远程调试服务器
    python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client main_monitor_gui_app.py
    
else
    echo "❌ 未找到可调试的Python文件"
    echo "请确保在开发环境中运行此脚本"
    echo "可用的调试文件:"
    ls -la *.py | grep -E "(main_monitor|gui)" || echo "  未找到main_monitor或gui相关文件"
    exit 1
fi 