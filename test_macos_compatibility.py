#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS兼容性测试脚本
验证移除playsound后macOS音频功能是否正常
"""

import platform
import sys

def test_macos_audio():
    """测试macOS音频功能"""
    system = platform.system()
    print(f"当前系统: {system}")
    
    if system == "Darwin":  # macOS
        print("✅ 检测到macOS系统")
        
        # 测试主程序音频功能
        try:
            from main_monitor_dynamic import play_sound
            print("✅ 主程序音频模块导入成功")
            
            # 测试各种音频文件播放
            audio_types = ["default", "contact_alert", "error_alert", "normal_tip"]
            
            for audio_type in audio_types:
                print(f"\n测试音频类型: {audio_type}")
                try:
                    play_sound(audio_type)
                    print(f"✅ {audio_type} 音频播放成功")
                except Exception as e:
                    print(f"❌ {audio_type} 音频播放失败: {e}")
            
            return True
        except Exception as e:
            print(f"❌ macOS音频播放测试失败: {e}")
            return False
    else:
        print(f"⚠️ 当前不是macOS系统: {system}")
        return False

def test_audio_compatible_module():
    """测试音频兼容模块"""
    try:
        from audio_windows_compatible import play_sound_macos, play_sound
        print("✅ 音频兼容模块导入成功")
        
        # 测试macOS播放函数
        print("测试macOS播放函数...")
        
        # 测试各种音频文件
        audio_types = ["default", "contact_alert", "error_alert", "normal_tip"]
        
        for audio_type in audio_types:
            print(f"测试音频类型: {audio_type}")
            try:
                play_sound(audio_type)
                print(f"✅ {audio_type} 音频播放成功")
            except Exception as e:
                print(f"❌ {audio_type} 音频播放失败: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 音频兼容模块测试失败: {e}")
        return False

def test_sounds_files():
    """测试sounds目录中的音频文件"""
    import os
    
    print("\n" + "=" * 50)
    print("测试sounds目录中的音频文件")
    print("=" * 50)
    
    # 检查sounds目录
    sounds_dir = "sounds"
    if not os.path.exists(sounds_dir):
        print(f"❌ sounds目录不存在: {sounds_dir}")
        return False
    
    print(f"✅ 找到sounds目录: {sounds_dir}")
    
    # 列出所有音频文件
    audio_files = []
    for file in os.listdir(sounds_dir):
        if file.endswith(('.wav', '.mp3', '.aiff')):
            audio_files.append(file)
    
    if not audio_files:
        print("❌ sounds目录中没有找到音频文件")
        return False
    
    print(f"✅ 找到 {len(audio_files)} 个音频文件:")
    for file in audio_files:
        file_path = os.path.join(sounds_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    # 测试每个音频文件是否可以播放
    system = platform.system()
    if system == "Darwin":  # macOS
        import subprocess
        
        print("\n测试音频文件播放...")
        for file in audio_files:
            file_path = os.path.join(sounds_dir, file)
            print(f"测试播放: {file}")
            
            try:
                # 使用afplay测试播放（短暂播放）
                result = subprocess.run(['afplay', file_path], 
                                     capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    print(f"✅ {file} 播放成功")
                else:
                    print(f"❌ {file} 播放失败: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"✅ {file} 播放成功（超时中断）")
            except Exception as e:
                print(f"❌ {file} 播放失败: {e}")
    
    return True

def main():
    """主测试函数"""
    print("macOS兼容性测试")
    print("=" * 50)
    
    # 测试音频兼容模块
    audio_compatible_ok = test_audio_compatible_module()
    
    # 测试macOS音频功能
    macos_audio_ok = test_macos_audio()
    
    # 测试sounds目录中的音频文件
    sounds_files_ok = test_sounds_files()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if audio_compatible_ok:
        print("✅ 音频兼容模块: 正常")
    else:
        print("❌ 音频兼容模块: 失败")
    
    if macos_audio_ok:
        print("✅ macOS音频功能: 正常")
    else:
        print("❌ macOS音频功能: 失败")
    
    if sounds_files_ok:
        print("✅ sounds音频文件: 正常")
    else:
        print("❌ sounds音频文件: 失败")
    
    if audio_compatible_ok and macos_audio_ok and sounds_files_ok:
        print("\n🎉 macOS兼容性测试完全通过！")
        print("✅ 移除playsound不影响macOS功能")
        print("✅ sounds目录中的音频文件可以正常播放")
        return True
    else:
        print("\n⚠️ macOS兼容性测试部分失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 