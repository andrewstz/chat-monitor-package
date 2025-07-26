#!/bin/bash
# ChatMonitor 应用启动脚本
# 自动启动带守护进程功能的应用

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 启动 ChatMonitor 应用...${NC}"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python3 未安装${NC}"
    exit 1
fi

# 检查主程序文件
if [[ ! -f "main_monitor_gui_app.py" ]]; then
    echo -e "${YELLOW}❌ 找不到主程序文件: main_monitor_gui_app.py${NC}"
    exit 1
fi

# 启动应用（自动启用守护进程）
echo -e "${GREEN}✅ 启动应用（已启用内部守护进程）${NC}"
python3 main_monitor_gui_app.py

# 如果GUI启动失败，使用守护进程启动器
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ GUI启动失败，使用守护进程启动器${NC}"
    python3 daemon_launcher.py
fi

echo -e "${GREEN}✅ 应用已退出${NC}" 