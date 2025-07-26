# 独立守护进程说明

## 概述

现在ChatMonitor使用独立的守护进程来监控主程序，当主程序意外退出时会自动重启。

## 架构

### 进程结构
```
┌─────────────────┐    ┌─────────────────┐
│   主程序        │    │   守护进程      │
│ main_monitor_   │    │ daemon_monitor  │
│ gui_app.py      │    │ .py             │
└─────────────────┘    └─────────────────┘
        │                       │
        │                       │ 监控
        │                       ▼
        │                ┌─────────────────┐
        │                │   进程检测      │
        │                │   重启逻辑      │
        │                └─────────────────┘
        │                       │
        └───────────────────────┘
                重启
```

### 优势
- ✅ **独立运行**: 守护进程独立于主程序，主程序关闭不影响守护进程
- ✅ **自动重启**: 主程序意外退出时自动重启
- ✅ **稳定监控**: 每30秒检查一次主程序状态
- ✅ **冷却机制**: 启动后60秒内不进行重启检查，避免误判
- ✅ **详细日志**: 记录所有监控和重启操作

## 使用方法

### 1. 启动应用和守护进程
```bash
# 方法1: 使用启动脚本
./start_with_daemon.sh

# 方法2: 手动启动
python daemon_monitor.py &  # 启动守护进程
python main_monitor_gui_app.py  # 启动主程序
```

### 2. 停止所有进程
```bash
# 使用停止脚本
./stop_all.sh

# 或手动停止
pkill -f "main_monitor_gui_app.py"
pkill -f "daemon_monitor.py"
```

### 3. 查看状态
```bash
# 查看进程
ps aux | grep -E "(main_monitor_gui_app|daemon_monitor)" | grep -v grep

# 查看守护进程日志
tail -f /tmp/chatmonitor_daemon.log
```

## 守护进程工作原理

### 1. 启动阶段
- 守护进程启动后记录启动时间
- 前60秒为冷却期，不进行重启检查
- 每30秒检查一次主程序状态

### 2. 监控阶段
- 扫描所有进程，查找主程序进程
- 如果找到主程序，记录状态
- 如果没找到主程序且超过冷却期，执行重启

### 3. 重启阶段
- 检测到主程序退出
- 启动新的主程序进程
- 等待5秒让新进程稳定
- 继续监控

### 4. 日志记录
- 所有操作都记录到 `/tmp/chatmonitor_daemon.log`
- 包括启动、监控、重启、错误等信息

## 测试验证

### 测试1: 正常启动
```bash
./start_with_daemon.sh
# 结果: 应该看到两个进程运行
```

### 测试2: 关闭主程序
```bash
# 找到主程序PID
ps aux | grep main_monitor_gui_app

# 关闭主程序
kill <主程序PID>

# 等待30秒后检查
ps aux | grep main_monitor_gui_app
# 结果: 应该看到新的主程序进程
```

### 测试3: 查看日志
```bash
tail -f /tmp/chatmonitor_daemon.log
# 应该看到类似输出:
# 2025-07-26 10:00:00,123 - INFO - ✅ 主程序正在运行 (PID: 12345)
# 2025-07-26 10:00:30,456 - INFO - ❌ 主程序已退出，正在重启...
# 2025-07-26 10:00:30,789 - INFO - ✅ 主程序重启成功
```

## 故障排除

### 问题1: 守护进程没有启动
```bash
# 检查文件是否存在
ls -la daemon_monitor.py

# 手动启动测试
python daemon_monitor.py
```

### 问题2: 主程序没有重启
```bash
# 检查守护进程是否在运行
ps aux | grep daemon_monitor

# 查看守护进程日志
tail -20 /tmp/chatmonitor_daemon.log
```

### 问题3: 进程冲突
```bash
# 停止所有相关进程
./stop_all.sh

# 重新启动
./start_with_daemon.sh
```

## 配置选项

### 守护进程配置
可以在 `daemon_monitor.py` 中修改以下参数：

```python
# 检查间隔（秒）
time.sleep(30)

# 冷却期（秒）
if time.time() - self.start_time < 60:

# 重启等待时间（秒）
time.sleep(5)
```

### 日志配置
```python
# 日志文件路径
logging.FileHandler('/tmp/chatmonitor_daemon.log')

# 日志级别
logging.basicConfig(level=logging.INFO)
```

## 打包应用

### 开发环境
- 守护进程和主程序分别运行
- 使用 `daemon_monitor.py` 监控 `main_monitor_gui_app.py`

### 打包环境
- 守护进程监控打包后的应用
- 自动检测 `sys.frozen` 状态
- 使用 `sys.executable` 启动打包应用

## 总结

独立守护进程系统提供了：
- 🔄 **自动重启**: 主程序意外退出时自动重启
- 🛡️ **稳定监控**: 独立的监控进程，不受主程序影响
- 📊 **详细日志**: 完整的操作记录
- ⚡ **快速响应**: 30秒内检测到程序退出
- 🛠️ **易于管理**: 简单的启动和停止脚本

这个系统确保了ChatMonitor应用的稳定运行，即使主程序意外退出也能自动恢复。 