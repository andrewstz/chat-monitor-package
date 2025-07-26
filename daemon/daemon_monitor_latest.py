#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的守护进程
监控主程序并在需要时重启
"""

import os
import sys
import time
import psutil
import subprocess
import signal
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/chatmonitor_daemon.log'),
        logging.StreamHandler()
    ]
)

class DaemonMonitor:
    def __init__(self):
        self.running = True
        self.start_time = time.time()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """信号处理"""
        logging.info(f"收到信号 {signum}，正在停止守护进程...")
        self.running = False
    
    def find_main_process(self):
        """查找主程序进程"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    # 查找主程序，但排除守护进程本身
                    if ('main_monitor_gui_app.py' in cmdline or 'ChatMonitor' in cmdline) and 'daemon_monitor.py' not in cmdline:
                        return proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    def start_main_process(self):
        """启动主程序"""
        try:
            if getattr(sys, 'frozen', False):
                # 打包后的应用
                app_path = sys.executable
                subprocess.Popen([app_path])
                logging.info("🔄 启动打包后的应用")
            else:
                # 开发环境
                script_path = os.path.abspath("../main_monitor_gui_app.py")
                subprocess.Popen([sys.executable, script_path])
                logging.info("🔄 启动开发环境应用")
            return True
        except Exception as e:
            logging.error(f"❌ 启动主程序失败: {e}")
            return False
    
    def run(self):
        """运行守护进程"""
        logging.info("🛡️ 守护进程启动...")
        
        while self.running:
            try:
                main_pid = self.find_main_process()
                
                if main_pid:
                    logging.info(f"✅ 主程序正在运行 (PID: {main_pid})")
                else:
                    # 检查是否在冷却期内
                    if time.time() - self.start_time < 60:
                        logging.info("⏳ 冷却期内，等待60秒...")
                        time.sleep(30)
                        continue
                    
                    logging.info("❌ 主程序已退出，正在重启...")
                    if self.start_main_process():
                        logging.info("✅ 主程序重启成功")
                        # 等待新进程启动
                        time.sleep(5)
                    else:
                        logging.error("❌ 主程序重启失败")
                
                # 每30秒检查一次
                time.sleep(30)
                
            except Exception as e:
                logging.error(f"❌ 守护进程错误: {e}")
                time.sleep(30)
        
        logging.info("🛑 守护进程已停止")

def main():
    """主函数"""
    daemon = DaemonMonitor()
    daemon.run()

if __name__ == "__main__":
    main() 