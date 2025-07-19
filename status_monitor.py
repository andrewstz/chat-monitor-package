#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor 状态监控脚本
用于跟踪程序运行状态、识别情况和热更新状态
"""

import os
import sys
import time
import psutil
import subprocess
from datetime import datetime

def find_chatmonitor_process():
    """查找 ChatMonitor 进程"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'ChatMonitor' in proc.info['name']:
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def get_process_info(proc):
    """获取进程详细信息"""
    try:
        return {
            'pid': proc.pid,
            'name': proc.name(),
            'status': proc.status(),
            'cpu_percent': proc.cpu_percent(),
            'memory_mb': proc.memory_info().rss / 1024 / 1024,
            'create_time': datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
            'cmdline': ' '.join(proc.cmdline())
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

def check_config_file():
    """检查配置文件状态"""
    config_paths = [
        "config_with_yolo.yaml",
        os.path.expanduser("~/ChatMonitor/config_with_yolo.yaml"),
        "./release/ChatMonitor.app/Contents/Resources/config_with_yolo.yaml"
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            stat = os.stat(path)
            return {
                'path': path,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'exists': True
            }
    
    return {'exists': False}

def monitor_logs():
    """监控日志输出"""
    print("📊 ChatMonitor 状态监控")
    print("=" * 50)
    
    while True:
        try:
            # 清屏
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print(f"🕐 监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 50)
            
            # 1. 进程状态
            print("🔍 进程状态:")
            proc = find_chatmonitor_process()
            if proc:
                info = get_process_info(proc)
                if info:
                    print(f"  ✅ 进程运行中 (PID: {info['pid']})")
                    print(f"  📊 CPU使用率: {info['cpu_percent']:.1f}%")
                    print(f"  💾 内存使用: {info['memory_mb']:.1f} MB")
                    print(f"  🕐 启动时间: {info['create_time']}")
                    print(f"  📝 状态: {info['status']}")
                else:
                    print("  ❌ 无法获取进程信息")
            else:
                print("  ❌ ChatMonitor 进程未运行")
            
            print()
            
            # 2. 配置文件状态
            print("📋 配置文件状态:")
            config_info = check_config_file()
            if config_info['exists']:
                print(f"  ✅ 配置文件存在: {config_info['path']}")
                print(f"  📏 文件大小: {config_info['size']} 字节")
                print(f"  🕐 最后修改: {config_info['modified']}")
            else:
                print("  ❌ 配置文件不存在")
            
            print()
            
            # 3. 权限状态
            print("🔐 权限状态:")
            try:
                # 检查屏幕录制权限
                result = subprocess.run([
                    'sqlite3', '/Library/Application Support/com.apple.TCC/TCC.db',
                    "SELECT client FROM access WHERE service='kTCCServiceScreenCapture' AND client='com.chatmonitor.app';"
                ], capture_output=True, text=True)
                if result.stdout.strip():
                    print("  ✅ 屏幕录制权限: 已授权")
                else:
                    print("  ❌ 屏幕录制权限: 未授权")
            except:
                print("  ⚠️  屏幕录制权限: 无法检查")
            
            try:
                # 检查辅助功能权限
                result = subprocess.run([
                    'sqlite3', '/Library/Application Support/com.apple.TCC/TCC.db',
                    "SELECT client FROM access WHERE service='kTCCServiceAccessibility' AND client='com.chatmonitor.app';"
                ], capture_output=True, text=True)
                if result.stdout.strip():
                    print("  ✅ 辅助功能权限: 已授权")
                else:
                    print("  ❌ 辅助功能权限: 未授权")
            except:
                print("  ⚠️  辅助功能权限: 无法检查")
            
            print()
            
            # 4. 系统资源
            print("💻 系统资源:")
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            print(f"  🖥️  CPU使用率: {cpu_percent:.1f}%")
            print(f"  💾 内存使用: {memory.percent:.1f}% ({memory.used // 1024 // 1024} MB / {memory.total // 1024 // 1024} MB)")
            
            print()
            
            # 5. 操作提示
            print("🎮 操作提示:")
            print("  📝 修改配置文件: open ~/ChatMonitor/config_with_yolo.yaml")
            print("  🔧 权限管理: ./manage_permissions.sh")
            print("  🚀 启动应用: open ./release/ChatMonitor.app")
            print("  ⏹️  停止监控: Ctrl+C")
            
            print()
            print("🔄 5秒后刷新...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
            break
        except Exception as e:
            print(f"❌ 监控出错: {e}")
            time.sleep(5)

def check_detection_status():
    """检查检测状态"""
    print("🔍 检测状态检查")
    print("=" * 30)
    
    # 检查目标应用是否运行
    target_apps = ["WeChat", "QQ", "钉钉", "企业微信", "Mango"]
    for app in target_apps:
        for proc in psutil.process_iter(['name']):
            try:
                if app.lower() in proc.info['name'].lower():
                    print(f"✅ {app} 正在运行")
                    break
            except:
                pass
        else:
            print(f"❌ {app} 未运行")
    
    print()
    print("📋 检测配置:")
    config_info = check_config_file()
    if config_info['exists']:
        try:
            import yaml
            with open(config_info['path'], 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            target_contacts = config.get('chat_app', {}).get('target_contacts', [])
            print(f"🎯 目标联系人: {target_contacts}")
            
            check_interval = config.get('monitor', {}).get('check_interval', 30)
            print(f"⏱️  检测间隔: {check_interval} 秒")
            
            yolo_enabled = config.get('yolo', {}).get('enabled', True)
            print(f"🤖 YOLO检测: {'启用' if yolo_enabled else '禁用'}")
            
        except Exception as e:
            print(f"❌ 读取配置失败: {e}")
    else:
        print("❌ 配置文件不存在")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "detection":
            check_detection_status()
        else:
            print("用法: python status_monitor.py [detection]")
            print("  detection: 检查检测状态")
            print("  无参数: 启动实时监控")
    else:
        monitor_logs() 