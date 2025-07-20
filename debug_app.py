#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试应用程序路径解析
"""

import os
import sys

def debug_paths():
    """调试路径信息"""
    print("=== 调试信息 ===")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"sys.frozen: {getattr(sys, 'frozen', False)}")
    print(f"sys.executable: {sys.executable}")
    print(f"__file__: {__file__}")
    
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(sys.executable)
        resources_dir = os.path.join(app_dir, "..", "Resources")
        print(f"应用程序目录: {app_dir}")
        print(f"资源目录: {resources_dir}")
        print(f"资源目录存在: {os.path.exists(resources_dir)}")
        
        # 检查模型文件
        model_path = os.path.join(resources_dir, "models", "best.pt")
        print(f"模型路径: {model_path}")
        print(f"模型文件存在: {os.path.exists(model_path)}")
        
        # 列出资源目录内容
        if os.path.exists(resources_dir):
            print("资源目录内容:")
            for item in os.listdir(resources_dir):
                item_path = os.path.join(resources_dir, item)
                if os.path.isdir(item_path):
                    print(f"  目录: {item}")
                    if item == "models":
                        for model_item in os.listdir(item_path):
                            print(f"    模型: {model_item}")
                else:
                    print(f"  文件: {item}")

if __name__ == "__main__":
    debug_paths() 