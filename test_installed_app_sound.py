#!/usr/bin/env python3
"""
测试安装的应用程序声音播放
"""

import subprocess
import os
import sys

def test_installed_app_sound():
    """测试从安装的应用程序播放声音"""
    print("🔊 测试安装的应用程序声音播放...")
    
    # 检查安装的应用程序
    app_path = "/Applications/ChatMonitor.app"
    if not os.path.exists(app_path):
        print(f"❌ 应用程序不存在: {app_path}")
        return False
    
    print(f"✅ 应用程序存在: {app_path}")
    
    # 检查音频文件
    sound_file = "/Applications/ChatMonitor.app/Contents/Resources/sounds/contact_alert_pitch_speed_volume.wav"
    if not os.path.exists(sound_file):
        print(f"❌ 音频文件不存在: {sound_file}")
        return False
    
    print(f"✅ 音频文件存在: {sound_file}")
    print(f"📊 文件大小: {os.path.getsize(sound_file)} 字节")
    
    # 测试从应用程序目录播放
    try:
        print("🔊 从应用程序目录播放音频...")
        result = subprocess.run(['afplay', sound_file], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ 从应用程序目录播放成功")
            return True
        else:
            print(f"❌ 从应用程序目录播放失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 播放超时")
        return False
    except Exception as e:
        print(f"❌ 播放异常: {e}")
        return False

def test_app_permissions():
    """测试应用程序权限"""
    print("\n🔊 测试应用程序权限...")
    
    try:
        # 检查应用程序是否有音频权限
        result = subprocess.run(['osascript', '-e', 'tell application "ChatMonitor" to activate'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ 应用程序可以激活")
        else:
            print(f"⚠️  应用程序激活失败: {result.stderr}")
        
        # 检查系统音频权限
        result = subprocess.run(['osascript', '-e', 'tell application "System Events" to get properties'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ 系统事件权限正常")
        else:
            print(f"⚠️  系统事件权限可能有问题: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 权限检测异常: {e}")
        return False
    
    return True

def test_audio_output():
    """测试音频输出"""
    print("\n🔊 测试音频输出...")
    
    try:
        # 使用系统声音测试
        result = subprocess.run(['osascript', '-e', 'beep'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ 系统声音测试成功")
            return True
        else:
            print(f"❌ 系统声音测试失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 音频输出测试异常: {e}")
        return False

def main():
    print("🔧 安装的应用程序声音播放测试")
    print("=" * 50)
    
    # 运行测试
    tests = [
        ("应用程序权限", test_app_permissions),
        ("音频输出", test_audio_output),
        ("应用程序声音播放", test_installed_app_sound),
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
        print("- 所有测试都失败，请检查应用程序权限设置")
        print("- 在系统偏好设置 > 安全性与隐私 > 隐私中检查ChatMonitor的权限")
    elif not results[-1][1]:  # 应用程序声音播放测试失败
        print("- 应用程序声音播放失败，请检查音频权限")
        print("- 尝试重新安装应用程序")
    else:
        print("- 所有测试通过，声音播放应该正常工作")

if __name__ == "__main__":
    main() 