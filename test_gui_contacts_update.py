#!/usr/bin/env python3
"""
测试GUI中的发信人更新功能
"""

import os
import yaml
import sys

def test_gui_contacts_update():
    """测试GUI中的发信人更新功能"""
    print("🧪 测试GUI中的发信人更新功能")
    
    # 模拟GUI中的保存过程
    try:
        # 1. 模拟用户输入
        user_input = "新用户A,新用户B,新用户C"
        print(f"📝 用户输入: {user_input}")
        
        # 2. 解析发信人
        import re
        contacts = re.split(r'[,，]', user_input)
        cleaned_contacts = [contact.strip() for contact in contacts if contact.strip()]
        print(f"🔍 解析后的发信人: {cleaned_contacts}")
        
        # 3. 读取现有配置
        from main_monitor_dynamic import get_config
        conf = get_config()
        print(f"📋 当前配置中的发信人: {conf.get('chat_app', {}).get('target_contacts', [])}")
        
        # 4. 更新配置
        if "chat_app" not in conf:
            conf["chat_app"] = {}
        conf["chat_app"]["target_contacts"] = cleaned_contacts
        
        # 5. 保存配置文件
        config_path = os.path.expanduser("~/ChatMonitor/config_with_yolo.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(conf, f, default_flow_style=False, allow_unicode=True)
        print(f"💾 已保存配置文件: {config_path}")
        
        # 6. 更新内存中的目标联系人
        from main_monitor_dynamic import update_target_contacts, TARGET_CONTACTS, FUZZY_MATCHER
        update_target_contacts(cleaned_contacts)
        
        # 7. 验证更新
        import main_monitor_dynamic
        print(f"✅ TARGET_CONTACTS: {main_monitor_dynamic.TARGET_CONTACTS}")
        if main_monitor_dynamic.FUZZY_MATCHER:
            print(f"✅ FUZZY_MATCHER.target_contacts: {main_monitor_dynamic.FUZZY_MATCHER.target_contacts}")
            
            # 8. 测试匹配
            print("\n🔍 测试匹配功能:")
            for contact in cleaned_contacts:
                result = main_monitor_dynamic.FUZZY_MATCHER.match_sender(contact)
                if result:
                    matched_contact, sender, similarity = result
                    print(f"  '{contact}' -> 匹配: {matched_contact} (相似度: {similarity:.2f})")
                else:
                    print(f"  '{contact}' -> 无匹配")
        else:
            print("❌ FUZZY_MATCHER未初始化")
            return False
            
        print("\n🎉 GUI发信人更新功能测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gui_contacts_update() 