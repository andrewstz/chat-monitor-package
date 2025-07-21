#!/usr/bin/env python3
"""
智能网络监控模块
- 支持连续失败检测，避免网络波动误报
- 可配置的容错时间和检测间隔
- 多种网络检测策略
"""

import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
import queue

class NetworkMonitor:
    def __init__(self, 
                 consecutive_failures=3,      # 连续失败次数阈值
                 check_interval=60,          # 检测间隔（秒）
                 timeout=10,                 # 单次检测超时时间
                 tolerance_minutes=15):      # 容错时间（分钟）
        
        self.consecutive_failures = consecutive_failures
        self.check_interval = check_interval
        self.timeout = timeout
        self.tolerance_minutes = tolerance_minutes
        
        # 状态跟踪
        self.failure_count = 0
        self.last_success_time = None
        self.last_check_time = None
        self.is_network_down = False
        self.alert_sent = False
        
        # 检测历史
        self.check_history = []
        self.max_history_size = 100
        
        # 线程控制
        self.monitoring = False
        self.monitor_thread = None
        self.alert_queue = queue.Queue()
        
        # 检测目标配置 - 只使用谷歌检测
        self.test_targets = [
            {
                "name": "谷歌",
                "url": "https://www.google.com",
                "method": "http"
            }
        ]
    
    def check_http_connectivity(self, url: str) -> bool:
        """检测HTTP连接 - 使用HEAD请求，与原代码保持一致"""
        try:
            response = requests.head(url, timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            print(f"HTTP检测失败 {url}: {e}")
            return False
    

    
    def perform_network_check(self) -> Dict:
        """执行网络检测"""
        check_result = {
            "timestamp": datetime.now(),
            "success": False,
            "details": {},
            "total_tests": len(self.test_targets),
            "passed_tests": 0
        }
        
        for target in self.test_targets:
            test_name = target["name"]
            test_url = target["url"]
            test_method = target["method"]
            
            success = False
            if test_method == "http":
                success = self.check_http_connectivity(test_url)
            
            check_result["details"][test_name] = {
                "method": test_method,
                "target": test_url,
                "success": success
            }
            
            if success:
                check_result["passed_tests"] += 1
        
        # 判断整体是否成功（至少有一个测试通过）
        check_result["success"] = check_result["passed_tests"] > 0
        
        return check_result
    
    def update_network_status(self, check_result: Dict):
        """更新网络状态"""
        current_time = datetime.now()
        
        # 记录检测历史
        self.check_history.append(check_result)
        if len(self.check_history) > self.max_history_size:
            self.check_history.pop(0)
        
        self.last_check_time = current_time
        
        if check_result["success"]:
            # 网络正常
            self.failure_count = 0
            self.last_success_time = current_time
            
            # 如果之前网络异常，现在恢复正常
            if self.is_network_down:
                self.is_network_down = False
                self.alert_sent = False
                print(f"✅ 网络恢复正常 - {current_time.strftime('%H:%M:%S')}")
                self.alert_queue.put({
                    "type": "network_restored",
                    "timestamp": current_time,
                    "message": "网络连接已恢复正常"
                })
        else:
            # 网络异常
            self.failure_count += 1
            print(f"❌ 网络检测失败 ({self.failure_count}/{self.consecutive_failures}) - {current_time.strftime('%H:%M:%S')}")
            
            # 检查是否达到连续失败阈值
            if (self.failure_count >= self.consecutive_failures and 
                not self.is_network_down and 
                not self.alert_sent):
                
                # 修复：首次失败时设置当前时间为最后成功时间
                if self.last_success_time is None:
                    self.last_success_time = current_time
                    print(f"⏳ 首次网络失败，开始计时 - {current_time.strftime('%H:%M:%S')}")
                else:
                    # 检查容错时间
                    time_since_success = current_time - self.last_success_time
                    if time_since_success >= timedelta(minutes=self.tolerance_minutes):
                        self.is_network_down = True
                        self.alert_sent = True
                        print(f"🚨 网络异常警报 - 连续失败{self.failure_count}次，超过容错时间{self.tolerance_minutes}分钟")
                        self.alert_queue.put({
                            "type": "network_down",
                            "timestamp": current_time,
                            "message": f"网络连接异常，连续失败{self.failure_count}次",
                            "failure_count": self.failure_count,
                            "tolerance_minutes": self.tolerance_minutes
                        })
                    else:
                        remaining_time = timedelta(minutes=self.tolerance_minutes) - time_since_success
                        print(f"⏳ 网络异常但未超过容错时间，剩余{remaining_time.seconds}秒")
    
    def get_network_status(self) -> Dict:
        """获取当前网络状态"""
        return {
            "is_network_down": self.is_network_down,
            "failure_count": self.failure_count,
            "consecutive_failures": self.consecutive_failures,
            "last_success_time": self.last_success_time,
            "last_check_time": self.last_check_time,
            "tolerance_minutes": self.tolerance_minutes,
            "check_interval": self.check_interval,
            "alert_sent": self.alert_sent
        }
    
    def get_check_history(self, limit: int = 10) -> List[Dict]:
        """获取检测历史"""
        return self.check_history[-limit:] if self.check_history else []
    
    def reset_status(self):
        """重置状态"""
        self.failure_count = 0
        self.is_network_down = False
        self.alert_sent = False
        self.last_success_time = None
        print("🔄 网络监控状态已重置")
    
    def update_config(self, **kwargs):
        """更新配置"""
        if "consecutive_failures" in kwargs:
            self.consecutive_failures = kwargs["consecutive_failures"]
        if "check_interval" in kwargs:
            self.check_interval = kwargs["check_interval"]
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
        if "tolerance_minutes" in kwargs:
            self.tolerance_minutes = kwargs["tolerance_minutes"]
        
        print(f"⚙️ 网络监控配置已更新: {kwargs}")
    
    def monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                # 执行网络检测
                check_result = self.perform_network_check()
                
                # 更新状态
                self.update_network_status(check_result)
                
                # 等待下次检测
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"网络监控循环出错: {e}")
                time.sleep(self.check_interval)
    
    def start_monitoring(self):
        """开始监控"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
            print(f"🚀 网络监控已启动 - 检测间隔{self.check_interval}秒，容错时间{self.tolerance_minutes}分钟")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("🛑 网络监控已停止")
    
    def get_alert(self, timeout: float = 0) -> Optional[Dict]:
        """获取警报（非阻塞）"""
        try:
            return self.alert_queue.get_nowait()
        except queue.Empty:
            return None

def main():
    """主函数 - 演示网络监控"""
    print("=== 智能网络监控演示 ===")
    
    # 创建网络监控器
    monitor = NetworkMonitor(
        consecutive_failures=3,      # 连续失败3次
        check_interval=30,           # 每30秒检测一次
        timeout=10,                  # 10秒超时
        tolerance_minutes=15         # 15分钟容错时间
    )
    
    print("配置说明：")
    print(f"  - 连续失败阈值: {monitor.consecutive_failures}次")
    print(f"  - 检测间隔: {monitor.check_interval}秒")
    print(f"  - 容错时间: {monitor.tolerance_minutes}分钟")
    print(f"  - 检测超时: {monitor.timeout}秒")
    
    print("\n开始监控...")
    monitor.start_monitoring()
    
    try:
        while True:
            # 检查警报
            alert = monitor.get_alert()
            if alert:
                print(f"\n🚨 收到警报: {alert['message']}")
            
            # 显示状态
            status = monitor.get_network_status()
            print(f"\r网络状态: {'❌异常' if status['is_network_down'] else '✅正常'} "
                  f"失败次数: {status['failure_count']}/{status['consecutive_failures']} "
                  f"时间: {datetime.now().strftime('%H:%M:%S')}", end="")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n用户中断，停止监控...")
        monitor.stop_monitoring()

if __name__ == "__main__":
    main() 