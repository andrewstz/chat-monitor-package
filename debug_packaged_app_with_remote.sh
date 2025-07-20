#!/bin/bash
# 启动打包后的应用程序并启用远程调试

echo "🚀 启动打包后的ChatMonitor应用程序（带远程调试）"

# 检查应用程序是否存在
if [ ! -d "release/ChatMonitor.app" ]; then
    echo "❌ 未找到 release/ChatMonitor.app"
    echo "请先运行 ./build_macos_app.sh 构建应用程序"
    exit 1
fi

# 设置环境变量启用远程调试
export PYTHONPATH="/Users/andrewstz/Documents/study/promgramLang/python/work/chat_monitor_ai/yolov5-popup-detector/doPackage"
export CHATMONITOR_DEBUG=1
export CHATMONITOR_REMOTE_DEBUG=1

echo "🔧 修改应用程序以支持远程调试..."

# 备份原始可执行文件
cp "release/ChatMonitor.app/Contents/MacOS/ChatMonitor" "release/ChatMonitor.app/Contents/MacOS/ChatMonitor.backup"

# 创建一个启动脚本，在应用程序启动前启动debugpy
cat > "release/ChatMonitor.app/Contents/MacOS/ChatMonitor_debug" << 'EOF'
#!/bin/bash
# 启动debugpy服务器
cd "/Users/andrewstz/Documents/study/promgramLang/python/work/chat_monitor_ai/yolov5-popup-detector/doPackage"
source /Users/andrewstz/miniconda3/etc/profile.d/conda.sh
conda activate paddle
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main_monitor_gui_app.py &
DEBUG_PID=$!

# 等待debugpy启动
sleep 2

# 启动原始应用程序
exec "$0.backup" "$@"
EOF

chmod +x "release/ChatMonitor.app/Contents/MacOS/ChatMonitor_debug"

# 启动应用程序
echo "📱 启动应用程序..."
open release/ChatMonitor.app

echo "✅ 应用程序已启动"
echo "🔗 现在可以在Cursor中连接远程调试到 localhost:5678"
echo "💡 在Cursor中："
echo "   1. 打开调试面板 (Cmd+Shift+D)"
echo "   2. 选择 'Attach to Python Process'"
echo "   3. 点击绿色播放按钮开始调试" 







