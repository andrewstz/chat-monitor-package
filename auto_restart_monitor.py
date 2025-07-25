#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor 自动重启监控脚本
监控主程序运行状态，如果崩溃则自动重启
"""

import os
import sys
import time
import subprocess
import signal
import psutil
from datetime import datetime

class AutoRestartMonitor:
    def __init__(self):
        self.target_process_name = "ChatMonitor"  # 目标进程名
        self.main_script = "main_monitor_gui_app.py"  # 主程序脚本
        self.max_restart_attempts = 5  # 最大重启次数
        self.restart_delay = 10  # 重启延迟（秒）
        self.restart_count = 0
        self.last_restart_time = 0
        
    def log_message(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # 写入日志文件
        try:
            with open("/tmp/chatmonitor_restart.log", "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"写入日志失败: {e}")
    
    def play_system_sound(self):
        """播放系统声音"""
        try:
            # macOS 系统声音
            if sys.platform == "darwin":
                subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"], 
                             capture_output=True, timeout=5)
            # Linux 系统声音
            elif sys.platform.startswith("linux"):
                subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"], 
                             capture_output=True, timeout=5)
            # Windows 系统声音
            elif sys.platform == "win32":
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            self.log_message(f"播放系统声音失败: {e}")
    
    def is_process_running(self):
        """检查目标进程是否在运行"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # 检查进程名
                    if self.target_process_name in proc.info['name']:
                        return True
                    
                    # 检查命令行参数
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if self.main_script in cmdline:
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except Exception as e:
            self.log_message(f"检查进程状态失败: {e}")
            return False
    
    def start_main_program(self):
        """启动主程序"""
        try:
            self.log_message("🚀 启动 ChatMonitor 主程序...")
            
            # 构建启动命令
            cmd = [sys.executable, self.main_script]
            
            # 启动进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            self.log_message(f"✅ 主程序已启动 (PID: {process.pid})")
            return process
            
        except Exception as e:
            self.log_message(f"❌ 启动主程序失败: {e}")
            return None
    
    def monitor_and_restart(self):
        """监控并自动重启"""
        self.log_message("🔍 开始监控 ChatMonitor 程序...")
        self.log_message(f"📊 配置信息:")
        self.log_message(f"  - 目标进程: {self.target_process_name}")
        self.log_message(f"  - 主程序脚本: {self.main_script}")
        self.log_message(f"  - 最大重启次数: {self.max_restart_attempts}")
        self.log_message(f"  - 重启延迟: {self.restart_delay}秒")
        
        current_process = None
        
        while True:
            try:
                # 检查进程是否运行
                if not self.is_process_running():
                    current_time = time.time()
                    
                    # 检查重启限制
                    if (self.restart_count >= self.max_restart_attempts and 
                        current_time - self.last_restart_time < 3600):  # 1小时内限制重启次数
                        self.log_message(f"⚠️ 已达到最大重启次数 ({self.max_restart_attempts})，等待1小时后重试")
                        time.sleep(3600)  # 等待1小时
                        self.restart_count = 0
                        continue
                    
                    # 检查重启延迟
                    if current_time - self.last_restart_time < self.restart_delay:
                        remaining = self.restart_delay - (current_time - self.last_restart_time)
                        self.log_message(f"⏰ 等待重启延迟: {remaining:.1f}秒")
                        time.sleep(1)
                        continue
                    
                    # 执行重启
                    self.restart_count += 1
                    self.last_restart_time = current_time
                    
                    self.log_message(f"🔄 检测到程序崩溃，开始第 {self.restart_count} 次重启...")
                    
                    # 播放系统声音提醒
                    self.play_system_sound()
                    
                    # 启动新进程
                    current_process = self.start_main_program()
                    
                    if current_process:
                        self.log_message("✅ 重启成功")
                    else:
                        self.log_message("❌ 重启失败")
                
                # 进程正常运行，重置重启计数
                else:
                    if self.restart_count > 0:
                        self.log_message("✅ 程序运行正常，重置重启计数")
                        self.restart_count = 0
                
                # 等待一段时间再检查
                time.sleep(5)
                
            except KeyboardInterrupt:
                self.log_message("🛑 收到中断信号，停止监控")
                break
            except Exception as e:
                self.log_message(f"❌ 监控过程中发生错误: {e}")
                time.sleep(10)
    
    def run(self):
        """运行监控器"""
        try:
            self.monitor_and_restart()
        except KeyboardInterrupt:
            self.log_message("🛑 监控器已停止")
        except Exception as e:
            self.log_message(f"❌ 监控器运行失败: {e}")

def main():
    """主函数"""
    print("🚀 ChatMonitor 自动重启监控器")
    print("=" * 50)
    
    # 检查依赖
    try:
        import psutil
    except ImportError:
        print("❌ 缺少依赖: psutil")
        print("请运行: pip install psutil")
        return
    
    # 检查主程序文件是否存在
    if not os.path.exists("main_monitor_gui_app.py"):
        print("❌ 找不到主程序文件: main_monitor_gui_app.py")
        return
    
    # 启动监控器
    monitor = AutoRestartMonitor()
    monitor.run()

if __name__ == "__main__":
    main() 