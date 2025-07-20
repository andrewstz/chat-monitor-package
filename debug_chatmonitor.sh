#!/bin/bash
# ChatMonitor调试启动脚本

echo "🔧 ChatMonitor调试模式启动"

# 设置调试环境变量
export CHATMONITOR_DEBUG=1

# 检查是否在打包环境中
if [ -f "release/ChatMonitor.app/Contents/MacOS/ChatMonitor" ]; then
    echo "📱 启动打包后的应用程序（调试模式）..."
    cd release/ChatMonitor.app/Contents/MacOS
    ./ChatMonitor
elif [ -f "dist/ChatMonitor/ChatMonitor" ]; then
    echo "📱 启动dist目录的应用程序（调试模式）..."
    cd dist/ChatMonitor
    ./ChatMonitor
else
    echo "❌ 未找到ChatMonitor可执行文件"
    echo "请先运行 ./build_macos_app.sh 构建应用程序"
    exit 1
fi 