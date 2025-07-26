# ChatMonitor 守护进程使用说明

## 概述

这是一个**最小化修改**的守护进程方案，可以在main分支代码基础上添加守护进程功能，而不需要大幅修改原有代码。

## 文件说明

### 核心文件
- `simple_daemon.py` - 独立的守护进程模块
- `start_with_daemon.sh` - macOS/Linux启动脚本
- `start_with_daemon.bat` - Windows启动脚本

### 特点
- ✅ **最小化修改**: 不需要修改main分支的核心代码
- ✅ **独立模块**: 守护进程完全独立，可以单独使用
- ✅ **跨平台**: 支持macOS、Linux、Windows
- ✅ **简单易用**: 通过启动脚本选择是否启用守护进程

## 使用方法

### 1. 普通模式（无守护进程）
```bash
# macOS/Linux
./start_with_daemon.sh

# Windows
start_with_daemon.bat
```

### 2. 守护进程模式
```bash
# macOS/Linux
./start_with_daemon.sh --daemon

# Windows
start_with_daemon.bat --daemon
```

### 3. 直接使用Python
```bash
# 普通模式
python main_monitor_gui_app.py

# 守护进程模式
python simple_daemon.py
```

## 守护进程功能

### 监控功能
- 🔍 **进程监控**: 每10秒检查应用是否运行
- 🔄 **自动重启**: 应用崩溃时自动重启
- ⏰ **冷却机制**: 1小时内最多重启5次，避免无限重启
- 📝 **日志记录**: 详细记录守护进程活动

### 配置参数
```python
SimpleDaemon(
    app_name="main_monitor_gui_app.py",  # 应用文件名
    max_restarts=5,                      # 最大重启次数
    cooldown_hours=1                     # 冷却时间（小时）
)
```

### 日志文件
- **守护进程日志**: `/tmp/chatmonitor_daemon.log`
- **应用日志**: `/tmp/chatmonitor_debug.log`

## 与main分支的差异

### 最小化修改
这个方案**不需要修改main分支的核心代码**，只需要：

1. 添加 `simple_daemon.py` 文件
2. 添加启动脚本
3. 可选：在main分支中添加简单的守护进程导入

### 可选的main分支集成
如果希望在main分支中集成守护进程，只需要在 `main_monitor_gui_app.py` 中添加：

```python
# 在文件顶部添加导入
from simple_daemon import SimpleDaemon

# 在main函数中添加参数解析
parser.add_argument("--daemon", action="store_true", help="启用守护进程")

# 在应用启动时检查
if args.daemon:
    daemon = SimpleDaemon()
    daemon.start()
```

## 优势对比

### 当前方案的优势
- ✅ **代码简洁**: 守护进程逻辑独立，易于维护
- ✅ **向后兼容**: 不影响main分支的现有功能
- ✅ **灵活选择**: 用户可以选择是否启用守护进程
- ✅ **易于调试**: 守护进程和应用分离，便于问题定位

### 与之前方案的对比
- ❌ **之前**: 大幅修改main分支代码，增加复杂性
- ✅ **现在**: 独立模块，最小化修改，保持代码简洁

## 故障排除

### 常见问题

1. **守护进程无法启动应用**
   - 检查Python环境是否正确激活
   - 确认 `main_monitor_gui_app.py` 文件存在
   - 查看守护进程日志: `/tmp/chatmonitor_daemon.log`

2. **应用频繁重启**
   - 检查应用是否有严重错误
   - 查看应用日志: `/tmp/chatmonitor_debug.log`
   - 调整 `max_restarts` 和 `cooldown_hours` 参数

3. **权限问题**
   - 确保脚本有执行权限: `chmod +x start_with_daemon.sh`
   - 检查文件读写权限

### 调试命令
```bash
# 查看守护进程日志
tail -f /tmp/chatmonitor_daemon.log

# 查看应用日志
tail -f /tmp/chatmonitor_debug.log

# 检查进程状态
ps aux | grep main_monitor_gui_app
```

## 总结

这个方案实现了**最小化修改**的目标：
- 保持了main分支代码的简洁性
- 提供了独立的守护进程功能
- 用户可以根据需要选择是否启用
- 便于维护和调试

通过这种方式，我们既获得了守护进程的可靠性，又保持了代码的简洁性和可维护性。 