#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows音频播放模块 - 修复版本
解决Windows下音频播放问题
"""

import platform
import subprocess
import os
import sys

def play_sound_windows(sound_type="default"):
    """Windows下播放音频"""
    try:
        system = platform.system()
        
        if system != "Windows":
            print(f"⚠️ 当前不是Windows系统: {system}")
            return False
        
        # 音频文件映射
        sound_files = {
            "default": "sounds/default.wav",
            "contact": "sounds/contact_alert_pitch_speed_volume.wav",
            "error": "sounds/error_alert_pitch_speed_volume.wav",
            "normal": "sounds/normal_tip_pitch_speed_volume.wav"
        }
        
        # 获取音频文件路径
        sound_file = sound_files.get(sound_type, sound_files["default"])
        
        # 检查文件是否存在
        if not os.path.exists(sound_file):
            print(f"❌ 音频文件不存在: {sound_file}")
            return False
        
        # 使用PowerShell播放音频
        try:
            # 方法1: 使用PowerShell的Media.SoundPlayer
            ps_command = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $player = New-Object System.Media.SoundPlayer
            $player.SoundLocation = "{os.path.abspath(sound_file)}"
            $player.Play()
            Start-Sleep -Milliseconds 1000
            $player.Stop()
            $player.Dispose()
            '''
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ Windows音频播放成功: {sound_type}")
                return True
            else:
                print(f"⚠️ PowerShell播放失败: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⚠️ PowerShell播放超时")
        except Exception as e:
            print(f"⚠️ PowerShell播放异常: {e}")
        
        # 方法2: 使用Windows Media Player COM对象
        try:
            ps_command = f'''
            $player = New-Object System.Media.SoundPlayer
            $player.SoundLocation = "{os.path.abspath(sound_file)}"
            $player.Play()
            Start-Sleep -Seconds 2
            $player.Stop()
            $player.Dispose()
            '''
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ Windows音频播放成功(方法2): {sound_type}")
                return True
            else:
                print(f"⚠️ 方法2播放失败: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ 方法2播放异常: {e}")
        
        # 方法3: 使用系统提示音
        try:
            ps_command = '''
            [System.Console]::Beep(800, 500)
            Start-Sleep -Milliseconds 100
            [System.Console]::Beep(1000, 500)
            '''
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"✅ Windows系统提示音播放成功: {sound_type}")
                return True
            else:
                print(f"⚠️ 系统提示音失败: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ 系统提示音异常: {e}")
        
        print(f"❌ 所有Windows音频播放方法都失败了: {sound_type}")
        return False
        
    except Exception as e:
        print(f"❌ Windows音频播放异常: {e}")
        return False

def play_sound_macos(sound_type="default"):
    """macOS下播放音频"""
    try:
        system = platform.system()
        
        if system != "Darwin":
            print(f"⚠️ 当前不是macOS系统: {system}")
            return False
        
        # 音频文件映射
        sound_files = {
            "default": "sounds/default.wav",
            "contact": "sounds/contact_alert_pitch_speed_volume.wav",
            "error": "sounds/error_alert_pitch_speed_volume.wav",
            "normal": "sounds/normal_tip_pitch_speed_volume.wav"
        }
        
        # 获取音频文件路径
        sound_file = sound_files.get(sound_type, sound_files["default"])
        
        # 检查文件是否存在
        if not os.path.exists(sound_file):
            print(f"❌ 音频文件不存在: {sound_file}")
            return False
        
        # 使用afplay播放音频
        result = subprocess.run(
            ['afplay', sound_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✅ macOS音频播放成功: {sound_type}")
            return True
        else:
            print(f"❌ macOS音频播放失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ macOS音频播放异常: {e}")
        return False

def play_sound_linux(sound_type="default"):
    """Linux下播放音频"""
    try:
        system = platform.system()
        
        if system != "Linux":
            print(f"⚠️ 当前不是Linux系统: {system}")
            return False
        
        # 音频文件映射
        sound_files = {
            "default": "sounds/default.wav",
            "contact": "sounds/contact_alert_pitch_speed_volume.wav",
            "error": "sounds/error_alert_pitch_speed_volume.wav",
            "normal": "sounds/normal_tip_pitch_speed_volume.wav"
        }
        
        # 获取音频文件路径
        sound_file = sound_files.get(sound_type, sound_files["default"])
        
        # 检查文件是否存在
        if not os.path.exists(sound_file):
            print(f"❌ 音频文件不存在: {sound_file}")
            return False
        
        # 尝试不同的音频播放器
        players = ['paplay', 'aplay', 'mpg123', 'ffplay']
        
        for player in players:
            try:
                result = subprocess.run(
                    [player, sound_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    print(f"✅ Linux音频播放成功({player}): {sound_type}")
                    return True
                else:
                    print(f"⚠️ {player}播放失败: {result.stderr}")
                    
            except FileNotFoundError:
                print(f"⚠️ {player}未安装")
            except Exception as e:
                print(f"⚠️ {player}播放异常: {e}")
        
        print(f"❌ 所有Linux音频播放器都失败了: {sound_type}")
        return False
        
    except Exception as e:
        print(f"❌ Linux音频播放异常: {e}")
        return False

def play_sound(sound_type="default"):
    """跨平台音频播放函数"""
    system = platform.system()
    
    if system == "Windows":
        return play_sound_windows(sound_type)
    elif system == "Darwin":
        return play_sound_macos(sound_type)
    elif system == "Linux":
        return play_sound_linux(sound_type)
    else:
        print(f"⚠️ 不支持的系统: {system}")
        return False

def test_audio_playback():
    """测试音频播放功能"""
    print("=== 音频播放测试 ===")
    
    system = platform.system()
    print(f"当前系统: {system}")
    
    # 测试不同音频类型
    audio_types = ["default", "contact", "error", "normal"]
    
    for audio_type in audio_types:
        print(f"\n测试音频类型: {audio_type}")
        success = play_sound(audio_type)
        if success:
            print(f"✅ {audio_type} 播放成功")
        else:
            print(f"❌ {audio_type} 播放失败")

if __name__ == "__main__":
    test_audio_playback() 