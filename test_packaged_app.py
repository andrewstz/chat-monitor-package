#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试打包后应用程序的模型路径解析
"""

import os
import sys

def test_model_path():
    """测试模型路径解析"""
    print("🔍 测试打包后应用程序的模型路径解析")
    print(f"🔍 当前工作目录: {os.getcwd()}")
    print(f"🔍 sys.frozen: {getattr(sys, 'frozen', False)}")
    print(f"🔍 sys.executable: {sys.executable}")
    print(f"🔍 sys._MEIPASS: {getattr(sys, '_MEIPASS', 'Not available')}")
    
    model_path = "models/best.pt"
    possible_paths = []
    
    # 基本路径
    possible_paths.append(model_path)
    possible_paths.append(os.path.abspath(model_path))
    
    # 如果是 .app 包，尝试从 Resources 目录加载
    if getattr(sys, 'frozen', False):
        # 打包后的应用
        app_dir = os.path.dirname(sys.executable)
        resources_dir = os.path.join(app_dir, "..", "Resources")
        resources_path = os.path.join(resources_dir, model_path)
        possible_paths.insert(0, resources_path)
        print(f"🔍 添加Resources路径: {resources_path}")
        
        # 也尝试从用户目录加载
        user_home = os.path.expanduser("~")
        user_models_path = os.path.join(user_home, "ChatMonitor", "models", "best.pt")
        possible_paths.insert(0, user_models_path)
        print(f"🔍 添加用户目录路径: {user_models_path}")
        
        # 尝试从应用程序包内的相对路径加载
        app_resources_path = os.path.join("..", "Resources", model_path)
        possible_paths.insert(0, app_resources_path)
        print(f"🔍 添加相对Resources路径: {app_resources_path}")
        
        # 尝试从当前工作目录的上级目录加载
        parent_models_path = os.path.join("..", model_path)
        possible_paths.insert(0, parent_models_path)
        print(f"🔍 添加上级目录路径: {parent_models_path}")
        
        # 尝试从 sys._MEIPASS 目录加载（PyInstaller 临时目录）
        if hasattr(sys, '_MEIPASS'):
            meipass_path = os.path.join(sys._MEIPASS, model_path)
            possible_paths.insert(0, meipass_path)
            print(f"🔍 添加_MEIPASS路径: {meipass_path}")
        
        # 尝试从当前工作目录直接加载
        cwd_path = os.path.join(os.getcwd(), model_path)
        possible_paths.insert(0, cwd_path)
        print(f"🔍 添加当前工作目录路径: {cwd_path}")
        
        # 尝试从脚本所在目录加载
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_models_path = os.path.join(script_dir, model_path)
        possible_paths.insert(0, script_models_path)
        print(f"🔍 添加脚本目录路径: {script_models_path}")
    
    print(f"🔍 尝试的路径列表:")
    for i, path in enumerate(possible_paths):
        exists = os.path.exists(path)
        print(f"  {i+1}. {path} - {'✅ 存在' if exists else '❌ 不存在'}")
        if exists:
            print(f"     📁 文件大小: {os.path.getsize(path)} bytes")
    
    # 查找第一个存在的路径
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到模型文件: {path}")
            return path
    
    print("❌ 未找到模型文件")
    return None

if __name__ == "__main__":
    test_model_path() 