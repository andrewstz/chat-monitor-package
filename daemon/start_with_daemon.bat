@echo off
REM ChatMonitor 启动脚本（支持守护进程）
REM 用法: start_with_daemon.bat [--daemon]

REM 切换到上级目录（项目根目录）
cd /d "%~dp0.."

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到python命令，请确保已激活conda环境
    pause
    exit /b 1
)

REM 检查主程序文件
if not exist "main_monitor_gui_app.py" (
    echo ❌ 未找到main_monitor_gui_app.py文件
    pause
    exit /b 1
)

REM 检查守护进程文件
if not exist "daemon\simple_daemon.py" (
    echo ❌ 未找到daemon\simple_daemon.py文件
    pause
    exit /b 1
)

REM 检查参数
if "%1"=="--daemon" (
    echo 🚀 启动ChatMonitor（守护进程模式）
    echo 📝 守护进程将监控应用状态，自动重启崩溃的应用
    echo 📝 日志文件: %TEMP%\chatmonitor_daemon.log
    echo.
    
    REM 启动守护进程
    python daemon\simple_daemon.py
) else (
    echo 🚀 启动ChatMonitor（普通模式）
    echo 📝 直接启动应用，无守护进程
    echo.
    
    REM 直接启动应用
    python main_monitor_gui_app.py
)

pause 