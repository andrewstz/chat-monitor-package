#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试打包后应用程序的路径解析
"""

import os
import sys

def main():
    print("🔍 测试打包后应用程序的路径解析")
    print(f"🔍 当前工作目录: {os.getcwd()}")
    print(f"🔍 sys.frozen: {getattr(sys, 'frozen', False)}")
    print(f"🔍 sys.executable: {sys.executable}")
    print(f"🔍 sys._MEIPASS: {getattr(sys, '_MEIPASS', 'Not available')}")
    
    model_path = "models/best.pt"
    
    # 测试各种可能的路径
    test_paths = [
        model_path,
        os.path.abspath(model_path),
    ]
    
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(sys.executable)
        resources_dir = os.path.join(app_dir, "..", "Resources")
        resources_path = os.path.join(resources_dir, model_path)
        test_paths.insert(0, resources_path)
        
        if hasattr(sys, '_MEIPASS'):
            meipass_path = os.path.join(sys._MEIPASS, model_path)
            test_paths.insert(0, meipass_path)
    
    print(f"🔍 测试的路径列表:")
    for i, path in enumerate(test_paths):
        exists = os.path.exists(path)
        print(f"  {i+1}. {path} - {'✅ 存在' if exists else '❌ 不存在'}")
        if exists:
            print(f"     📁 文件大小: {os.path.getsize(path)} bytes")
    
    # 查找第一个存在的路径
    for path in test_paths:
        if os.path.exists(path):
            print(f"✅ 找到模型文件: {path}")
            return path
    
    print("❌ 未找到模型文件")
    return None

if __name__ == "__main__":
    main() 