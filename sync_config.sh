#!/bin/bash

echo "🔄 同步配置文件"
echo "📁 当前目录: $(pwd)"

# 检查用户目录是否存在
user_config_dir="$HOME/ChatMonitor"
user_config_file="$user_config_dir/config_with_yolo.yaml"

# 检查应用程序内的配置文件
app_config_file="release/ChatMonitor.app/Contents/Resources/config_with_yolo.yaml"

echo "🔍 检查配置文件..."

# 如果用户目录不存在，创建它
if [ ! -d "$user_config_dir" ]; then
    echo "📁 创建用户配置目录: $user_config_dir"
    mkdir -p "$user_config_dir"
fi

# 如果用户配置文件不存在，从应用程序复制
if [ ! -f "$user_config_file" ]; then
    echo "📋 复制默认配置文件到用户目录..."
    cp "$app_config_file" "$user_config_file"
    echo "✅ 配置文件已复制到: $user_config_file"
else
    echo "✅ 用户配置文件已存在: $user_config_file"
fi

# 显示两个配置文件的内容差异
echo ""
echo "📊 配置文件对比:"
echo "用户目录配置 ($user_config_file):"
echo "  target_contacts: $(grep -A 1 "target_contacts:" "$user_config_file" | tail -1 | sed 's/^[[:space:]]*//')"

echo ""
echo "应用程序内配置 ($app_config_file):"
echo "  target_contacts: $(grep -A 1 "target_contacts:" "$app_config_file" | tail -1 | sed 's/^[[:space:]]*//')"

echo ""
echo "💡 提示:"
echo "  - 应用程序优先读取用户目录的配置文件"
echo "  - 修改 $user_config_file 可以实时生效"
echo "  - 如果需要重置配置，可以删除用户目录的配置文件"

# 显示如何编辑配置文件
echo ""
echo "📝 编辑配置文件的方法:"
echo "  方法1: 直接编辑用户配置文件"
echo "    open $user_config_file"
echo ""
echo "  方法2: 使用文本编辑器"
echo "    code $user_config_file"
echo ""
echo "  方法3: 使用命令行编辑器"
echo "    nano $user_config_file"
echo "    或"
echo "    vim $user_config_file" 