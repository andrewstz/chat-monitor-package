#!/usr/bin/env python3
"""
带图标的应用打包脚本
使用 PyInstaller 打包应用并设置图标
"""

import os
import subprocess
import sys

def check_requirements():
    """检查打包要求"""
    print("🔍 检查打包要求...")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print("  ✅ PyInstaller 已安装")
    except ImportError:
        print("  ❌ PyInstaller 未安装")
        print("  💡 请运行: pip install pyinstaller")
        return False
    
    # 检查图标文件
    icon_files = ["icon.icns", "assets/icon.icns", "icons/icon.icns"]
    icon_found = False
    
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            print(f"  ✅ 找到图标文件: {icon_file}")
            icon_found = True
            break
    
    if not icon_found:
        print("  ⚠️  未找到图标文件")
        print("  💡 请先运行: python3 create_icon.py")
    
    return True

def build_app():
    """打包应用"""
    print("🚀 开始打包应用...")
    
    # 查找图标文件
    icon_file = None
    icon_candidates = ["icon.icns", "assets/icon.icns", "icons/icon.icns"]
    
    for candidate in icon_candidates:
        if os.path.exists(candidate):
            icon_file = candidate
            break
    
    # 构建 PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 无控制台窗口
        "--name=ChatMonitor",  # 应用名称
        "--distpath=dist",  # 输出目录
        "--workpath=build",  # 工作目录
        "--specpath=build",  # spec文件目录
        "--clean",  # 清理临时文件
    ]
    
    # 添加图标
    if icon_file:
        cmd.extend(["--icon", icon_file])
        print(f"  📋 使用图标: {icon_file}")
    else:
        print("  ⚠️  未找到图标文件，使用默认图标")
    
    # 添加数据文件
    cmd.extend([
        "--add-data", "sounds:sounds",  # 音频文件
        "--add-data", "models:models",  # 模型文件
    ])
    
    # 添加主程序
    cmd.append("main_monitor_gui_app.py")
    
    print(f"  📋 执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 应用打包成功！")
        print(f"📁 输出目录: dist/ChatMonitor")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_app_bundle():
    """创建 macOS .app 包"""
    print("📦 创建 macOS .app 包...")
    
    app_name = "ChatMonitor.app"
    app_path = f"dist/{app_name}"
    
    # 检查是否已存在
    if os.path.exists(app_path):
        print(f"  🗑️  删除现有应用包: {app_path}")
        subprocess.run(["rm", "-rf", app_path])
    
    try:
        # 创建 .app 包结构
        subprocess.run([
            "mkdir", "-p", 
            f"{app_path}/Contents/MacOS",
            f"{app_path}/Contents/Resources"
        ], check=True)
        
        # 复制可执行文件
        subprocess.run([
            "cp", "dist/ChatMonitor", f"{app_path}/Contents/MacOS/ChatMonitor"
        ], check=True)
        
        # 复制图标文件
        icon_file = None
        for candidate in ["icon.icns", "assets/icon.icns", "icons/icon.icns"]:
            if os.path.exists(candidate):
                icon_file = candidate
                break
        
        if icon_file:
            subprocess.run([
                "cp", icon_file, f"{app_path}/Contents/Resources/icon.icns"
            ], check=True)
            print(f"  ✅ 复制图标: {icon_file}")
        
        # 创建 Info.plist
        info_plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ChatMonitor</string>
    <key>CFBundleIdentifier</key>
    <string>com.chatmonitor.app</string>
    <key>CFBundleName</key>
    <string>ChatMonitor</string>
    <key>CFBundleDisplayName</key>
    <string>ChatMonitor</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>'''
        
        with open(f"{app_path}/Contents/Info.plist", "w") as f:
            f.write(info_plist_content)
        
        print(f"  ✅ 创建 Info.plist")
        
        # 设置权限
        subprocess.run(["chmod", "+x", f"{app_path}/Contents/MacOS/ChatMonitor"])
        
        print(f"✅ 成功创建应用包: {app_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建应用包失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 ChatMonitor 应用打包工具")
    print("=" * 50)
    
    # 检查要求
    if not check_requirements():
        return
    
    # 打包应用
    if not build_app():
        return
    
    # 创建应用包
    if not create_app_bundle():
        return
    
    print("\n🎉 打包完成！")
    print("📋 输出文件:")
    print("  📁 dist/ChatMonitor (可执行文件)")
    print("  📦 dist/ChatMonitor.app (macOS 应用包)")
    print("\n💡 使用说明:")
    print("  1. 双击 ChatMonitor.app 运行应用")
    print("  2. 或运行 ./dist/ChatMonitor")
    print("  3. 应用会自动设置图标")

if __name__ == "__main__":
    main() 