#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试打包后的环境
"""

import os
import sys

def debug_frozen_environment():
    """调试打包后的环境"""
    print("=== 打包环境调试信息 ===")
    print(f"sys.frozen: {getattr(sys, 'frozen', False)}")
    print(f"sys.executable: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")
    
    if getattr(sys, 'frozen', False):
        print("✅ 运行在打包环境中")
        app_dir = os.path.dirname(sys.executable)
        resources_dir = os.path.join(app_dir, "..", "Resources")
        print(f"应用程序目录: {app_dir}")
        print(f"资源目录: {resources_dir}")
        print(f"资源目录存在: {os.path.exists(resources_dir)}")
        
        # 检查模型文件
        model_path = os.path.join(resources_dir, "models", "best.pt")
        print(f"模型路径: {model_path}")
        print(f"模型文件存在: {os.path.exists(model_path)}")
        
        # 测试ultralytics导入
        try:
            import ultralytics
            print(f"✅ ultralytics导入成功: {ultralytics.__version__}")
        except ImportError as e:
            print(f"❌ ultralytics导入失败: {e}")
        
        # 测试cv2导入
        try:
            import cv2
            print(f"✅ cv2导入成功: {cv2.__version__}")
        except ImportError as e:
            print(f"❌ cv2导入失败: {e}")
        
        # 测试numpy导入
        try:
            import numpy
            print(f"✅ numpy导入成功: {numpy.__version__}")
        except ImportError as e:
            print(f"❌ numpy导入失败: {e}")
    else:
        print("❌ 未在打包环境中运行")

if __name__ == "__main__":
    debug_frozen_environment() 