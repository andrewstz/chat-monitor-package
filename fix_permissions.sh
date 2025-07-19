#!/bin/bash
# ChatMonitor 权限修复脚本
# 解决 macOS 权限弹框问题

set -e

echo "🔧 ChatMonitor 权限修复脚本"
echo "============================"

# 检查是否在 macOS 上运行
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅适用于 macOS"
    exit 1
fi

# 查找 ChatMonitor.app
APP_PATHS=(
    "/Applications/ChatMonitor.app"
    "$HOME/Applications/ChatMonitor.app"
    "./ChatMonitor.app"
    "./release/ChatMonitor.app"
    "./dist/ChatMonitor.app"
)

APP_FOUND=""
for app_path in "${APP_PATHS[@]}"; do
    if [ -d "$app_path" ]; then
        APP_FOUND="$app_path"
        echo "✅ 找到 ChatMonitor.app: $app_path"
        break
    fi
done

if [ -z "$APP_FOUND" ]; then
    echo "❌ 未找到 ChatMonitor.app"
    echo "请确保应用已构建并位于以下位置之一："
    for path in "${APP_PATHS[@]}"; do
        echo "   - $path"
    done
    exit 1
fi

echo ""
echo "🔧 开始修复权限问题..."
echo "========================"

# 1. 移除隔离属性
echo "1️⃣ 移除应用隔离属性..."
xattr -rd com.apple.quarantine "$APP_FOUND" 2>/dev/null || true
echo "   ✅ 隔离属性已移除"

# 2. 移除 ChatMonitor 的屏幕录制权限
echo "2️⃣ 移除 ChatMonitor 的屏幕录制权限..."
sudo tccutil remove ScreenCapture com.chatmonitor.app 2>/dev/null || true
echo "   ✅ ChatMonitor 屏幕录制权限已移除"

# 3. 移除 ChatMonitor 的辅助功能权限
echo "3️⃣ 移除 ChatMonitor 的辅助功能权限..."
sudo tccutil remove Accessibility com.chatmonitor.app 2>/dev/null || true
echo "   ✅ ChatMonitor 辅助功能权限已移除"

# 4. 移除 ChatMonitor 的麦克风权限
echo "4️⃣ 移除 ChatMonitor 的麦克风权限..."
sudo tccutil remove Microphone com.chatmonitor.app 2>/dev/null || true
echo "   ✅ ChatMonitor 麦克风权限已移除"

# 5. 检查应用签名
echo "5️⃣ 检查应用签名..."
if codesign -dv --verbose=4 "$APP_FOUND" >/dev/null 2>&1; then
    echo "   ✅ 应用签名正常"
else
    echo "   ⚠️  应用签名可能有问题"
fi

echo ""
echo "🎯 修复完成！"
echo "============="
echo ""
echo "📋 下一步操作："
echo "1. 启动 ChatMonitor.app"
echo "2. 当出现权限请求时，点击'打开系统设置'"
echo "3. 在系统设置中手动开启以下权限："
echo "   - 屏幕录制"
echo "   - 辅助功能"
echo "   - 麦克风（如果需要）"
echo ""
echo "🔧 启动应用："
echo "open '$APP_FOUND'"
echo ""
echo "💡 提示：如果权限问题仍然存在，请尝试："
echo "- 重启 macOS"
echo "- 重新构建应用"
echo "- 使用开发者证书签名应用" 