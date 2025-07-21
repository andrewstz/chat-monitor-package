#!/usr/bin/env python3
"""
声音播放测试脚本
用于诊断声音播放问题
"""

import subprocess
import os
import platform
import time

def test_afplay():
    """测试afplay命令"""
    print("🔊 测试afplay命令...")
    
    sound_file = "sounds/contact_alert_pitch_speed_volume.wav"
    
    if not os.path.exists(sound_file):
        print(f"❌ 音频文件不存在: {sound_file}")
        return False
    
    print(f"✅ 音频文件存在: {sound_file}")
    print(f"📊 文件大小: {os.path.getsize(sound_file)} 字节")
    
    try:
        print("🔊 开始播放音频...")
        result = subprocess.run(['afplay', sound_file], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ afplay播放成功")
            return True
        else:
            print(f"❌ afplay播放失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ afplay播放超时")
        return False
    except Exception as e:
        print(f"❌ afplay播放异常: {e}")
        return False

def test_system_volume():
    """测试系统音量"""
    print("\n🔊 测试系统音量...")
    
    try:
        # 获取当前音量
        result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            volume = result.stdout.strip()
            print(f"📊 当前系统音量: {volume}")
            
            if volume == "0":
                print("⚠️  系统音量为0，请调高音量")
                return False
            else:
                print("✅ 系统音量正常")
                return True
        else:
            print("❌ 无法获取系统音量")
            return False
            
    except Exception as e:
        print(f"❌ 音量检测异常: {e}")
        return False

def test_audio_permissions():
    """测试音频权限"""
    print("\n🔊 测试音频权限...")
    
    try:
        # 检查是否有音频输出设备
        result = subprocess.run(['system_profiler', 'SPAudioDataType'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "Output" in result.stdout:
                print("✅ 检测到音频输出设备")
                return True
            else:
                print("❌ 未检测到音频输出设备")
                return False
        else:
            print("❌ 无法检测音频设备")
            return False
            
    except Exception as e:
        print(f"❌ 音频权限检测异常: {e}")
        return False

def test_audio_file_format():
    """测试音频文件格式"""
    print("\n🔊 测试音频文件格式...")
    
    sound_file = "sounds/contact_alert_pitch_speed_volume.wav"
    
    try:
        # 使用file命令检查文件类型
        result = subprocess.run(['file', sound_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"📊 文件类型: {result.stdout.strip()}")
            
            # 检查是否是有效的音频文件
            if "Audio" in result.stdout or "WAVE" in result.stdout:
                print("✅ 音频文件格式正确")
                return True
            else:
                print("❌ 音频文件格式可能有问题")
                return False
        else:
            print("❌ 无法检测文件类型")
            return False
            
    except Exception as e:
        print(f"❌ 文件格式检测异常: {e}")
        return False

def main():
    print("🔧 声音播放诊断工具")
    print("=" * 50)
    
    # 检查系统
    system = platform.system()
    print(f"🖥️  操作系统: {system}")
    
    if system != "Darwin":
        print("❌ 此脚本仅适用于macOS")
        return
    
    # 运行各项测试
    tests = [
        ("音频文件格式", test_audio_file_format),
        ("音频权限", test_audio_permissions),
        ("系统音量", test_system_volume),
        ("afplay播放", test_afplay),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # 总结结果
    print(f"\n{'='*50}")
    print("📊 测试结果总结:")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    # 建议
    print(f"\n💡 建议:")
    if not any(result for _, result in results):
        print("- 所有测试都失败，请检查系统音频设置")
    elif not results[-1][1]:  # afplay测试失败
        print("- afplay播放失败，请检查音频文件和系统设置")
    elif not results[2][1]:  # 系统音量测试失败
        print("- 系统音量为0，请调高音量")
    else:
        print("- 所有测试通过，声音播放应该正常工作")

if __name__ == "__main__":
    main() 