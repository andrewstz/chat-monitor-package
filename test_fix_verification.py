#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证修复的简单测试
"""

def test_imports():
    """测试导入是否正常"""
    print("🧪 测试导入...")
    
    try:
        # 测试配置管理器导入
        from config_manager import get_config_manager
        print("✅ config_manager.get_config_manager 导入成功")
        
        # 测试GUI模块导入
        from gui.contacts_settings import ContactsSettingsWindow
        print("✅ gui.contacts_settings.ContactsSettingsWindow 导入成功")
        
        # 测试主程序导入
        from main_monitor_gui_app import get_config_manager as app_get_config_manager
        print("✅ main_monitor_gui_app.get_config_manager 导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        return False

def test_contact_parsing():
    """测试联系人解析格式"""
    print("\n🧪 测试联系人解析格式...")
    
    try:
        from gui.contacts_settings import ContactsSettingsWindow
        
        # 创建临时实例来测试解析
        temp_window = ContactsSettingsWindow(None)
        
        # 测试换行分隔的输入
        test_text1 = """联系人1
联系人2
联系人3"""
        
        result1 = temp_window.parse_contacts(test_text1)
        print(f"✅ 换行分隔解析: {result1}")
        
        # 测试混合格式（换行+逗号）
        test_text2 = """联系人1,联系人2
联系人3,联系人4
联系人5"""
        
        result2 = temp_window.parse_contacts(test_text2)
        print(f"✅ 混合格式解析: {result2}")
        
        return True
        
    except Exception as e:
        print(f"❌ 解析测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 开始验证修复...")
    
    import_success = test_imports()
    parse_success = test_contact_parsing()
    
    if import_success and parse_success:
        print("\n🎉 所有修复验证通过！")
    else:
        print("\n⚠️ 部分修复验证失败") 