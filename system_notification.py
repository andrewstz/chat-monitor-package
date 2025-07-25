#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统声音通知模块
支持跨平台的系统声音播放和通知
"""

import os
import sys
import subprocess
import platform
from datetime import datetime

class SystemNotification:
    def __init__(self):
        self.platform = platform.system().lower()
        self.sound_enabled = True
        
    def log_message(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # 写入日志文件
        try:
            with open("/tmp/chatmonitor_notification.log", "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"写入日志失败: {e}")
    
    def play_system_sound(self, sound_type="default"):
        """播放系统声音"""
        if not self.sound_enabled:
            return False
            
        try:
            if self.platform == "darwin":  # macOS
                return self._play_macos_sound(sound_type)
            elif self.platform == "linux":
                return self._play_linux_sound(sound_type)
            elif self.platform == "windows":
                return self._play_windows_sound(sound_type)
            else:
                self.log_message(f"⚠️ 不支持的操作系统: {self.platform}")
                return False
        except Exception as e:
            self.log_message(f"❌ 播放系统声音失败: {e}")
            return False
    
    def _play_macos_sound(self, sound_type):
        """播放 macOS 系统声音"""
        sound_files = {
            "default": "/System/Library/Sounds/Ping.aiff",
            "alert": "/System/Library/Sounds/Basso.aiff",
            "warning": "/System/Library/Sounds/Sosumi.aiff",
            "success": "/System/Library/Sounds/Glass.aiff",
            "error": "/System/Library/Sounds/Basso.aiff",
            "notification": "/System/Library/Sounds/Ping.aiff"
        }
        
        sound_file = sound_files.get(sound_type, sound_files["default"])
        
        try:
            result = subprocess.run(
                ["afplay", sound_file],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                self.log_message(f"✅ 播放 macOS 声音: {sound_type}")
                return True
            else:
                self.log_message(f"❌ macOS 声音播放失败: {result.stderr.decode()}")
                return False
        except subprocess.TimeoutExpired:
            self.log_message("❌ macOS 声音播放超时")
            return False
        except Exception as e:
            self.log_message(f"❌ macOS 声音播放异常: {e}")
            return False
    
    def _play_linux_sound(self, sound_type):
        """播放 Linux 系统声音"""
        # 尝试不同的音频播放器
        players = [
            ("paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"),
            ("aplay", "/usr/share/sounds/alsa/Front_Center.wav"),
            ("mpg123", "/usr/share/sounds/notification.mp3")
        ]
        
        for player, sound_file in players:
            try:
                result = subprocess.run(
                    [player, sound_file],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    self.log_message(f"✅ 播放 Linux 声音: {sound_type} (使用 {player})")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
            except Exception as e:
                self.log_message(f"❌ Linux 声音播放异常 ({player}): {e}")
                continue
        
        self.log_message("❌ 所有 Linux 音频播放器都失败")
        return False
    
    def _play_windows_sound(self, sound_type):
        """播放 Windows 系统声音"""
        try:
            import winsound
            
            sound_types = {
                "default": winsound.MB_ICONASTERISK,
                "alert": winsound.MB_ICONEXCLAMATION,
                "warning": winsound.MB_ICONEXCLAMATION,
                "success": winsound.MB_ICONASTERISK,
                "error": winsound.MB_ICONHAND,
                "notification": winsound.MB_ICONASTERISK
            }
            
            sound_type_code = sound_types.get(sound_type, winsound.MB_ICONASTERISK)
            winsound.MessageBeep(sound_type_code)
            
            self.log_message(f"✅ 播放 Windows 声音: {sound_type}")
            return True
            
        except ImportError:
            self.log_message("❌ Windows 缺少 winsound 模块")
            return False
        except Exception as e:
            self.log_message(f"❌ Windows 声音播放异常: {e}")
            return False
    
    def send_desktop_notification(self, title, message, sound_type="default"):
        """发送桌面通知"""
        try:
            if self.platform == "darwin":  # macOS
                return self._send_macos_notification(title, message, sound_type)
            elif self.platform == "linux":
                return self._send_linux_notification(title, message, sound_type)
            elif self.platform == "windows":
                return self._send_windows_notification(title, message, sound_type)
            else:
                self.log_message(f"⚠️ 不支持的操作系统: {self.platform}")
                return False
        except Exception as e:
            self.log_message(f"❌ 发送桌面通知失败: {e}")
            return False
    
    def _send_macos_notification(self, title, message, sound_type):
        """发送 macOS 桌面通知"""
        try:
            # 使用 osascript 发送通知
            script = f'''
            display notification "{message}" with title "{title}" sound name "{sound_type}"
            '''
            
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.log_message(f"✅ 发送 macOS 通知: {title}")
                return True
            else:
                self.log_message(f"❌ macOS 通知发送失败: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ macOS 通知异常: {e}")
            return False
    
    def _send_linux_notification(self, title, message, sound_type):
        """发送 Linux 桌面通知"""
        try:
            # 尝试使用 notify-send
            cmd = ["notify-send", title, message, "--urgency=normal"]
            
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            
            if result.returncode == 0:
                self.log_message(f"✅ 发送 Linux 通知: {title}")
                return True
            else:
                self.log_message(f"❌ Linux 通知发送失败: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Linux 通知异常: {e}")
            return False
    
    def _send_windows_notification(self, title, message, sound_type):
        """发送 Windows 桌面通知"""
        try:
            # 使用 PowerShell 发送通知
            script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $notification = New-Object System.Windows.Forms.NotifyIcon
            $notification.Icon = [System.Drawing.SystemIcons]::Information
            $notification.BalloonTipTitle = "{title}"
            $notification.BalloonTipText = "{message}"
            $notification.Visible = $true
            $notification.ShowBalloonTip(5000)
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", script],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.log_message(f"✅ 发送 Windows 通知: {title}")
                return True
            else:
                self.log_message(f"❌ Windows 通知发送失败: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Windows 通知异常: {e}")
            return False
    
    def test_system_sounds(self):
        """测试系统声音"""
        print("🧪 测试系统声音功能")
        print(f"📊 当前平台: {self.platform}")
        
        test_sounds = ["default", "alert", "warning", "success", "error"]
        
        for sound in test_sounds:
            print(f"🔊 测试声音: {sound}")
            success = self.play_system_sound(sound)
            print(f"  结果: {'✅ 成功' if success else '❌ 失败'}")
            time.sleep(1)  # 等待1秒
        
        print("🎉 系统声音测试完成")

def main():
    """主函数 - 测试系统通知功能"""
    print("🚀 系统通知模块测试")
    print("=" * 40)
    
    notification = SystemNotification()
    
    # 测试系统声音
    notification.test_system_sounds()
    
    # 测试桌面通知
    print("\n📱 测试桌面通知...")
    notification.send_desktop_notification(
        "ChatMonitor 测试", 
        "这是一条测试通知消息"
    )

if __name__ == "__main__":
    import time
    main() 