#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows兼容音频播放模块
完全替代playsound，使用系统命令播放音频
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def debug_log(msg):
    """调试日志"""
    try:
        with open("/tmp/chatmonitor_debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] [AUDIO] {msg}\n")
    except Exception:
        pass

def get_resource_path(filename):
    """获取资源文件路径"""
    try:
        # 如果是打包后的应用
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        sound_path = os.path.join(base_path, 'sounds', filename)
        if os.path.exists(sound_path):
            return sound_path
        
        # 尝试相对路径
        sound_path = os.path.join('sounds', filename)
        if os.path.exists(sound_path):
            return sound_path
            
        return None
    except Exception as e:
        debug_log(f"获取资源路径失败: {e}")
        return None

def play_sound_windows(sound_file):
    """Windows系统播放音频"""
    try:
        # 方法1: PowerShell Media.SoundPlayer
        cmd = ['powershell', '-c', f'(New-Object Media.SoundPlayer "{sound_file}").PlaySync()']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            debug_log(f"✅ PowerShell播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ PowerShell播放失败: {e}")
    
    try:
        # 方法2: 使用系统默认播放器
        cmd = ['start', '', sound_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ 系统播放器播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ 系统播放器播放失败: {e}")
    
    try:
        # 方法3: 使用Windows Media Player
        cmd = ['wmplayer', sound_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ WMP播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ WMP播放失败: {e}")
    
    return False

def play_sound_macos(sound_file):
    """macOS系统播放音频"""
    try:
        # 使用afplay播放
        result = subprocess.run(['afplay', sound_file], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ afplay播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ afplay播放失败: {e}")
    
    try:
        # 使用open命令
        result = subprocess.run(['open', sound_file], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ open播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ open播放失败: {e}")
    
    return False

def play_sound_linux(sound_file):
    """Linux系统播放音频"""
    try:
        # 尝试paplay
        result = subprocess.run(['paplay', sound_file], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ paplay播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ paplay播放失败: {e}")
    
    try:
        # 尝试aplay
        result = subprocess.run(['aplay', sound_file], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ aplay播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ aplay播放失败: {e}")
    
    try:
        # 尝试mpg123
        result = subprocess.run(['mpg123', sound_file], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            debug_log(f"✅ mpg123播放成功: {sound_file}")
            return True
    except Exception as e:
        debug_log(f"❌ mpg123播放失败: {e}")
    
    return False

def play_sound(sound_type="default"):
    """播放音频文件（完全替代playsound）"""
    system = platform.system()
    debug_log(f"播放音频: {sound_type}, 系统: {system}")
    
    # 音频文件映射
    sound_files = {
        "default": {
            "Windows": "default.wav",
            "Darwin": "default.wav",  # macOS
            "Linux": "default.wav"
        },
        "contact_alert": {
            "Windows": "contact_alert_pitch_speed_volume.wav",
            "Darwin": "contact_alert_pitch_speed_volume.wav",
            "Linux": "contact_alert_pitch_speed_volume.wav"
        },
        "error_alert": {
            "Windows": "error_alert_pitch_speed_volume.wav",
            "Darwin": "error_alert_pitch_speed_volume.wav",
            "Linux": "error_alert_pitch_speed_volume.wav"
        },
        "normal_tip": {
            "Windows": "normal_tip_pitch_speed_volume.wav",
            "Darwin": "normal_tip_pitch_speed_volume.wav",
            "Linux": "normal_tip_pitch_speed_volume.wav"
        }
    }
    
    try:
        # 获取音频文件名
        sound_file_name = sound_files.get(sound_type, {}).get(system)
        if not sound_file_name:
            debug_log(f"❌ 未找到音频配置: {sound_type}")
            return False
        
        # 获取音频文件路径
        sound_file = get_resource_path(sound_file_name)
        if not sound_file:
            debug_log(f"❌ 未找到音频文件: {sound_file_name}")
            return False
        
        # 根据系统选择播放方法
        if system == "Windows":
            return play_sound_windows(sound_file)
        elif system == "Darwin":
            return play_sound_macos(sound_file)
        elif system == "Linux":
            return play_sound_linux(sound_file)
        else:
            debug_log(f"❌ 不支持的系统: {system}")
            return False
            
    except Exception as e:
        debug_log(f"❌ 音频播放异常: {e}")
        return False

def test_audio():
    """测试音频播放功能"""
    print("测试音频播放功能...")
    
    # 测试默认音频
    print("1. 测试默认音频...")
    if play_sound("default"):
        print("✅ 默认音频播放成功")
    else:
        print("❌ 默认音频播放失败")
    
    # 测试联系人提醒
    print("2. 测试联系人提醒音频...")
    if play_sound("contact_alert"):
        print("✅ 联系人提醒音频播放成功")
    else:
        print("❌ 联系人提醒音频播放失败")
    
    # 测试错误提醒
    print("3. 测试错误提醒音频...")
    if play_sound("error_alert"):
        print("✅ 错误提醒音频播放成功")
    else:
        print("❌ 错误提醒音频播放失败")
    
    # 测试普通提示
    print("4. 测试普通提示音频...")
    if play_sound("normal_tip"):
        print("✅ 普通提示音频播放成功")
    else:
        print("❌ 普通提示音频播放失败")

if __name__ == "__main__":
    test_audio() 