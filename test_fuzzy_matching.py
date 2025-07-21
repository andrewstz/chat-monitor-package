#!/usr/bin/env python3
"""
测试FUZZY_MATCHER的匹配功能
"""

def test_fuzzy_matching():
    """测试模糊匹配功能"""
    print("🧪 测试FUZZY_MATCHER匹配功能")
    
    try:
        from main_monitor_dynamic import FUZZY_MATCHER, TARGET_CONTACTS
        
        print(f"📋 当前目标联系人: {TARGET_CONTACTS}")
        if FUZZY_MATCHER:
            print(f"🎯 FUZZY_MATCHER目标联系人: {FUZZY_MATCHER.target_contacts}")
        else:
            print("❌ FUZZY_MATCHER未初始化")
            return False
        
        # 测试文本
        test_texts = [
            "【常规】客户端项目",
            "客户端项目",
            "Morton: https://commonjira.itcom888.com/browse/SKGCRUM-559918",
            "老板,这个之前0625迭代是你负责的吗?我们测试了品牌域名还没改变",
            "人事小姐姐",
            "js_wbmalia-研发部助理",
            "测试用户A",
            "新用户B"
        ]
        
        print("\n🔍 测试匹配功能:")
        for text in test_texts:
            result = FUZZY_MATCHER.match_sender(text)
            if result:
                contact, sender, similarity = result
                print(f"  ✅ '{text}' -> 匹配: {contact} (相似度: {similarity:.2f})")
            else:
                print(f"  ❌ '{text}' -> 无匹配")
        
        # 测试相似度阈值
        print(f"\n🔧 当前相似度阈值: {FUZZY_MATCHER.similarity_threshold}")
        
        # 测试部分匹配
        print("\n🔍 测试部分匹配:")
        partial_texts = [
            "客户端",
            "项目",
            "人事",
            "小姐姐",
            "研发部",
            "助理"
        ]
        
        for text in partial_texts:
            result = FUZZY_MATCHER.match_sender(text)
            if result:
                contact, sender, similarity = result
                print(f"  ✅ '{text}' -> 匹配: {contact} (相似度: {similarity:.2f})")
            else:
                print(f"  ❌ '{text}' -> 无匹配")
        
        print("\n🎉 模糊匹配功能测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fuzzy_matching() 