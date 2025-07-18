#!/bin/bash
# 动态监控启动脚本（精简版）
# 支持配置文件热更新

echo "🚀 启动动态监控系统（精简版）..."
echo "📁 工作目录: $(pwd)"
echo "⚙️  配置文件: config_with_yolo.yaml"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖
if [ ! -f "requirements_clean.txt" ]; then
    echo "❌ 未找到依赖文件 requirements_clean.txt"
    exit 1
fi

# 安装依赖（如果需要）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "🔧 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装依赖..."
pip install -r requirements_clean.txt

echo "🎯 启动主程序..."
python3 main_monitor_dynamic.py

echo "👋 程序已退出"
