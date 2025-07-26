# ChatMonitor 自动启动守护进程

## 概述

现在 ChatMonitor 支持自动启动守护进程功能，无需手动启动脚本。应用启动时会自动启用守护进程，确保程序崩溃时能够自动重启。

## 功能特性

### 🛡️ 自动守护进程
- **自动启动**: 应用启动时自动启用内部守护进程
- **自动重启**: 程序崩溃时自动重启（最多5次，1小时冷却期）
- **系统通知**: 崩溃和重启时播放系统声音和桌面通知
- **日志记录**: 详细记录守护进程的运行状态

### 🔧 多种启动方式
1. **普通启动**: 带GUI界面，自动启用守护进程
2. **守护进程模式**: 隐藏GUI，只显示系统托盘图标
3. **独立守护进程**: 不依赖GUI，纯后台运行

## 使用方法

### 方式一：普通启动（推荐）
```bash
# 启动应用，自动启用守护进程
python3 main_monitor_gui_app.py

# 或者使用启动脚本
./start_app.sh
```

### 方式二：守护进程模式
```bash
# 隐藏GUI，只显示系统托盘图标
python3 main_monitor_gui_app.py --daemon
```

### 方式三：独立守护进程
```bash
# 直接启动守护进程，不依赖GUI
python3 daemon_launcher.py

# 或者使用启动脚本
./start_daemon.sh
```

### 方式四：禁用守护进程
```bash
# 禁用守护进程功能
python3 main_monitor_gui_app.py --no-daemon
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--daemon` | 以守护进程模式运行（隐藏GUI，显示系统托盘） |
| `--daemon-monitor` | 启动独立的守护进程监控器 |
| `--no-daemon` | 禁用守护进程功能 |

## 守护进程功能

### 自动重启机制
- **最大重启次数**: 5次
- **重启延迟**: 10秒
- **冷却期**: 1小时内达到最大重启次数后，等待1小时再重试
- **监控间隔**: 每5秒检查一次进程状态

### 系统通知
- **启动通知**: 守护进程启动时播放成功声音和通知
- **崩溃通知**: 检测到程序崩溃时播放警告声音和通知
- **重启通知**: 每次重启时显示重启进度
- **停止通知**: 守护进程停止时播放成功声音和通知

### 日志记录
- **日志文件**: `/tmp/chatmonitor_daemon.log` (macOS/Linux)
- **日志级别**: INFO, WARN, ERROR, DEBUG
- **日志内容**: 启动、监控、重启、错误等详细信息

## 系统托盘功能（守护进程模式）

当使用 `--daemon` 参数启动时，应用会隐藏主窗口并显示系统托盘图标：

### 托盘菜单
- **显示窗口**: 显示主程序窗口
- **隐藏窗口**: 隐藏主程序窗口
- **开始监控**: 启动弹框监控
- **停止监控**: 停止弹框监控
- **设置**: 打开设置窗口
- **退出**: 完全退出程序

### 托盘图标
- 正常状态: 绿色图标
- 监控中: 蓝色图标
- 错误状态: 红色图标

## 故障排除

### 常见问题

#### 1. tkinter 模块错误
```
ModuleNotFoundError: No module named '_tkinter'
```

**解决方案**:
- 使用独立守护进程: `python3 daemon_launcher.py`
- 或者安装tkinter: `brew install python-tk`

#### 2. psutil 模块错误
```
ModuleNotFoundError: No module named 'psutil'
```

**解决方案**:
```bash
pip3 install psutil --break-system-packages
```

#### 3. 守护进程无法启动主程序
**检查项目**:
- 确保 `main_monitor_gui_app.py` 文件存在
- 检查Python环境是否正确
- 查看日志文件: `cat /tmp/chatmonitor_daemon.log`

#### 4. 系统通知不工作
**检查项目**:
- macOS: 确保通知权限已开启
- Windows: 确保通知设置已启用
- Linux: 确保 `notify-send` 已安装

### 日志查看

```bash
# 查看守护进程日志
cat /tmp/chatmonitor_daemon.log

# 实时查看日志
tail -f /tmp/chatmonitor_daemon.log

# 查看应用启动日志
cat /tmp/chatmonitor_start.log
```

### 进程管理

```bash
# 查看守护进程
ps aux | grep daemon_launcher

# 查看主程序进程
ps aux | grep main_monitor_gui_app

# 停止守护进程
pkill -f daemon_launcher.py

# 停止所有相关进程
pkill -f chatmonitor
```

## 高级配置

### 修改守护进程参数

编辑 `daemon_launcher.py` 中的参数：

```python
class DaemonLauncher:
    def __init__(self):
        self.max_restarts = 5        # 最大重启次数
        self.restart_delay = 10      # 重启延迟（秒）
        # ...
```

### 自定义日志路径

```python
def _get_log_path(self):
    """获取日志文件路径"""
    if self.platform == "darwin":  # macOS
        return "/tmp/chatmonitor_daemon.log"
    elif self.platform == "windows":
        return os.path.join(os.getenv('TEMP', ''), "chatmonitor_daemon.log")
    else:  # Linux
        return "/tmp/chatmonitor_daemon.log"
```

## 打包应用

### macOS 打包
```bash
# 使用 PyInstaller 打包
pyinstaller --onefile --windowed --icon=assets/icons/icon.icns main_monitor_gui_app.py

# 打包后的应用会自动包含守护进程功能
```

### Windows 打包
```bash
# 使用 PyInstaller 打包
pyinstaller --onefile --windowed --icon=assets/icons/icon.ico main_monitor_gui_app.py

# 打包后的应用会自动包含守护进程功能
```

## 总结

现在 ChatMonitor 具有完整的自动守护进程功能：

1. **自动启动**: 应用启动时自动启用守护进程
2. **自动重启**: 程序崩溃时自动重启
3. **系统通知**: 崩溃和重启时通知用户
4. **多种模式**: 支持GUI模式、守护进程模式、独立守护进程
5. **完整日志**: 详细记录所有操作和状态

用户只需要正常启动应用，守护进程就会自动工作，无需额外的手动操作。 