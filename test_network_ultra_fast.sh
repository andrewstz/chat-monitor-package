#!/bin/bash

echo "⚡ 超快速网络监控验证脚本"
echo "================================"

# 备份原始配置
echo "📋 备份原始配置文件..."
cp ~/ChatMonitor/config_with_yolo.yaml ~/ChatMonitor/config_with_yolo.yaml.backup

# 复制超快速测试配置
echo "⚡ 应用超快速测试配置..."
cp config_network_test_ultra_fast.yaml ~/ChatMonitor/config_with_yolo.yaml

echo ""
echo "✅ 配置已更新为超快速验证模式："
echo "  - 检测间隔: 3秒"
echo "  - 超时时间: 2秒"
echo "  - 连续失败阈值: 1次"
echo "  - 容错时间: 0.1分钟 (6秒)"
echo ""

echo "🚀 超快速测试时间线："
echo "  - 启动后3秒开始第一次网络检测"
echo "  - 网络断开后6秒内触发警报"
echo "  - 网络恢复后6秒内恢复正常"
echo ""

echo "🔍 测试步骤："
echo "1. 启动应用程序"
echo "2. 等待约5-8秒让网络监控开始工作"
echo "3. 断开网络连接（关闭WiFi或拔网线）"
echo "4. 观察应用程序是否在6秒内检测到网络断开"
echo "5. 重新连接网络，观察是否在6秒内恢复正常"
echo ""

echo "📱 启动应用程序..."
echo "请手动启动 ChatMonitor.app 或运行以下命令："
echo "  open release/ChatMonitor.app"
echo ""

echo "⏰ 时间说明："
echo "  - 首次启动后约3秒开始网络检测"
echo "  - 网络断开后约6秒会触发警报"
echo "  - 网络恢复后约6秒内会恢复正常状态"
echo ""

echo "💡 小数分钟的优势："
echo "  - tolerance_minutes: 0.1 = 6秒"
echo "  - tolerance_minutes: 0.05 = 3秒"
echo "  - tolerance_minutes: 0.02 = 1.2秒"
echo "  - 比整数分钟更精确的时间控制"
echo ""

echo "🔄 恢复原始配置："
echo "测试完成后，运行以下命令恢复原始配置："
echo "  cp ~/ChatMonitor/config_with_yolo.yaml.backup ~/ChatMonitor/config_with_yolo.yaml"
echo ""

echo "🎯 更极端的测试配置："
echo "如果需要更快的响应，可以修改 tolerance_minutes 为："
echo "  - 0.05 (3秒)"
echo "  - 0.02 (1.2秒)"
echo "  - 0.01 (0.6秒)" 