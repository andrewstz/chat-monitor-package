#!/bin/bash
# 启动打包后的应用程序并启用远程调试

echo "🚀 启动打包后的ChatMonitor应用程序（带远程调试）"

# 设置环境变量启用远程调试
export PYTHONPATH="/Users/andrewstz/Documents/study/promgramLang/python/work/chat_monitor_ai/yolov5-popup-detector/doPackage"
export CHATMONITOR_DEBUG=1

# 启动应用程序
echo "📱 启动应用程序..."
open release/ChatMonitor.app

echo "✅ 应用程序已启动"
echo "🔗 现在可以在Cursor中连接远程调试到 localhost:5678"
echo "💡 在Cursor中："
echo "   1. 打开调试面板 (Cmd+Shift+D)"
echo "   2. 选择 'Attach to Python Process'"
echo "   3. 点击绿色播放按钮开始调试" 