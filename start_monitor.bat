@echo off
REM 动态监控启动脚本 (Windows) - 精简版
REM 支持配置文件热更新

echo 🚀 启动动态监控系统（精简版）...
echo 📁 工作目录: %cd%
echo ⚙️  配置文件: config_with_yolo.yaml

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖文件
if not exist "requirements_clean.txt" (
    echo ❌ 未找到依赖文件 requirements_clean.txt
    pause
    exit /b 1
)

REM 创建虚拟环境（如果需要）
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

echo 📦 安装依赖...
pip install -r requirements_clean.txt

echo 🎯 启动主程序...
python main_monitor_dynamic.py

echo 👋 程序已退出
pause
