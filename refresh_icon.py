#!/usr/bin/env python3
"""
图标刷新脚本
强制重新加载图标，解决缓存问题
"""

import os
import time
import subprocess

def refresh_icon():
    """刷新图标"""
    print("🔄 开始刷新图标...")
    
    # 1. 停止所有相关进程
    print("  📋 停止相关进程...")
    subprocess.run(["pkill", "-f", "python3 main_monitor_gui_app.py"], 
                   capture_output=True)
    
    # 2. 清理缓存
    print("  🧹 清理缓存...")
    subprocess.run(["sudo", "rm", "-rf", "/Library/Caches/com.apple.iconservices.store"], 
                   capture_output=True)
    subprocess.run(["sudo", "killall", "Dock"], capture_output=True)
    
    # 3. 确保使用最新图标
    print("  📁 更新图标文件...")
    if os.path.exists("icon_256x256.png"):
        subprocess.run(["cp", "icon_256x256.png", "icon.png"])
        print("    ✅ 已复制最新图标到 icon.png")
    
    # 4. 清空调试日志
    print("  📝 清空调试日志...")
    subprocess.run(["echo", '""', ">", "/tmp/chatmonitor_debug.log"], 
                   shell=True)
    
    print("✅ 图标刷新完成！")
    print("💡 现在可以重新运行应用了")

if __name__ == "__main__":
    refresh_icon() 