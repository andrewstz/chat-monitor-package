# 守护进程使用说明

## 概述

ChatMonitor现在使用独立的守护进程来监控主程序，当主程序意外退出时会自动重启。

## 文件结构

```
doPackage/
├── main_monitor_gui_app.py          # 主程序
├── start_with_daemon.sh             # 启动脚本
├── stop_all.sh                      # 停止脚本
└── daemon/
    ├── daemon_monitor_latest.py     # 守护进程
    ├── start_with_daemon_latest.sh  # 备用启动脚本
    ├── stop_all_latest.sh           # 备用停止脚本
    └── README_独立守护进程说明_latest.md  # 详细说明
```

## 使用方法

### 1. 启动应用和守护进程
```bash
./start_with_daemon.sh
```

### 2. 停止所有进程
```bash
./stop_all.sh
```

### 3. 查看状态
```bash
# 查看进程
ps aux | grep -E "(main_monitor_gui_app|daemon_monitor)" | grep -v grep

# 查看守护进程日志
tail -f /tmp/chatmonitor_daemon.log
```

## 工作原理

1. **启动**: 守护进程和主程序分别启动
2. **监控**: 守护进程每30秒检查一次主程序状态
3. **重启**: 如果主程序退出，守护进程自动重启它
4. **冷却**: 启动后60秒内不进行重启检查

## 优势

- ✅ **独立运行**: 守护进程不受主程序影响
- ✅ **自动重启**: 主程序意外退出时自动重启
- ✅ **稳定监控**: 每30秒检查一次主程序状态
- ✅ **详细日志**: 记录所有监控和重启操作

## 故障排除

### 问题1: 守护进程没有启动
```bash
# 检查文件是否存在
ls -la daemon/daemon_monitor_latest.py

# 手动启动测试
python daemon/daemon_monitor_latest.py
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

## 总结

守护进程系统确保了ChatMonitor应用的稳定运行，即使主程序意外退出也能自动恢复。 