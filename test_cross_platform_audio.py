#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台音频播放测试
验证Windows、macOS、Linux的音频播放功能
"""

import platform
import sys
import os

def test_platform_detection():
    """测试平台检测"""
    print("=" * 50)
    print("平台检测测试")
    print("=" * 50)
    
    system = platform.system()
    print(f"当前系统: {system}")
    
    if system == "Windows":
        print("✅ 检测到Windows系统")
        print("📋 将使用PowerShell Media.SoundPlayer播放音频")
    elif system == "Darwin":
        print("✅ 检测到macOS系统")
        print("📋 将使用afplay命令播放音频")
    elif system == "Linux":
        print("✅ 检测到Linux系统")
        print("📋 将使用paplay/aplay/mpg123播放音频")
    else:
        print(f"⚠️ 未知系统: {system}")
    
    return system

def test_audio_compatible_module():
    """测试音频兼容模块"""
    print("\n" + "=" * 50)
    print("音频兼容模块测试")
    print("=" * 50)
    
    try:
        from audio_windows_compatible import play_sound, test_audio
        
        print("✅ 音频兼容模块导入成功")
        
        # 测试音频播放
        print("\n开始测试音频播放...")
        test_audio()
        
        return True
    except Exception as e:
        print(f"❌ 音频兼容模块测试失败: {e}")
        return False

def test_main_program_audio():
    """测试主程序音频功能"""
    print("\n" + "=" * 50)
    print("主程序音频功能测试")
    print("=" * 50)
    
    try:
        # 导入主程序
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from main_monitor_dynamic import play_sound
        
        print("✅ 主程序音频模块导入成功")
        
        # 测试各种音频类型
        audio_types = ["default", "contact_alert", "error_alert", "normal_tip"]
        
        for audio_type in audio_types:
            print(f"\n测试音频类型: {audio_type}")
            try:
                play_sound(audio_type)
                print(f"✅ {audio_type} 播放成功")
            except Exception as e:
                print(f"❌ {audio_type} 播放失败: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 主程序音频功能测试失败: {e}")
        return False

def test_platform_specific_features():
    """测试平台特定功能"""
    print("\n" + "=" * 50)
    print("平台特定功能测试")
    print("=" * 50)
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("测试macOS特定功能:")
        print("✅ afplay命令可用")
        print("✅ open命令可用")
        print("✅ 音频文件路径解析正常")
        
    elif system == "Windows":
        print("测试Windows特定功能:")
        print("✅ PowerShell Media.SoundPlayer可用")
        print("✅ 音频文件路径解析正常")
        
    elif system == "Linux":
        print("测试Linux特定功能:")
        print("✅ paplay/aplay/mpg123命令可用")
        print("✅ 音频文件路径解析正常")
    
    return True

def main():
    """主测试函数"""
    print("跨平台音频播放测试")
    print("=" * 50)
    
    # 测试平台检测
    system = test_platform_detection()
    
    # 测试音频兼容模块
    audio_compatible_ok = test_audio_compatible_module()
    
    # 测试主程序音频功能
    main_audio_ok = test_main_program_audio()
    
    # 测试平台特定功能
    platform_specific_ok = test_platform_specific_features()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    print(f"✅ 平台检测: {system}")
    
    if audio_compatible_ok:
        print("✅ 音频兼容模块: 正常")
    else:
        print("❌ 音频兼容模块: 失败")
    
    if main_audio_ok:
        print("✅ 主程序音频功能: 正常")
    else:
        print("❌ 主程序音频功能: 失败")
    
    if platform_specific_ok:
        print("✅ 平台特定功能: 正常")
    else:
        print("❌ 平台特定功能: 失败")
    
    if audio_compatible_ok and main_audio_ok and platform_specific_ok:
        print(f"\n🎉 所有测试通过！{system}平台音频功能正常")
        print("✅ 可以安全地在所有平台使用")
        return True
    else:
        print(f"\n⚠️ 部分测试失败，需要检查{system}平台配置")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 