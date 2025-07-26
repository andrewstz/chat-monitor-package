#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor 守护进程启动器
独立运行，不依赖 tkinter
"""

import os
import sys
import time
import signal
import threading
import subprocess
import psutil
import platform
from datetime import datetime

class DaemonLauncher:
    def __init__(self):
        self.running = False
        self.main_process = None
        self.monitor_thread = None
        self.max_restarts = 5
        self.restart_delay = 10
        self.restart_count = 0
        self.last_restart_time = 0
        
        # 平台检测
        self.platform = platform.system().lower()
        
        # 日志文件路径
        self.log_file = self._get_log_path()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _get_log_path(self):
        """获取日志文件路径"""
        if self.platform == "darwin":  # macOS
            return "/tmp/chatmonitor_daemon.log"
        elif self.platform == "windows":
            return os.path.join(os.getenv('TEMP', ''), "chatmonitor_daemon.log")
        else:  # Linux
            return "/tmp/chatmonitor_daemon.log"
    
    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        self.log_message("INFO", f"收到信号 {signum}，正在停止守护进程...")
        self.stop()
    
    def log_message(self, level, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}"
        print(log_message)
        
        # 写入日志文件
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"写入日志失败: {e}")
    
    def play_system_sound(self, sound_type="default"):
        """播放系统声音"""
        try:
            if self.platform == "darwin":  # macOS
                sound_files = {
                    "default": "/System/Library/Sounds/Ping.aiff",
                    "alert": "/System/Library/Sounds/Basso.aiff",
                    "warning": "/System/Library/Sounds/Sosumi.aiff",
                    "success": "/System/Library/Sounds/Glass.aiff"
                }
                sound_file = sound_files.get(sound_type, sound_files["default"])
                subprocess.run(["afplay", sound_file], capture_output=True, timeout=5)
                
            elif self.platform == "windows":
                import winsound
                sound_types = {
                    "default": winsound.MB_ICONASTERISK,
                    "alert": winsound.MB_ICONEXCLAMATION,
                    "warning": winsound.MB_ICONEXCLAMATION,
                    "success": winsound.MB_ICONASTERISK
                }
                sound_type_code = sound_types.get(sound_type, winsound.MB_ICONASTERISK)
                winsound.MessageBeep(sound_type_code)
                
            else:  # Linux
                subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"], 
                             capture_output=True, timeout=5)
                
        except Exception as e:
            self.log_message("WARN", f"播放系统声音失败: {e}")
    
    def send_desktop_notification(self, title, message):
        """发送桌面通知"""
        try:
            if self.platform == "darwin":  # macOS
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(["osascript", "-e", script], capture_output=True, timeout=10)
                
            elif self.platform == "linux":
                subprocess.run(["notify-send", title, message], capture_output=True, timeout=10)
                
            elif self.platform == "windows":
                # Windows 使用 PowerShell 发送通知
                script = f'''
                Add-Type -AssemblyName System.Windows.Forms
                $notification = New-Object System.Windows.Forms.NotifyIcon
                $notification.Icon = [System.Drawing.SystemIcons]::Information
                $notification.BalloonTipTitle = "{title}"
                $notification.BalloonTipText = "{message}"
                $notification.Visible = $true
                $notification.ShowBalloonTip(5000)
                '''
                subprocess.run(["powershell", "-Command", script], capture_output=True, timeout=10)
                
        except Exception as e:
            self.log_message("WARN", f"发送桌面通知失败: {e}")
    
    def find_main_script(self):
        """查找主程序脚本"""
        # 可能的脚本名称
        possible_scripts = [
            "main_monitor_gui_app.py",
            "main_monitor_gui.py",
            "main_monitor_dynamic.py"
        ]
        
        # 检查当前目录
        for script in possible_scripts:
            if os.path.exists(script):
                return script
        
        # 检查打包后的资源路径
        if hasattr(sys, '_MEIPASS'):  # PyInstaller 打包
            resource_path = sys._MEIPASS
            for script in possible_scripts:
                script_path = os.path.join(resource_path, script)
                if os.path.exists(script_path):
                    return script_path
        
        return None
    
    def start_main_program(self):
        """启动主程序"""
        try:
            main_script = self.find_main_script()
            if not main_script:
                self.log_message("ERROR", "找不到主程序脚本")
                return None
            
            self.log_message("INFO", f"启动主程序: {main_script}")
            
            # 构建启动命令
            if hasattr(sys, '_MEIPASS'):  # 打包后的应用
                # 直接运行可执行文件
                if self.platform == "darwin":
                    cmd = ["./ChatMonitor"]
                elif self.platform == "windows":
                    cmd = ["ChatMonitor.exe"]
                else:
                    cmd = ["./ChatMonitor"]
            else:
                # 开发环境
                cmd = [sys.executable, main_script]
            
            # 启动进程
            self.main_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            self.log_message("INFO", f"主程序已启动 (PID: {self.main_process.pid})")
            return self.main_process
            
        except Exception as e:
            self.log_message("ERROR", f"启动主程序失败: {e}")
            return None
    
    def is_process_running(self):
        """检查主程序是否在运行"""
        if not self.main_process:
            return False
        
        try:
            # 检查进程是否还在运行
            return self.main_process.poll() is None
        except Exception:
            return False
    
    def monitor_loop(self):
        """监控循环"""
        self.log_message("INFO", "开始监控主程序...")
        
        while self.running:
            try:
                if not self.is_process_running():
                    current_time = time.time()
                    
                    # 检查重启限制
                    if (self.restart_count >= self.max_restarts and 
                        current_time - self.last_restart_time < 3600):  # 1小时内限制重启次数
                        self.log_message("WARN", f"已达到最大重启次数 ({self.max_restarts})，等待1小时后重试")
                        time.sleep(3600)  # 等待1小时
                        self.restart_count = 0
                        continue
                    
                    # 检查重启延迟
                    if current_time - self.last_restart_time < self.restart_delay:
                        remaining = self.restart_delay - (current_time - self.last_restart_time)
                        self.log_message("DEBUG", f"等待重启延迟: {remaining:.1f}秒")
                        time.sleep(1)
                        continue
                    
                    # 执行重启
                    self.restart_count += 1
                    self.last_restart_time = current_time
                    
                    self.log_message("WARN", f"检测到程序崩溃，开始第 {self.restart_count} 次重启...")
                    
                    # 播放系统声音和发送通知
                    self.play_system_sound("alert")
                    self.send_desktop_notification("ChatMonitor", f"程序崩溃，正在重启 ({self.restart_count}/{self.max_restarts})")
                    
                    # 启动新进程
                    if self.start_main_program():
                        self.log_message("INFO", "重启成功")
                    else:
                        self.log_message("ERROR", "重启失败")
                
                # 进程正常运行，重置重启计数
                else:
                    if self.restart_count > 0:
                        self.log_message("INFO", "程序运行正常，重置重启计数")
                        self.restart_count = 0
                
                # 等待一段时间再检查
                time.sleep(5)
                
            except Exception as e:
                self.log_message("ERROR", f"监控过程中发生错误: {e}")
                time.sleep(10)
    
    def start(self):
        """启动守护进程"""
        if self.running:
            self.log_message("WARN", "守护进程已在运行")
            return
        
        self.log_message("INFO", "启动 ChatMonitor 守护进程...")
        self.log_message("INFO", f"平台: {self.platform}")
        self.log_message("INFO", f"日志文件: {self.log_file}")
        
        # 播放启动声音
        self.play_system_sound("success")
        self.send_desktop_notification("ChatMonitor", "守护进程已启动")
        
        # 启动主程序
        if not self.start_main_program():
            self.log_message("ERROR", "主程序启动失败")
            return
        
        # 启动监控线程
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.log_message("INFO", "守护进程启动完成")
    
    def stop(self):
        """停止守护进程"""
        if not self.running:
            return
        
        self.log_message("INFO", "正在停止守护进程...")
        self.running = False
        
        # 停止主程序
        if self.main_process:
            try:
                self.main_process.terminate()
                self.main_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.main_process.kill()
            except Exception as e:
                self.log_message("WARN", f"停止主程序时发生错误: {e}")
        
        # 等待监控线程结束
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        
        self.log_message("INFO", "守护进程已停止")
        self.play_system_sound("success")
        self.send_desktop_notification("ChatMonitor", "守护进程已停止")

def main():
    """主函数"""
    print("🚀 ChatMonitor 守护进程启动器")
    print("=" * 40)
    
    # 检查依赖
    try:
        import psutil
    except ImportError:
        print("❌ 缺少依赖: psutil")
        print("请运行: pip install psutil")
        return
    
    # 创建并启动守护进程
    launcher = DaemonLauncher()
    
    try:
        launcher.start()
        
        # 保持主线程运行
        while launcher.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 收到中断信号")
    except Exception as e:
        print(f"❌ 守护进程运行失败: {e}")
    finally:
        launcher.stop()

if __name__ == "__main__":
    main() 