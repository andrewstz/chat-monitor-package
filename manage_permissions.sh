#!/bin/bash
# ChatMonitor 精确权限管理脚本
# 只针对 ChatMonitor 进行权限操作，不影响其他应用

set -e

echo "🔧 ChatMonitor 精确权限管理脚本"
echo "================================"

# 检查是否在 macOS 上运行
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅适用于 macOS"
    exit 1
fi

# ChatMonitor 的 Bundle ID
BUNDLE_ID="com.chatmonitor.app"

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
    exit 1
fi

echo ""
echo "📋 当前 ChatMonitor 权限状态："
echo "=============================="

# 检查屏幕录制权限
echo "🔍 检查屏幕录制权限..."
if sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "SELECT client FROM access WHERE service='kTCCServiceScreenCapture' AND client='$BUNDLE_ID';" 2>/dev/null | grep -q "$BUNDLE_ID"; then
    echo "   ✅ 屏幕录制权限：已授权"
else
    echo "   ❌ 屏幕录制权限：未授权"
fi

# 检查辅助功能权限
echo "🔍 检查辅助功能权限..."
if sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "SELECT client FROM access WHERE service='kTCCServiceAccessibility' AND client='$BUNDLE_ID';" 2>/dev/null | grep -q "$BUNDLE_ID"; then
    echo "   ✅ 辅助功能权限：已授权"
else
    echo "   ❌ 辅助功能权限：未授权"
fi

# 检查麦克风权限
echo "🔍 检查麦克风权限..."
if sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "SELECT client FROM access WHERE service='kTCCServiceMicrophone' AND client='$BUNDLE_ID';" 2>/dev/null | grep -q "$BUNDLE_ID"; then
    echo "   ✅ 麦克风权限：已授权"
else
    echo "   ❌ 麦克风权限：未授权"
fi

echo ""
echo "🔧 权限管理选项："
echo "=================="
echo "1. 移除 ChatMonitor 的所有权限（重新授权）"
echo "2. 只移除屏幕录制权限"
echo "3. 只移除辅助功能权限"
echo "4. 只移除麦克风权限"
echo "5. 查看当前权限状态"
echo "6. 退出"
echo ""

read -p "请选择操作 (1-6): " choice

case $choice in
    1)
        echo "🗑️  移除 ChatMonitor 的所有权限..."
        sudo tccutil remove ScreenCapture "$BUNDLE_ID" 2>/dev/null || true
        sudo tccutil remove Accessibility "$BUNDLE_ID" 2>/dev/null || true
        sudo tccutil remove Microphone "$BUNDLE_ID" 2>/dev/null || true
        echo "✅ 所有权限已移除"
        ;;
    2)
        echo "🗑️  移除屏幕录制权限..."
        sudo tccutil remove ScreenCapture "$BUNDLE_ID" 2>/dev/null || true
        echo "✅ 屏幕录制权限已移除"
        ;;
    3)
        echo "🗑️  移除辅助功能权限..."
        sudo tccutil remove Accessibility "$BUNDLE_ID" 2>/dev/null || true
        echo "✅ 辅助功能权限已移除"
        ;;
    4)
        echo "🗑️  移除麦克风权限..."
        sudo tccutil remove Microphone "$BUNDLE_ID" 2>/dev/null || true
        echo "✅ 麦克风权限已移除"
        ;;
    5)
        echo "📋 当前权限状态已显示"
        ;;
    6)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🔓 移除应用隔离属性..."
xattr -rd com.apple.quarantine "$APP_FOUND" 2>/dev/null || true
echo "✅ 隔离属性已移除"

echo ""
echo "🎯 操作完成！"
echo "============="
echo ""
echo "📋 下一步操作："
echo "1. 启动 ChatMonitor.app"
echo "2. 当出现权限请求时，点击'打开系统设置'"
echo "3. 在系统设置中手动开启需要的权限"
echo ""
echo "🔧 启动应用："
echo "open '$APP_FOUND'" 