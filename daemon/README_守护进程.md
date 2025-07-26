# ChatMonitor 守护进程使用说明

## 概述

ChatMonitor 现在支持守护进程模式，可以自动监控程序状态并在崩溃时自动重启，同时提供系统声音和桌面通知功能。

## 功能特性

### 🔄 自动重启
- 监控主程序运行状态
- 检测到崩溃时自动重启
- 可配置重启次数限制和延迟时间
- 防止无限重启循环

### 🔊 系统声音通知
- **macOS**: 使用系统声音文件
- **Windows**: 使用系统蜂鸣声
- **Linux**: 使用 PulseAudio 或 ALSA

### 📱 桌面通知
- **macOS**: 使用系统通知中心
- **Windows**: 使用系统托盘通知
- **Linux**: 使用 notify-send

### 📊 详细日志
- 记录所有操作和状态变化
- 支持不同日志级别（INFO、WARN、ERROR）
- 日志文件位置：
  - macOS/Linux: `/tmp/chatmonitor_daemon.log`
  - Windows: `%TEMP%\chatmonitor_daemon.log`

## 使用方法

### 1. 守护进程监控器模式

启动专门的守护进程监控器，它会监控并自动重启主程序：

```bash
# macOS/Linux
python main_monitor_gui_app.py --daemon-monitor

# Windows
python main_monitor_gui_app.py --daemon-monitor
```

### 2. 守护进程模式

以守护进程模式运行主程序（隐藏窗口，只显示系统托盘）：

```bash
# macOS/Linux
python main_monitor_gui_app.py --daemon

# Windows
python main_monitor_gui_app.py --daemon
```

### 3. 使用启动脚本

#### macOS/Linux
```bash
# 启动守护进程
./start_chatmonitor.sh

# 测试功能
./start_chatmonitor.sh -t

# 清理进程
./start_chatmonitor.sh -c

# 查看帮助
./start_chatmonitor.sh -h
```

#### Windows
```cmd
# 启动守护进程
start_chatmonitor.bat

# 测试功能
start_chatmonitor.bat -t

# 清理进程
start_chatmonitor.bat -c

# 查看帮助
start_chatmonitor.bat -h
```

## 配置选项

### 守护进程配置

在 `daemon_monitor.py` 中可以修改以下配置：

```python
class ChatMonitorDaemon:
    def __init__(self):
        self.max_restarts = 5        # 最大重启次数
        self.restart_delay = 10      # 重启延迟（秒）
```

### 系统通知配置

在 `system_notification.py` 中可以自定义声音和通知：

```python
# 自定义声音文件路径
sound_files = {
    "default": "/System/Library/Sounds/Ping.aiff",
    "alert": "/System/Library/Sounds/Basso.aiff",
    "warning": "/System/Library/Sounds/Sosumi.aiff",
    "success": "/System/Library/Sounds/Glass.aiff"
}
```

## 系统托盘功能

在守护进程模式下，程序会显示系统托盘图标，提供以下功能：

- **显示主窗口**: 显示/隐藏主程序窗口
- **开始监控**: 手动启动监控
- **停止监控**: 手动停止监控
- **设置**: 打开设置窗口
- **退出**: 完全退出程序

## 日志监控

### 查看实时日志

```bash
# macOS/Linux
tail -f /tmp/chatmonitor_daemon.log

# Windows
type %TEMP%\chatmonitor_daemon.log
```

### 日志级别

- **INFO**: 一般信息（启动、停止、配置更新等）
- **WARN**: 警告信息（程序崩溃、重启等）
- **ERROR**: 错误信息（启动失败、依赖缺失等）
- **DEBUG**: 调试信息（详细的状态变化）

## 故障排除

### 1. 程序无法启动

检查依赖：
```bash
# 检查 Python 包
python -c "import psutil, pyautogui, cv2, pytesseract"

# 检查系统权限
# macOS: 系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制
# Windows: 确保有管理员权限
```

### 2. 声音不播放

```bash
# 测试系统声音
python system_notification.py

# macOS 测试
afplay /System/Library/Sounds/Ping.aiff

# Windows 测试
echo 
```

### 3. 通知不显示

```bash
# macOS 测试
osascript -e 'display notification "测试" with title "ChatMonitor"'

# Linux 测试
notify-send "ChatMonitor" "测试通知"

# Windows 测试
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('测试')"
```

### 4. 守护进程无法启动

检查日志文件：
```bash
# 查看启动日志
cat /tmp/chatmonitor_startup.log

# 查看守护进程日志
cat /tmp/chatmonitor_daemon.log
```

## 高级配置

### 自定义重启策略

修改 `daemon_monitor.py` 中的重启逻辑：

```python
def monitor_loop(self):
    # 自定义重启条件
    if not self.is_process_running():
        # 检查是否需要重启
        if self.should_restart():
            self.restart_program()
```

### 自定义通知策略

修改 `system_notification.py` 中的通知逻辑：

```python
def send_custom_notification(self, event_type, details):
    """发送自定义通知"""
    if event_type == "crash":
        self.send_desktop_notification("ChatMonitor", f"程序崩溃: {details}")
        self.play_system_sound("alert")
    elif event_type == "restart":
        self.send_desktop_notification("ChatMonitor", f"程序重启: {details}")
        self.play_system_sound("warning")
```

## 性能优化

### 1. 减少资源占用

```python
# 调整检查间隔
self.check_interval = 30  # 30秒检查一次

# 限制日志文件大小
if os.path.getsize(self.log_file) > 10 * 1024 * 1024:  # 10MB
    self.rotate_log_file()
```

### 2. 内存管理

```python
# 定期清理内存
import gc
gc.collect()

# 限制重启次数
if self.restart_count > 10:
    self.stop_monitoring()
```

## 安全考虑

### 1. 权限管理

- 确保程序有必要的系统权限
- 限制文件访问权限
- 使用安全的日志记录

### 2. 错误处理

- 捕获所有异常并记录
- 防止无限重启循环
- 提供优雅的退出机制

### 3. 资源清理

- 正确关闭所有子进程
- 清理临时文件
- 释放系统资源

## 常见问题

### Q: 守护进程和主程序有什么区别？

A: 
- **主程序**: 提供完整的 GUI 界面，用户可以直接操作
- **守护进程**: 在后台运行，监控主程序状态，提供自动重启功能

### Q: 如何停止守护进程？

A: 
```bash
# 方法1: 使用 Ctrl+C
# 方法2: 查找并杀死进程
ps aux | grep chatmonitor
kill <PID>

# 方法3: 使用清理脚本
./start_chatmonitor.sh -c
```

### Q: 守护进程会消耗多少资源？

A: 守护进程本身资源占用很少：
- CPU: < 1%
- 内存: < 10MB
- 磁盘: 只写日志文件

### Q: 如何自定义重启策略？

A: 修改 `daemon_monitor.py` 中的配置：
```python
self.max_restarts = 10        # 增加重启次数
self.restart_delay = 5        # 减少重启延迟
```

## 更新日志

### v1.0.0
- 初始版本
- 支持基本的自动重启功能
- 支持系统声音和桌面通知
- 支持跨平台（macOS、Windows、Linux）

### 计划功能
- 支持配置文件自定义
- 支持远程监控
- 支持集群部署
- 支持 Web 管理界面 