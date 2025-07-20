#!/bin/bash
# ChatMonitor远程调试启动脚本

echo "🔧 ChatMonitor远程调试模式启动"

# 设置远程调试环境变量
export CHATMONITOR_REMOTE_DEBUG=1
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 检查是否在打包环境中
if [ -f "release/ChatMonitor.app/Contents/MacOS/ChatMonitor" ]; then
    echo "📱 启动打包后的应用程序（远程调试模式）..."
    echo "🔗 远程调试端口: 5678"
    echo "📋 在VS Code中连接: localhost:5678"
    cd release/ChatMonitor.app/Contents/MacOS
    python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client ./ChatMonitor
elif [ -f "dist/ChatMonitor/ChatMonitor" ]; then
    echo "📱 启动dist目录的应用程序（远程调试模式）..."
    echo "🔗 远程调试端口: 5678"
    echo "📋 在VS Code中连接: localhost:5678"
    cd dist/ChatMonitor
    python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client ./ChatMonitor
else
    echo "❌ 未找到ChatMonitor可执行文件"
    echo "请先运行 ./build_macos_app.sh 构建应用程序"
    exit 1
fi 