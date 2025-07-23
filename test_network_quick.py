#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_monitor_dynamic import check_network_with_alert, debug_log, clear_debug_log

def test_network_monitor():
    """快速测试网络监控"""
    print("🔍 开始测试网络监控...")
    
    # 清空调试日志
    clear_debug_log()
    
    # 测试网络监控
    for i in range(10):
        print(f"\n--- 第 {i+1} 次测试 ---")
        try:
            result = check_network_with_alert()
            print(f"网络监控结果: {result}")
        except Exception as e:
            print(f"网络监控异常: {e}")
        
        time.sleep(2)  # 等待2秒
    
    print("\n📋 调试日志:")
    try:
        with open("/tmp/chatmonitor_debug.log", "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"读取日志失败: {e}")

if __name__ == "__main__":
    test_network_monitor() 