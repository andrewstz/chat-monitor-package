#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试YOLO模型路径解析
"""

import os
import sys

def test_model_path_resolution():
    """测试模型路径解析逻辑"""
    model_path = "models/best.pt"
    
    print(f"🔍 开始解析模型路径: {model_path}")
    print(f"🔍 当前工作目录: {os.getcwd()}")
    print(f"🔍 sys.frozen: {getattr(sys, 'frozen', False)}")
    if getattr(sys, 'frozen', False):
        print(f"🔍 sys.executable: {sys.executable}")
        print(f"🔍 可执行文件目录: {os.path.dirname(sys.executable)}")
    
    # 如果路径已经是绝对路径且存在，直接返回
    if os.path.isabs(model_path) and os.path.exists(model_path):
        print(f"✅ 绝对路径存在: {model_path}")
        return model_path
        
    # 可能的模型路径
    possible_paths = [
        model_path,  # 当前目录
        os.path.join(os.path.dirname(__file__), model_path),  # 脚本目录
        os.path.join(os.path.dirname(os.path.abspath(__file__)), model_path),  # 绝对路径
    ]
    
    # 如果是 .app 包，尝试从 Resources 目录加载
    if getattr(sys, 'frozen', False):
        # 打包后的应用
        app_dir = os.path.dirname(sys.executable)
        resources_dir = os.path.join(app_dir, "..", "Resources")
        resources_path = os.path.join(resources_dir, model_path)
        possible_paths.insert(0, resources_path)
        print(f"🔍 添加Resources路径: {resources_path}")
    
    print(f"🔍 尝试的路径列表:")
    for i, path in enumerate(possible_paths):
        exists = os.path.exists(path)
        print(f"  {i+1}. {path} - {'✅存在' if exists else '❌不存在'}")
    
    # 查找存在的模型文件
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到YOLO模型文件: {path}")
            return path
    
    # 如果都找不到，返回原始路径
    print(f"⚠️  未找到YOLO模型文件: {model_path}")
    return model_path

if __name__ == "__main__":
    result = test_model_path_resolution()
    print(f"�� 最终结果: {result}") 