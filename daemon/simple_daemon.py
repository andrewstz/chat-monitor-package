#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的守护进程模块
可以独立导入到main分支代码中，最小化修改
"""

import os
import sys
import time
import threading
import subprocess
import psutil
from datetime import datetime

class SimpleDaemon:
    """简单的守护进程类"""
    
    def __init__(self, app_name="main_monitor_gui_app.py", max_restarts=5, cooldown_hours=1):
        self.app_name = app_name
        self.max_restarts = max_restarts
        self.cooldown_hours = cooldown_hours
        self.running = False
        self.restart_count = 0
        self.last_restart_time = 0
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [DAEMON] {message}\n"
        
        # 写入日志文件
        try:
            with open("/tmp/chatmonitor_daemon.log", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except:
            pass
        
        # 同时输出到控制台
        print(log_entry.strip())
    
    def find_app_process(self):
        """查找应用进程"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline'] and self.app_name in ' '.join(proc.info['cmdline']):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    def start_app(self):
        """启动应用"""
        try:
            # 检查是否已经运行
            if self.find_app_process():
                self.log(f"应用 {self.app_name} 已在运行")
                return True
            
            # 启动应用
            if sys.platform == "win32":
                # Windows
                subprocess.Popen([sys.executable, self.app_name], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # macOS/Linux
                subprocess.Popen([sys.executable, self.app_name])
            
            self.log(f"✅ 应用 {self.app_name} 启动成功")
            return True
            
        except Exception as e:
            self.log(f"❌ 启动应用失败: {e}")
            return False
    
    def monitor_loop(self):
        """监控循环"""
        self.log("🚀 守护进程启动")
        
        while self.running:
            try:
                # 检查应用是否运行
                proc = self.find_app_process()
                
                if not proc:
                    # 应用未运行，尝试重启
                    current_time = time.time()
                    hours_since_last_restart = (current_time - self.last_restart_time) / 3600
                    
                    # 检查是否在冷却期内
                    if hours_since_last_restart < self.cooldown_hours:
                        self.log(f"⏰ 冷却期内，跳过重启 ({self.cooldown_hours - hours_since_last_restart:.1f}小时剩余)")
                        time.sleep(30)
                        continue
                    
                    # 检查重启次数限制
                    if self.restart_count >= self.max_restarts:
                        self.log(f"⚠️ 达到最大重启次数 ({self.max_restarts})，停止监控")
                        break
                    
                    self.log(f"🔄 应用未运行，尝试重启 (第{self.restart_count + 1}次)")
                    
                    if self.start_app():
                        self.restart_count += 1
                        self.last_restart_time = current_time
                        self.log(f"✅ 重启成功，等待应用稳定...")
                        time.sleep(10)  # 等待应用启动
                    else:
                        self.log(f"❌ 重启失败")
                        time.sleep(30)
                else:
                    # 应用正在运行，重置计数器
                    if self.restart_count > 0:
                        self.log(f"✅ 应用运行正常，重置重启计数器")
                        self.restart_count = 0
                        self.last_restart_time = 0
                
                # 等待下次检查
                time.sleep(10)
                
            except Exception as e:
                self.log(f"❌ 监控循环错误: {e}")
                time.sleep(30)
    
    def start(self):
        """启动守护进程"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.log("🛡️ 守护进程已启动")
    
    def stop(self):
        """停止守护进程"""
        self.running = False
        self.log("🛑 守护进程已停止")

def run_daemon():
    """运行守护进程"""
    daemon = SimpleDaemon()
    try:
        daemon.start()
        # 保持主线程运行
        while daemon.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 收到中断信号")
    finally:
        daemon.stop()

if __name__ == "__main__":
    run_daemon() 