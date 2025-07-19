#!/bin/bash
# ChatMonitor 配置文件设置脚本
# 用于在 .app 包中管理配置文件

set -e

echo "🔧 ChatMonitor 配置文件设置脚本"
echo "================================"

# 检查是否在 macOS 上运行
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅适用于 macOS"
    exit 1
fi

# 用户配置目录
USER_CONFIG_DIR="$HOME/ChatMonitor"
USER_CONFIG_FILE="$USER_CONFIG_DIR/config_with_yolo.yaml"

echo "📁 用户配置目录: $USER_CONFIG_DIR"

# 创建用户配置目录
if [ ! -d "$USER_CONFIG_DIR" ]; then
    echo "📁 创建用户配置目录..."
    mkdir -p "$USER_CONFIG_DIR"
    echo "✅ 配置目录已创建: $USER_CONFIG_DIR"
fi

# 查找 ChatMonitor.app
APP_PATHS=(
    "/Applications/ChatMonitor.app"
    "$HOME/Applications/ChatMonitor.app"
    "./ChatMonitor.app"
    "./release/ChatMonitor.app"
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
    echo "⚠️  未找到 ChatMonitor.app，请确保应用已安装"
    echo "   可能的安装位置:"
    for path in "${APP_PATHS[@]}"; do
        echo "   - $path"
    done
    exit 1
fi

# 查找应用内的配置文件
APP_CONFIG_FILE="$APP_FOUND/Contents/Resources/config_with_yolo.yaml"

if [ ! -f "$APP_CONFIG_FILE" ]; then
    echo "❌ 未找到应用内的配置文件: $APP_CONFIG_FILE"
    exit 1
fi

echo "✅ 找到应用配置文件: $APP_CONFIG_FILE"

# 检查用户配置文件是否存在
if [ ! -f "$USER_CONFIG_FILE" ]; then
    echo "📋 复制默认配置文件到用户目录..."
    cp "$APP_CONFIG_FILE" "$USER_CONFIG_FILE"
    echo "✅ 配置文件已复制到: $USER_CONFIG_FILE"
    echo ""
    echo "📝 现在你可以编辑用户配置文件:"
    echo "   $USER_CONFIG_FILE"
    echo ""
    echo "🔧 编辑方法:"
    echo "   1. 使用文本编辑器: open -e $USER_CONFIG_FILE"
    echo "   2. 使用 VS Code: code $USER_CONFIG_FILE"
    echo "   3. 使用命令行: nano $USER_CONFIG_FILE"
else
    echo "✅ 用户配置文件已存在: $USER_CONFIG_FILE"
    echo ""
    echo "📝 当前配置文件内容预览:"
    echo "================================"
    head -20 "$USER_CONFIG_FILE"
    echo "================================"
fi

echo ""
echo "🚀 配置说明:"
echo "============"
echo "1. 应用会优先使用用户目录的配置文件: $USER_CONFIG_FILE"
echo "2. 修改配置文件后，应用会自动检测并热更新"
echo "3. 支持热更新的配置项:"
echo "   - chat_app.target_contacts: 目标联系人列表"
echo "   - chat_app.fuzzy_match: 模糊匹配参数"
echo "   - monitor_settings: 监控设置"
echo "   - alert_settings: 警报设置"
echo ""
echo "📋 常用配置项:"
echo "=============="
echo "- target_contacts: 要监控的联系人名称列表"
echo "- similarity_threshold: 模糊匹配阈值 (0.0-1.0)"
echo "- check_interval: 检测间隔 (秒)"
echo "- sound_enabled: 是否启用声音警报"
echo ""
echo "🔧 快速编辑命令:"
echo "================"
echo "open -e $USER_CONFIG_FILE  # 使用文本编辑器"
echo "code $USER_CONFIG_FILE     # 使用 VS Code"
echo "nano $USER_CONFIG_FILE     # 使用 nano"
echo ""
echo "✅ 设置完成！现在可以启动 ChatMonitor.app 了" 