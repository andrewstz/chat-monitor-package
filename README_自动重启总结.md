# ChatMonitor 自动重启功能总结

## 🎯 功能概述

ChatMonitor 现在具备了完整的自动重启和系统通知功能，确保程序在崩溃时能够自动恢复，并通过声音和桌面通知及时提醒用户。

## 📁 新增文件

### 1. 核心模块
- **`daemon_monitor.py`** - 守护进程模块，可集成到打包应用中
- **`system_notification.py`** - 跨平台系统通知模块
- **`auto_restart_monitor.py`** - 独立的自动重启监控器

### 2. 启动脚本
- **`start_chatmonitor.sh`** - macOS/Linux 启动脚本
- **`start_chatmonitor.bat`** - Windows 启动脚本

### 3. 文档和测试
- **`README_守护进程.md`** - 详细使用说明
- **`test_daemon.py`** - 功能测试脚本

## 🔧 功能特性

### ✅ 已实现功能

#### 1. 自动重启机制
- **进程监控**: 实时监控主程序运行状态
- **崩溃检测**: 自动检测程序崩溃
- **智能重启**: 可配置重启次数和延迟时间
- **防循环**: 防止无限重启循环

#### 2. 系统声音通知
- **macOS**: 使用系统声音文件 (`afplay`)
- **Windows**: 使用系统蜂鸣声 (`winsound`)
- **Linux**: 使用 PulseAudio 或 ALSA

#### 3. 桌面通知
- **macOS**: 系统通知中心 (`osascript`)
- **Windows**: 系统托盘通知 (PowerShell)
- **Linux**: notify-send

#### 4. 详细日志记录
- 支持不同日志级别 (INFO, WARN, ERROR, DEBUG)
- 跨平台日志文件路径
- 实时日志监控

#### 5. 命令行支持
```bash
# 守护进程监控器模式
python3 main_monitor_gui_app.py --daemon-monitor

# 守护进程模式（隐藏窗口）
python3 main_monitor_gui_app.py --daemon

# 普通模式
python3 main_monitor_gui_app.py
```

## 🚀 使用方法

### 方法1: 使用启动脚本（推荐）

#### macOS/Linux
```bash
# 启动守护进程
./start_chatmonitor.sh

# 测试功能
./start_chatmonitor.sh -t

# 清理进程
./start_chatmonitor.sh -c
```

#### Windows
```cmd
# 启动守护进程
start_chatmonitor.bat

# 测试功能
start_chatmonitor.bat -t

# 清理进程
start_chatmonitor.bat -c
```

### 方法2: 直接使用Python

```bash
# 启动守护进程监控器
python3 main_monitor_gui_app.py --daemon-monitor

# 以守护进程模式运行
python3 main_monitor_gui_app.py --daemon
```

## 📊 测试结果

### ✅ 测试通过的功能

1. **系统通知功能**
   - ✅ 声音播放 (macOS)
   - ✅ 桌面通知 (macOS)
   - ✅ 跨平台兼容

2. **自动重启功能**
   - ✅ 进程检查
   - ✅ 日志记录
   - ✅ 系统声音

3. **守护进程功能**
   - ✅ 文件完整性检查
   - ✅ 模块导入测试
   - ✅ 基础功能验证

## 🔧 配置选项

### 守护进程配置 (`daemon_monitor.py`)
```python
class ChatMonitorDaemon:
    def __init__(self):
        self.max_restarts = 5        # 最大重启次数
        self.restart_delay = 10      # 重启延迟（秒）
```

### 系统通知配置 (`system_notification.py`)
```python
# macOS 声音文件
sound_files = {
    "default": "/System/Library/Sounds/Ping.aiff",
    "alert": "/System/Library/Sounds/Basso.aiff",
    "warning": "/System/Library/Sounds/Sosumi.aiff",
    "success": "/System/Library/Sounds/Glass.aiff"
}
```

## 📝 日志文件

### 日志文件位置
- **macOS/Linux**: `/tmp/chatmonitor_*.log`
- **Windows**: `%TEMP%\chatmonitor_*.log`

### 日志类型
- `chatmonitor_daemon.log` - 守护进程日志
- `chatmonitor_notification.log` - 通知日志
- `chatmonitor_startup.log` - 启动脚本日志
- `chatmonitor_debug.log` - 调试日志

## 🔍 故障排除

### 常见问题

1. **依赖缺失**
   ```bash
   pip3 install psutil --break-system-packages
   ```

2. **权限问题**
   - macOS: 系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制
   - Windows: 以管理员身份运行

3. **声音不播放**
   ```bash
   # 测试系统声音
   python3 system_notification.py
   ```

4. **通知不显示**
   ```bash
   # macOS 测试
   osascript -e 'display notification "测试" with title "ChatMonitor"'
   ```

## 🎯 使用场景

### 1. 生产环境部署
- 使用守护进程监控器确保程序稳定运行
- 自动处理程序崩溃和重启
- 通过系统通知及时了解程序状态

### 2. 开发环境调试
- 使用普通模式进行开发和调试
- 通过详细日志了解程序运行状态
- 快速定位和解决问题

### 3. 用户日常使用
- 使用守护进程模式隐藏窗口
- 通过系统托盘快速访问功能
- 自动处理程序异常

## 🔮 未来扩展

### 计划功能
1. **配置文件支持**
   - 自定义重启策略
   - 自定义通知设置
   - 自定义日志级别

2. **远程监控**
   - Web 管理界面
   - 远程状态查看
   - 远程控制功能

3. **集群部署**
   - 多实例监控
   - 负载均衡
   - 故障转移

4. **高级功能**
   - 性能监控
   - 资源使用统计
   - 自动更新

## 📋 文件清单

```
doPackage/
├── 核心模块
│   ├── daemon_monitor.py          # 守护进程模块
│   ├── system_notification.py     # 系统通知模块
│   ├── auto_restart_monitor.py    # 自动重启监控器
│   └── main_monitor_gui_app.py    # 主程序（已更新）
├── 启动脚本
│   ├── start_chatmonitor.sh       # macOS/Linux 启动脚本
│   └── start_chatmonitor.bat      # Windows 启动脚本
├── 文档
│   ├── README_守护进程.md         # 详细使用说明
│   └── README_自动重启总结.md     # 功能总结
└── 测试
    └── test_daemon.py             # 功能测试脚本
```

## ✅ 总结

ChatMonitor 现在具备了完整的自动重启和系统通知功能，可以：

1. **自动监控程序状态** - 实时检测程序崩溃
2. **智能重启机制** - 可配置的重启策略
3. **跨平台通知** - 声音和桌面通知
4. **详细日志记录** - 完整的操作记录
5. **多种启动方式** - 适应不同使用场景

这些功能确保了 ChatMonitor 在生产环境中的稳定性和可靠性，同时提供了良好的用户体验。 