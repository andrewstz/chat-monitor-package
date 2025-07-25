#!/bin/bash
# ChatMonitor 启动脚本
# 包含自动重启和系统通知功能

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "INFO")
            echo -e "${GREEN}[${timestamp}] INFO: ${message}${NC}"
            ;;
        "WARN")
            echo -e "${YELLOW}[${timestamp}] WARN: ${message}${NC}"
            ;;
        "ERROR")
            echo -e "${RED}[${timestamp}] ERROR: ${message}${NC}"
            ;;
        "DEBUG")
            echo -e "${BLUE}[${timestamp}] DEBUG: ${message}${NC}"
            ;;
    esac
    
    # 写入日志文件
    echo "[${timestamp}] ${level}: ${message}" >> /tmp/chatmonitor_startup.log
}

# 播放系统声音
play_system_sound() {
    local sound_type=$1
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        case $sound_type in
            "alert")
                afplay /System/Library/Sounds/Basso.aiff
                ;;
            "success")
                afplay /System/Library/Sounds/Glass.aiff
                ;;
            "warning")
                afplay /System/Library/Sounds/Sosumi.aiff
                ;;
            *)
                afplay /System/Library/Sounds/Ping.aiff
                ;;
        esac
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || \
        aplay /usr/share/sounds/alsa/Front_Center.wav 2>/dev/null || \
        echo "无法播放系统声音"
    fi
}

# 发送桌面通知
send_notification() {
    local title=$1
    local message=$2
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "display notification \"${message}\" with title \"${title}\""
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        notify-send "${title}" "${message}" 2>/dev/null || echo "无法发送桌面通知"
    fi
}

# 检查依赖
check_dependencies() {
    log_message "INFO" "检查系统依赖..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_message "ERROR" "Python3 未安装"
        return 1
    fi
    
    # 检查必要的 Python 包
    local required_packages=("psutil" "pyautogui" "opencv-python" "pytesseract")
    for package in "${required_packages[@]}"; do
        if ! python3 -c "import ${package}" 2>/dev/null; then
            log_message "WARN" "缺少 Python 包: ${package}"
        fi
    done
    
    log_message "INFO" "依赖检查完成"
    return 0
}

# 启动主程序
start_main_program() {
    log_message "INFO" "启动 ChatMonitor 主程序..."
    
    # 检查主程序文件是否存在
    if [[ ! -f "main_monitor_gui_app.py" ]]; then
        log_message "ERROR" "找不到主程序文件: main_monitor_gui_app.py"
        return 1
    fi
    
    # 启动程序
    python3 main_monitor_gui_app.py &
    local pid=$!
    
    log_message "INFO" "主程序已启动 (PID: ${pid})"
    echo $pid > /tmp/chatmonitor.pid
    
    # 等待一段时间检查进程是否正常启动
    sleep 3
    if kill -0 $pid 2>/dev/null; then
        log_message "INFO" "主程序启动成功"
        play_system_sound "success"
        send_notification "ChatMonitor" "程序启动成功"
        return 0
    else
        log_message "ERROR" "主程序启动失败"
        play_system_sound "alert"
        send_notification "ChatMonitor" "程序启动失败"
        return 1
    fi
}

# 监控程序状态
monitor_program() {
    local max_restarts=5
    local restart_count=0
    local restart_delay=10
    
    log_message "INFO" "开始监控程序状态..."
    log_message "INFO" "最大重启次数: ${max_restarts}"
    log_message "INFO" "重启延迟: ${restart_delay}秒"
    
    while true; do
        # 检查 PID 文件
        if [[ -f "/tmp/chatmonitor.pid" ]]; then
            local pid=$(cat /tmp/chatmonitor.pid)
            
            # 检查进程是否还在运行
            if kill -0 $pid 2>/dev/null; then
                if [[ $restart_count -gt 0 ]]; then
                    log_message "INFO" "程序运行正常，重置重启计数"
                    restart_count=0
                fi
            else
                log_message "WARN" "检测到程序崩溃 (PID: ${pid})"
                
                # 检查重启限制
                if [[ $restart_count -ge $max_restarts ]]; then
                    log_message "ERROR" "已达到最大重启次数 (${max_restarts})，停止监控"
                    play_system_sound "alert"
                    send_notification "ChatMonitor" "程序崩溃次数过多，已停止自动重启"
                    break
                fi
                
                # 执行重启
                restart_count=$((restart_count + 1))
                log_message "INFO" "开始第 ${restart_count} 次重启..."
                
                play_system_sound "warning"
                send_notification "ChatMonitor" "程序崩溃，正在重启 (${restart_count}/${max_restarts})"
                
                # 等待重启延迟
                sleep $restart_delay
                
                # 启动新进程
                if start_main_program; then
                    log_message "INFO" "重启成功"
                else
                    log_message "ERROR" "重启失败"
                fi
            fi
        else
            log_message "WARN" "找不到 PID 文件，重新启动程序"
            start_main_program
        fi
        
        # 等待一段时间再检查
        sleep 5
    done
}

# 清理函数
cleanup() {
    log_message "INFO" "正在清理..."
    
    # 删除 PID 文件
    rm -f /tmp/chatmonitor.pid
    
    # 停止所有相关进程
    pkill -f "main_monitor_gui_app.py" 2>/dev/null
    
    log_message "INFO" "清理完成"
}

# 主函数
main() {
    log_message "INFO" "ChatMonitor 启动脚本开始执行"
    log_message "INFO" "当前目录: $(pwd)"
    log_message "INFO" "操作系统: $(uname -s)"
    
    # 设置信号处理
    trap cleanup EXIT
    trap 'log_message "INFO" "收到中断信号，正在退出..."; exit 0' INT TERM
    
    # 检查依赖
    if ! check_dependencies; then
        log_message "ERROR" "依赖检查失败，退出"
        exit 1
    fi
    
    # 播放启动声音
    play_system_sound "success"
    send_notification "ChatMonitor" "启动脚本已加载"
    
    # 启动主程序
    if start_main_program; then
        # 开始监控
        monitor_program
    else
        log_message "ERROR" "主程序启动失败，退出"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "ChatMonitor 启动脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -t, --test     测试系统声音和通知"
    echo "  -c, --clean    清理残留进程"
    echo ""
    echo "功能:"
    echo "  - 自动启动 ChatMonitor 主程序"
    echo "  - 监控程序状态，崩溃时自动重启"
    echo "  - 播放系统声音和发送桌面通知"
    echo "  - 记录详细日志到 /tmp/chatmonitor_startup.log"
}

# 测试功能
test_features() {
    echo "🧪 测试系统功能..."
    
    echo "🔊 测试系统声音..."
    play_system_sound "success"
    sleep 1
    play_system_sound "warning"
    sleep 1
    play_system_sound "alert"
    
    echo "📱 测试桌面通知..."
    send_notification "ChatMonitor 测试" "这是一条测试通知"
    
    echo "✅ 测试完成"
}

# 清理功能
cleanup_only() {
    echo "🧹 清理残留进程..."
    cleanup
    echo "✅ 清理完成"
}

# 解析命令行参数
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -t|--test)
        test_features
        exit 0
        ;;
    -c|--clean)
        cleanup_only
        exit 0
        ;;
    "")
        main
        ;;
    *)
        echo "错误: 未知选项 $1"
        show_help
        exit 1
        ;;
esac 