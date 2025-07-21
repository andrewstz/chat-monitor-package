#!/bin/bash
# 打包应用程序调试脚本

echo "🔧 ChatMonitor打包应用程序调试模式"

# 检查打包的应用程序是否存在
if [ ! -f "release/ChatMonitor.app/Contents/MacOS/ChatMonitor" ]; then
    echo "❌ 未找到打包的应用程序"
    echo "请先运行 ./build_macos_app.sh 构建应用程序"
    exit 1
fi

echo "📱 启动打包的应用程序（调试模式）..."
echo "🔍 调试方法："
echo "  1. 应用程序会输出详细日志"
echo "  2. 检查控制台输出"
echo "  3. 查看应用程序行为"
echo ""

# 设置调试环境变量
export CHATMONITOR_DEBUG=1
export CHATMONITOR_VERBOSE=1

# 启动应用程序并捕获输出
echo "🚀 启动应用程序..."
echo "================================"

# 直接运行可执行文件
./release/ChatMonitor.app/Contents/MacOS/ChatMonitor 2>&1 | tee chatmonitor_debug.log

echo ""
echo "📋 调试日志已保存到: chatmonitor_debug.log"
echo "💡 提示："
echo "  - 查看日志文件了解应用程序运行情况"
echo "  - 如果应用程序崩溃，检查日志中的错误信息"
echo "  - 可以修改配置文件后重新启动应用程序" 