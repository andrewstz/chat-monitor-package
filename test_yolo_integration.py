#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试YOLO模型集成
"""

import os
import sys

def test_yolo_integration():
    """测试YOLO模型集成"""
    print("=== YOLO模型集成测试 ===")
    
    # 测试ultralytics导入
    try:
        from ultralytics import YOLO
        print("✅ ultralytics导入成功")
    except ImportError as e:
        print(f"❌ ultralytics导入失败: {e}")
        return False
    
    # 测试模型路径解析
    model_path = "models/best.pt"
    print(f"🔍 测试模型路径: {model_path}")
    
    # 检查模型文件是否存在
    if os.path.exists(model_path):
        print(f"✅ 模型文件存在: {model_path}")
    else:
        print(f"❌ 模型文件不存在: {model_path}")
        return False
    
    # 尝试加载模型
    try:
        model = YOLO(model_path)
        print("✅ YOLO模型加载成功")
        
        # 测试模型推理（使用一个简单的测试图像）
        import numpy as np
        test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        results = model(test_image, conf=0.35)
        print("✅ YOLO模型推理测试成功")
        
        return True
    except Exception as e:
        print(f"❌ YOLO模型加载或推理失败: {e}")
        return False

if __name__ == "__main__":
    success = test_yolo_integration()
    if success:
        print("🎉 YOLO模型集成测试通过！")
    else:
        print("❌ YOLO模型集成测试失败！") 