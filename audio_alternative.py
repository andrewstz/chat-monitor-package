#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
替代的音频播放解决方案
当playsound不可用时使用系统命令播放音频
"""

import os
import platform
import subprocess
import sys

def play_sound_alternative(sound_type="normal"):
    """
    使用系统命令播放音频的替代方案
    
    Args:
        sound_type (str): 音频类型 ("normal", "contact", "error")
    """
    try:
        # 确定音频文件路径
        sound_file = None
        if sound_type == "contact":
            sound_file = "sounds/contact_alert_pitch_speed_volume.wav"
        elif sound_type == "error":
            sound_file = "error_alert_pitch_speed_volume.wav"
        else:
            sound_file = "sounds/normal_tip_pitch_speed_volume.wav"
        
        # 检查文件是否存在
        if not os.path.exists(sound_file):
            print(f"WARNING: Sound file not found: {sound_file}")
            return False
        
        # 根据操作系统选择播放命令
        system = platform.system()
        
        if system == "Windows":
            # Windows使用PowerShell播放音频
            try:
                subprocess.run([
                    "powershell", 
                    "-Command", 
                    f"(New-Object Media.SoundPlayer '{sound_file}').PlaySync()"
                ], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                # 备用方案：使用start命令
                try:
                    subprocess.run([
                        "start", 
                        "/min", 
                        "wmplayer", 
                        sound_file
                    ], shell=True, check=True)
                    return True
                except subprocess.CalledProcessError:
                    print(f"ERROR: Failed to play sound on Windows: {sound_file}")
                    return False
                    
        elif system == "Darwin":  # macOS
            # macOS使用afplay命令
            try:
                subprocess.run(["afplay", sound_file], check=True)
                return True
            except subprocess.CalledProcessError:
                print(f"ERROR: Failed to play sound on macOS: {sound_file}")
                return False
                
        elif system == "Linux":
            # Linux使用aplay或paplay命令
            for cmd in ["aplay", "paplay"]:
                try:
                    subprocess.run([cmd, sound_file], check=True)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            print(f"ERROR: Failed to play sound on Linux: {sound_file}")
            return False
            
        else:
            print(f"WARNING: Unknown operating system: {system}")
            return False
            
    except Exception as e:
        print(f"ERROR: Audio playback failed: {e}")
        return False

def test_audio_system():
    """测试音频系统是否可用"""
    print("Testing audio system...")
    
    # 测试系统命令
    system = platform.system()
    print(f"Operating system: {system}")
    
    if system == "Windows":
        # 测试PowerShell
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Write-Host 'PowerShell available'"],
                capture_output=True, text=True, check=True
            )
            print("✅ PowerShell available")
        except:
            print("❌ PowerShell not available")
            
    elif system == "Darwin":
        # 测试afplay
        try:
            result = subprocess.run(["afplay", "--help"], capture_output=True)
            print("✅ afplay available")
        except:
            print("❌ afplay not available")
            
    elif system == "Linux":
        # 测试音频命令
        for cmd in ["aplay", "paplay"]:
            try:
                result = subprocess.run([cmd, "--help"], capture_output=True)
                print(f"✅ {cmd} available")
                break
            except:
                continue
        else:
            print("❌ No audio command available")
    
    # 测试音频文件
    sound_files = [
        "sounds/normal_tip_pitch_speed_volume.wav",
        "sounds/contact_alert_pitch_speed_volume.wav", 
        "sounds/error_alert_pitch_speed_volume.wav"
    ]
    
    for sound_file in sound_files:
        if os.path.exists(sound_file):
            print(f"✅ Sound file exists: {sound_file}")
        else:
            print(f"❌ Sound file missing: {sound_file}")

if __name__ == "__main__":
    test_audio_system() 