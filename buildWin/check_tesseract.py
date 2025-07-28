#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def check_pytesseract():
    """检查pytesseract模块"""
    print("Step 1: Checking pytesseract module...")
    try:
        import pytesseract
        print("✓ pytesseract imported successfully")
        return True
    except ImportError as e:
        print(f"✗ pytesseract not installed: {e}")
        return False

def check_tesseract_executable():
    """检查tesseract可执行文件"""
    print("\nStep 2: Checking tesseract executable...")
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ tesseract executable found in PATH")
            print(f"Version: {result.stdout.strip()}")
            return True
        else:
            print("✗ tesseract executable not working")
            return False
    except Exception as e:
        print(f"✗ tesseract executable not found: {e}")
        return False

def find_tesseract_path():
    """查找tesseract安装路径"""
    print("\nStep 3: Searching for tesseract installation...")
    
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Users\%USERNAME%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    ]
    
    for path in possible_paths:
        expanded_path = os.path.expandvars(path)
        print(f"Checking: {expanded_path}")
        
        if os.path.exists(expanded_path):
            try:
                result = subprocess.run([expanded_path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✓ Found working tesseract: {expanded_path}")
                    print(f"Version: {result.stdout.strip()}")
                    return expanded_path
                else:
                    print("  ✗ Not working")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print("  ✗ Not found")
    
    return None

def test_pytesseract_functionality():
    """测试pytesseract功能"""
    print("\nStep 4: Testing pytesseract functionality...")
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✓ pytesseract working, version: {version}")
        return True
    except Exception as e:
        print(f"✗ pytesseract error: {e}")
        
        # 尝试手动设置路径
        tesseract_path = find_tesseract_path()
        if tesseract_path:
            try:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                version = pytesseract.get_tesseract_version()
                print(f"✓ Successfully set tesseract path: {tesseract_path}")
                print(f"Version: {version}")
                return True
            except Exception as e2:
                print(f"✗ Failed to set path: {e2}")
                return False
        else:
            print("✗ No working tesseract found")
            return False

def create_path_fix():
    """创建路径修复脚本"""
    print("\nStep 5: Creating path fix script...")
    
    tesseract_path = find_tesseract_path()
    if tesseract_path:
        script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'{tesseract_path}'

# Test the configuration
try:
    version = pytesseract.get_tesseract_version()
    print(f"Tesseract configured successfully: {{version}}")
except Exception as e:
    print(f"Error: {{e}}")
'''
        
        with open('tesseract_path_fix.py', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print("✓ Created: tesseract_path_fix.py")
        print("You can import this script to fix tesseract path")
        return True
    else:
        print("✗ Could not create path fix script")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("Tesseract Installation Check")
    print("=" * 50)
    
    pytesseract_ok = check_pytesseract()
    tesseract_ok = check_tesseract_executable()
    functionality_ok = test_pytesseract_functionality()
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("=" * 50)
    
    if pytesseract_ok and tesseract_ok and functionality_ok:
        print("✓ Tesseract is properly configured!")
        print("Your application should work without OCR errors.")
    else:
        print("✗ Tesseract is not properly configured")
        print("\nSolutions:")
        print("1. Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Add to PATH: C:\\Program Files\\Tesseract-OCR")
        print("3. Or use the path fix script if created above")
        
        if not functionality_ok:
            create_path_fix()
    
    print("\nCheck completed!")

if __name__ == "__main__":
    main() 