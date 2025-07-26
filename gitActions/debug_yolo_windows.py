#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows下YOLO模型调试脚本
"""

import sys
import os
import traceback

def test_yolo_imports():
    """测试YOLO相关库的导入"""
    print("=== 测试YOLO相关库导入 ===")
    
    # 测试基础库
    try:
        import torch
        print(f"✅ PyTorch版本: {torch.__version__}")
        print(f"✅ CUDA可用: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ PyTorch导入失败: {e}")
        return False
    
    try:
        import ultralytics
        print(f"✅ Ultralytics版本: {ultralytics.__version__}")
    except ImportError as e:
        print(f"❌ Ultralytics导入失败: {e}")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ YOLO类导入成功")
    except ImportError as e:
        print(f"❌ YOLO类导入失败: {e}")
        return False
    
    return True

def test_yolo_model():
    """测试YOLO模型加载"""
    print("\n=== 测试YOLO模型加载 ===")
    
    model_path = "models/best.pt"
    
    # 检查模型文件
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        return False
    
    print(f"✅ 模型文件存在: {model_path}")
    print(f"✅ 文件大小: {os.path.getsize(model_path)} bytes")
    
    try:
        from ultralytics import YOLO
        model = YOLO(model_path)
        print("✅ YOLO模型加载成功")
        
        # 测试推理
        import numpy as np
        dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        results = model(dummy_image)
        print("✅ YOLO推理测试成功")
        
        return True
    except Exception as e:
        print(f"❌ YOLO模型加载失败: {e}")
        print(f"详细错误: {traceback.format_exc()}")
        return False

def test_ocr_imports():
    """测试OCR相关库"""
    print("\n=== 测试OCR相关库 ===")
    
    try:
        import cv2
        print(f"✅ OpenCV版本: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV导入失败: {e}")
        return False
    
    try:
        import pytesseract
        print("✅ Pytesseract导入成功")
        
        # 测试tesseract路径
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract版本: {version}")
        except Exception as e:
            print(f"⚠️ Tesseract路径问题: {e}")
    except ImportError as e:
        print(f"❌ Pytesseract导入失败: {e}")
        return False
    
    return True

def test_audio_imports():
    """测试音频相关库"""
    print("\n=== 测试音频相关库 ===")
    
    try:
        import platform
        system = platform.system()
        print(f"✅ 系统类型: {system}")
        
        if system == "Windows":
            # Windows下测试音频播放
            import subprocess
            try:
                # 测试PowerShell音频播放
                result = subprocess.run(['powershell', '-Command', 'Write-Host "Audio test"'], 
                                     capture_output=True, text=True, timeout=5)
                print("✅ PowerShell可用")
            except Exception as e:
                print(f"❌ PowerShell测试失败: {e}")
        else:
            print("✅ 非Windows系统，跳过音频测试")
            
    except Exception as e:
        print(f"❌ 音频库测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("Windows YOLO调试工具")
    print("=" * 50)
    
    # 测试导入
    yolo_ok = test_yolo_imports()
    ocr_ok = test_ocr_imports()
    audio_ok = test_audio_imports()
    
    # 测试模型
    model_ok = test_yolo_model() if yolo_ok else False
    
    # 总结
    print("\n=== 测试总结 ===")
    print(f"YOLO库导入: {'✅' if yolo_ok else '❌'}")
    print(f"OCR库导入: {'✅' if ocr_ok else '❌'}")
    print(f"音频库导入: {'✅' if audio_ok else '❌'}")
    print(f"YOLO模型加载: {'✅' if model_ok else '❌'}")
    
    if not yolo_ok:
        print("\n🔧 建议解决方案:")
        print("1. 安装PyTorch: pip install torch torchvision")
        print("2. 安装Ultralytics: pip install ultralytics")
        print("3. 确保在打包时包含这些依赖")
    
    if not model_ok:
        print("\n🔧 模型问题解决方案:")
        print("1. 检查models/best.pt文件是否存在")
        print("2. 确保模型文件格式正确")
        print("3. 尝试重新训练或下载模型")
    
    if not audio_ok:
        print("\n🔧 音频问题解决方案:")
        print("1. 确保PowerShell可用")
        print("2. 检查音频驱动")
        print("3. 使用系统命令替代音频库")

if __name__ == "__main__":
    main() 