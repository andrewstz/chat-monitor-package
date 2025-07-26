#!/bin/bash
# ChatMonitor 守护进程启动脚本
# 直接启动守护进程，不依赖GUI

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 启动 ChatMonitor 守护进程...${NC}"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

# 检查守护进程启动器
if [[ ! -f "daemon_launcher.py" ]]; then
    echo -e "${RED}❌ 找不到守护进程启动器: daemon_launcher.py${NC}"
    exit 1
fi

# 检查依赖
echo -e "${GREEN}📋 检查依赖...${NC}"
python3 -c "import psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ 缺少依赖: psutil${NC}"
    echo -e "${GREEN}📦 正在安装依赖...${NC}"
    pip3 install psutil --break-system-packages
fi

# 启动守护进程
echo -e "${GREEN}✅ 启动守护进程...${NC}"
python3 daemon_launcher.py

echo -e "${GREEN}✅ 守护进程已退出${NC}" 