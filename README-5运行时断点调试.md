# 加的这些路径解析的代码可以在ChatMonitor运行起来时再断点调试吗
main_monitor_dynamic.py   _resolve_model_path
是的，可以在ChatMonitor运行时进行断点调试！有几种方法可以实现：
方法1：使用Python调试器（推荐）
让我修改代码，添加一个调试开关：
main_monitor_dynamic.py  CHATMONITOR_DEBUG
现在让我创建一个调试启动脚本：
debug_chatmonitor.sh
方法2：使用远程调试器
让我也创建一个支持远程调试的版本：
remote_debug_chatmonitor.sh
现在让我修改代码，添加远程调试支持
main_monitor_dynamic.py  CHATMONITOR_REMOTE_DEBUG
现在让我们给脚本添加执行权限：
chmod +x debug_chatmonitor.sh remote_debug_chatmonitor.sh
使用方法
现在你有几种调试方式：
方法1：本地断点调试
重新构建应用程序（包含调试代码）
conda activate paddle && ./build_macos_app.sh
启动调试模式
./debug_chatmonitor.sh
`方法2：远程调试（推荐）`
安装debugpy（如果需要）
pip install debugpy
启动远程调试模式
./remote_debug_chatmonitor.sh
然后在VS Code中：
打开调试面板
创建launch.json配置：
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            }
        }
    ]
}
点击"开始调试"




