@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ChatMonitor Windows 启动脚本
:: 包含自动重启和系统通知功能

:: 设置颜色代码
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

:: 日志函数
:log_message
set "level=%~1"
set "message=%~2"
for /f "tokens=1-3 delims=: " %%a in ("%time%") do set "timestamp=%%a:%%b:%%c"
echo %timestamp% %level%: %message%
echo [%date% %time%] %level%: %message% >> "%TEMP%\chatmonitor_startup.log"
goto :eof

:: 播放系统声音
:play_system_sound
set "sound_type=%~1"
if "%sound_type%"=="alert" (
    echo 
) else if "%sound_type%"=="success" (
    echo 
) else (
    echo 
)
goto :eof

:: 发送桌面通知
:send_notification
set "title=%~1"
set "message=%~2"
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $notification = New-Object System.Windows.Forms.NotifyIcon; $notification.Icon = [System.Drawing.SystemIcons]::Information; $notification.BalloonTipTitle = '%title%'; $notification.BalloonTipText = '%message%'; $notification.Visible = $true; $notification.ShowBalloonTip(5000)" 2>nul
goto :eof

:: 检查依赖
:check_dependencies
call :log_message "INFO" "检查系统依赖..."

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    call :log_message "ERROR" "Python 未安装"
    exit /b 1
)

:: 检查必要的 Python 包
for %%p in (psutil pyautogui opencv-python pytesseract) do (
    python -c "import %%p" 2>nul
    if errorlevel 1 (
        call :log_message "WARN" "缺少 Python 包: %%p"
    )
)

call :log_message "INFO" "依赖检查完成"
exit /b 0

:: 启动主程序
:start_main_program
call :log_message "INFO" "启动 ChatMonitor 主程序..."

:: 检查主程序文件是否存在
if not exist "main_monitor_gui_app.py" (
    call :log_message "ERROR" "找不到主程序文件: main_monitor_gui_app.py"
    exit /b 1
)

:: 启动程序
start /b python main_monitor_gui_app.py
set "pid=%ERRORLEVEL%"

call :log_message "INFO" "主程序已启动 (PID: %pid%)"
echo %pid% > "%TEMP%\chatmonitor.pid"

:: 等待一段时间检查进程是否正常启动
timeout /t 3 /nobreak >nul
tasklist /FI "PID eq %pid%" 2>nul | find "%pid%" >nul
if errorlevel 1 (
    call :log_message "ERROR" "主程序启动失败"
    call :play_system_sound "alert"
    call :send_notification "ChatMonitor" "程序启动失败"
    exit /b 1
) else (
    call :log_message "INFO" "主程序启动成功"
    call :play_system_sound "success"
    call :send_notification "ChatMonitor" "程序启动成功"
    exit /b 0
)

:: 监控程序状态
:monitor_program
set "max_restarts=5"
set "restart_count=0"
set "restart_delay=10"

call :log_message "INFO" "开始监控程序状态..."
call :log_message "INFO" "最大重启次数: %max_restarts%"
call :log_message "INFO" "重启延迟: %restart_delay%秒"

:monitor_loop
:: 检查 PID 文件
if exist "%TEMP%\chatmonitor.pid" (
    set /p pid=<"%TEMP%\chatmonitor.pid"
    
    :: 检查进程是否还在运行
    tasklist /FI "PID eq %pid%" 2>nul | find "%pid%" >nul
    if errorlevel 1 (
        call :log_message "WARN" "检测到程序崩溃 (PID: %pid%)"
        
        :: 检查重启限制
        if %restart_count% geq %max_restarts% (
            call :log_message "ERROR" "已达到最大重启次数 (%max_restarts%)，停止监控"
            call :play_system_sound "alert"
            call :send_notification "ChatMonitor" "程序崩溃次数过多，已停止自动重启"
            goto :end_monitor
        )
        
        :: 执行重启
        set /a restart_count+=1
        call :log_message "INFO" "开始第 %restart_count% 次重启..."
        
        call :play_system_sound "warning"
        call :send_notification "ChatMonitor" "程序崩溃，正在重启 (%restart_count%/%max_restarts%)"
        
        :: 等待重启延迟
        timeout /t %restart_delay% /nobreak >nul
        
        :: 启动新进程
        call :start_main_program
        if errorlevel 1 (
            call :log_message "ERROR" "重启失败"
        ) else (
            call :log_message "INFO" "重启成功"
        )
    ) else (
        if %restart_count% gtr 0 (
            call :log_message "INFO" "程序运行正常，重置重启计数"
            set "restart_count=0"
        )
    )
) else (
    call :log_message "WARN" "找不到 PID 文件，重新启动程序"
    call :start_main_program
)

:: 等待一段时间再检查
timeout /t 5 /nobreak >nul
goto :monitor_loop

:end_monitor
call :log_message "INFO" "监控已停止"

:: 清理函数
:cleanup
call :log_message "INFO" "正在清理..."

:: 删除 PID 文件
if exist "%TEMP%\chatmonitor.pid" del "%TEMP%\chatmonitor.pid"

:: 停止所有相关进程
taskkill /f /im python.exe /fi "WINDOWTITLE eq ChatMonitor*" 2>nul

call :log_message "INFO" "清理完成"

:: 主函数
:main
call :log_message "INFO" "ChatMonitor 启动脚本开始执行"
call :log_message "INFO" "当前目录: %CD%"
call :log_message "INFO" "操作系统: Windows"

:: 检查依赖
call :check_dependencies
if errorlevel 1 (
    call :log_message "ERROR" "依赖检查失败，退出"
    exit /b 1
)

:: 播放启动声音
call :play_system_sound "success"
call :send_notification "ChatMonitor" "启动脚本已加载"

:: 启动主程序
call :start_main_program
if errorlevel 1 (
    call :log_message "ERROR" "主程序启动失败，退出"
    exit /b 1
)

:: 开始监控
call :monitor_program

:: 显示帮助信息
:show_help
echo ChatMonitor 启动脚本
echo.
echo 用法: %0 [选项]
echo.
echo 选项:
echo   -h, --help     显示此帮助信息
echo   -t, --test     测试系统声音和通知
echo   -c, --clean    清理残留进程
echo.
echo 功能:
echo   - 自动启动 ChatMonitor 主程序
echo   - 监控程序状态，崩溃时自动重启
echo   - 播放系统声音和发送桌面通知
echo   - 记录详细日志到 %%TEMP%%\chatmonitor_startup.log

:: 测试功能
:test_features
echo 🧪 测试系统功能...
echo 🔊 测试系统声音...
call :play_system_sound "success"
timeout /t 1 /nobreak >nul
call :play_system_sound "warning"
timeout /t 1 /nobreak >nul
call :play_system_sound "alert"
echo 📱 测试桌面通知...
call :send_notification "ChatMonitor 测试" "这是一条测试通知"
echo ✅ 测试完成

:: 清理功能
:cleanup_only
echo 🧹 清理残留进程...
call :cleanup
echo ✅ 清理完成

:: 解析命令行参数
if "%1"=="-h" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-t" goto :test_features
if "%1"=="--test" goto :test_features
if "%1"=="-c" goto :cleanup_only
if "%1"=="--clean" goto :cleanup_only
if "%1"=="" goto :main

echo 错误: 未知选项 %1
goto :show_help 