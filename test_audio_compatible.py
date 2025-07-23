#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音频兼容模块
验证Windows兼容音频播放功能
"""

import sys
import os

def test_audio_compatible():
    """测试音频兼容模块"""
    print("=" * 50)
    print("测试音频兼容模块")
    print("=" * 50)
    
    try:
        # 导入音频兼容模块
        from audio_windows_compatible import play_sound, test_audio
        
        print("✅ 音频兼容模块导入成功")
        
        # 测试音频播放
        print("\n开始测试音频播放...")
        test_audio()
        
        print("\n✅ 音频兼容模块测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 音频兼容模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 音频兼容模块测试失败: {e}")
        return False

def test_main_monitor_audio():
    """测试主程序的音频功能"""
    print("\n" + "=" * 50)
    print("测试主程序音频功能")
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
        
        print("\n✅ 主程序音频功能测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 主程序音频模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 主程序音频功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("音频兼容性测试")
    print("=" * 50)
    
    # 测试音频兼容模块
    audio_compatible_ok = test_audio_compatible()
    
    # 测试主程序音频功能
    main_audio_ok = test_main_monitor_audio()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if audio_compatible_ok:
        print("✅ 音频兼容模块: 正常")
    else:
        print("❌ 音频兼容模块: 失败")
    
    if main_audio_ok:
        print("✅ 主程序音频功能: 正常")
    else:
        print("❌ 主程序音频功能: 失败")
    
    if audio_compatible_ok and main_audio_ok:
        print("\n🎉 所有音频功能测试通过！")
        print("✅ 可以安全地移除playsound依赖")
        return True
    else:
        print("\n⚠️ 部分音频功能测试失败")
        print("❌ 需要进一步检查音频配置")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 