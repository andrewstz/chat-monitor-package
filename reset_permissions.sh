#!/bin/bash
# 重置ChatMonitor的macOS权限

echo "🔓 重置ChatMonitor的macOS权限..."

# 检查是否以管理员权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    echo "使用方法: sudo ./reset_permissions.sh"
    exit 1
fi

BUNDLE_ID="com.chatmonitor.app"

echo "📱 重置应用程序: $BUNDLE_ID"

# 重置屏幕录制权限
echo "🖥️  重置屏幕录制权限..."
tccutil reset ScreenCapture "$BUNDLE_ID"

# 重置辅助功能权限
echo "♿ 重置辅助功能权限..."
tccutil reset Accessibility "$BUNDLE_ID"

# 重置麦克风权限
echo "🎤 重置麦克风权限..."
tccutil reset Microphone "$BUNDLE_ID"

# 重置系统管理权限
echo "⚙️  重置系统管理权限..."
tccutil reset SystemAdministration "$BUNDLE_ID"

# 重置Apple事件权限
echo "🍎 重置Apple事件权限..."
tccutil reset AppleEvents "$BUNDLE_ID"

echo "✅ 权限重置完成！"
echo ""
echo "📋 接下来需要手动授权："
echo "1. 打开 系统偏好设置 > 安全性与隐私"
echo "2. 在 隐私 标签页中，为以下项目添加ChatMonitor："
echo "   - 屏幕录制"
echo "   - 辅助功能"
echo "   - 麦克风"
echo "3. 重启ChatMonitor应用程序" 