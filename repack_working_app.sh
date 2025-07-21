#!/bin/bash

echo "🔄 重新打包正常工作的应用程序"
echo "📁 当前目录: $(pwd)"

# 检查原始应用程序是否存在
if [ ! -d "release/ChatMonitor.app" ]; then
    echo "❌ 原始应用程序不存在: release/ChatMonitor.app"
    exit 1
fi

echo "✅ 找到原始应用程序: release/ChatMonitor.app"

# 创建新的 DMG 安装包
echo "📦 创建新的 DMG 安装包..."
dmg_name="ChatMonitor-macOS-working-v1.0.0.dmg"
dmg_path="release/$dmg_name"

# 确保 release 目录存在
mkdir -p release

# 使用更安全的 DMG 创建方法
echo "🔧 使用安全的 DMG 创建方法..."

# 先创建一个临时目录
temp_dmg_dir="/tmp/ChatMonitor_working_dmg_temp"
rm -rf "$temp_dmg_dir"
mkdir -p "$temp_dmg_dir"

# 复制应用程序到临时目录（使用 cp -R 保持所有属性）
echo "📋 复制应用程序到临时目录..."
cp -R "release/ChatMonitor.app" "$temp_dmg_dir/"

# 确保所有文件都有正确的权限
echo "🔧 修复文件权限..."
find "$temp_dmg_dir" -name "*.dylib" -exec chmod 755 {} \;
find "$temp_dmg_dir" -name "*.so" -exec chmod 755 {} \;
find "$temp_dmg_dir" -name "*.app" -exec chmod 755 {} \;

# 移除应用隔离属性
echo "🔓 移除应用隔离属性..."
xattr -cr "$temp_dmg_dir/ChatMonitor.app" 2>/dev/null || true

# 创建 DMG
echo "📦 创建 DMG..."
hdiutil create -volname "ChatMonitor" -srcfolder "$temp_dmg_dir" -ov -format UDZO "$dmg_path"

# 清理临时目录
rm -rf "$temp_dmg_dir"

if [ $? -eq 0 ]; then
    dmg_size=$(du -sh "$dmg_path" | cut -f1)
    echo "✅ DMG创建成功: $dmg_path"
    echo "📦 DMG大小: $dmg_size"
else
    echo "❌ DMG创建失败"
    exit 1
fi

echo ""
echo "🎉 重新打包完成！"
echo "📦 新的安装包: $dmg_path"
echo ""
echo "🚀 使用方法:"
echo "  1. 双击 $dmg_name 挂载DMG"
echo "  2. 将 ChatMonitor.app 拖拽到应用程序文件夹"
echo "  3. 从启动台或应用程序文件夹启动"
echo ""
echo "⚠️  注意: 这个版本基于已知正常工作的应用程序"
echo "🔧 修复内容:"
echo "  - 使用已知正常工作的应用程序"
echo "  - 修复文件权限问题"
echo "  - 使用更安全的 DMG 创建方法"
echo "  - 确保符号链接正确" 