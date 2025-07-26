# Daemon 目录说明

这个目录包含了ChatMonitor的所有守护进程相关文件。

## 文件结构

```
daemon/
├── README.md                           # 本文件
├── simple_daemon.py                    # 简单的守护进程模块
├── daemon_monitor.py                   # 复杂的守护进程模块
├── daemon_launcher.py                  # 守护进程启动器
├── start_with_daemon.sh               # macOS/Linux启动脚本
├── start_with_daemon.bat              # Windows启动脚本
├── start_daemon.sh                    # 旧版启动脚本
├── test_daemon.py                     # 守护进程测试文件
├── README_守护进程使用说明.md          # 详细使用说明
├── README_自动启动守护进程.md          # 自动启动说明
└── README_守护进程.md                  # 守护进程说明
```

## 推荐使用

### 简单方案（推荐）
- **文件**: `simple_daemon.py`
- **启动脚本**: `start_with_daemon.sh` / `start_with_daemon.bat`
- **说明**: `README_守护进程使用说明.md`

### 复杂方案
- **文件**: `daemon_monitor.py` + `daemon_launcher.py`
- **启动脚本**: `start_daemon.sh`
- **说明**: `README_自动启动守护进程.md`

## 快速开始

```bash
# 从项目根目录运行
./daemon/start_with_daemon.sh --daemon

# 或者直接运行
python daemon/simple_daemon.py
```

## 特点

- ✅ **最小化修改**: 不需要修改main分支的核心代码
- ✅ **独立模块**: 守护进程完全独立，可以单独使用
- ✅ **跨平台**: 支持macOS、Linux、Windows
- ✅ **简单易用**: 通过启动脚本选择是否启用守护进程 