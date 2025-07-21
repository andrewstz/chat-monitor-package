#!/usr/bin/env python3
"""
简单的网络监控测试
"""

import time
import requests
from datetime import datetime

# 网络监控全局变量
last_network_check_time = time.time()
network_failure_count = 0
network_alert_sent = False

def check_network():
    """简单网络检测"""
    try:
        response = requests.head("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_network_with_alert():
    """网络检测带警报功能"""
    global last_network_check_time, network_failure_count, network_alert_sent
    
    current_time = time.time()
    
    # 配置参数
    consecutive_failures = 1  # 连续失败阈值
    tolerance_minutes = 0.05     # 容错时间（分钟）
    
    # 检查网络
    network_ok = check_network()
    
    if network_ok:
        # 网络正常，重置计数器
        if network_failure_count > 0:
            print(f"✅ 网络恢复正常 - {datetime.now().strftime('%H:%M:%S')}")
        network_failure_count = 0
        network_alert_sent = False
        last_network_check_time = current_time
        return True
    else:
        # 网络异常
        network_failure_count += 1
        print(f"❌ 网络检测失败 ({network_failure_count}/{consecutive_failures}) - {datetime.now().strftime('%H:%M:%S')}")
        
        # 检查是否达到连续失败阈值和时间阈值
        time_since_last_check = current_time - last_network_check_time
        if (network_failure_count >= consecutive_failures and 
            time_since_last_check >= tolerance_minutes * 60):
            
            print(f"🚨 网络异常警报 - 连续失败{network_failure_count}次，超过{tolerance_minutes}分钟")
            print("🔊 播放警告声音")
            return True  # 继续运行，不中断程序
        
        return True  # 继续运行，不中断程序

def main():
    print("🔧 简单网络监控测试")
    print("=" * 40)
    print("💡 现在可以断开网络连接进行测试")
    print()
    
    test_count = 0
    try:
        while True:
            test_count += 1
            print(f"🔍 第{test_count}次网络检测...")
            
            check_network_with_alert()  # 每次检测都调用，不暂停程序
            
            time.sleep(10)  # 每10秒检测一次
            
    except KeyboardInterrupt:
        print("\n⏹️  测试已停止")
    
    print(f"📊 测试完成，共检测{test_count}次")

if __name__ == "__main__":
    main() 