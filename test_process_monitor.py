#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_monitor_dynamic import check_process, play_sound, debug_log, clear_debug_log

def test_process_monitor():
    """测试进程监控功能"""
    print("🔍 开始测试进程监控...")
    
    # 清空调试日志
    clear_debug_log()
    
    # 测试目标应用名称
    test_apps = ["Mango", "WeChat", "QQ", "Telegram", "Slack"]
    
    for app_name in test_apps:
        print(f"\n--- 测试应用: {app_name} ---")
        try:
            is_running = check_process(app_name)
            print(f"应用 {app_name} 运行状态: {'✅ 正在运行' if is_running else '❌ 未运行'}")
            
            if not is_running:
                print("🔊 播放进程退出提醒音...")
                try:
                    play_sound("error")
                    print("✅ 进程退出提醒音播放成功")
                except Exception as e:
                    print(f"❌ 进程退出提醒音播放失败: {e}")
            
        except Exception as e:
            print(f"检查进程异常: {e}")
        
        time.sleep(1)  # 等待1秒
    
    print("\n📋 调试日志:")
    try:
        with open("/tmp/chatmonitor_debug.log", "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"读取日志失败: {e}")

if __name__ == "__main__":
    test_process_monitor() 