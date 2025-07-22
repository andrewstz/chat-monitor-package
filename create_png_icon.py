#!/usr/bin/env python3
"""
创建 PNG 格式的应用图标
生成适合 Tkinter iconphoto 的 PNG 图标
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_png_icon():
    """创建 PNG 格式的图标"""
    print("🎨 创建 PNG 格式图标...")
    
    # 创建不同尺寸的图标
    sizes = [16, 32, 64, 128, 256]
    
    for size in sizes:
        # 创建图像
        img = Image.new('RGBA', (size, size), (52, 152, 219, 255))  # 蓝色背景
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        try:
            # 尝试使用系统字体
            font_size = max(size // 4, 12)
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
        
        # 绘制文字
        text = "CM"  # ChatMonitor 缩写
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # 保存图标到 assets/icons 目录
        icon_path = f"assets/icons/icon_{size}x{size}.png"
        img.save(icon_path)
        print(f"  ✅ 创建 {size}x{size} PNG 图标: {icon_path}")
    
    # 创建默认图标（使用最大尺寸）
    default_icon = f"assets/icons/icon_{sizes[-1]}x{sizes[-1]}.png"
    if os.path.exists(default_icon):
        # 复制为默认图标名
        import shutil
        shutil.copy2(default_icon, "assets/icons/icon.png")
        print(f"  ✅ 创建默认图标: assets/icons/icon.png")
    
    print("✅ PNG 图标创建完成！")

def create_assets_directory():
    """创建资源目录"""
    print("📁 创建资源目录...")
    
    directories = ["assets", "icons"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  ✅ 创建目录: {directory}")
        else:
            print(f"  📋 目录已存在: {directory}")

def main():
    """主函数"""
    print("🚀 开始创建 PNG 图标...")
    
    # 创建资源目录
    create_assets_directory()
    
    # 创建 PNG 图标
    create_png_icon()
    
    print("\n📋 PNG 图标创建完成！")
    print("💡 使用说明:")
    print("  1. 图标文件: icon.png, icon_256x256.png 等")
    print("  2. 程序会自动查找 PNG 图标文件")
    print("  3. 支持多种路径: 当前目录、assets/、icons/")
    print("  4. 使用 iconphoto 方法设置图标")

if __name__ == "__main__":
    main() 