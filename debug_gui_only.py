#!/usr/bin/env python3
"""
纯GUI调试版本 - 只测试发信人设置功能
完全绕过YOLO和复杂初始化
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import yaml
import re
import sys

def debug_log(msg):
    """简化的调试日志"""
    print(f"[DEBUG] {msg}")

class ContactSettingsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatMonitor - 发信人设置调试")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # 配置文件路径
        self.config_path = "config_with_yolo.yaml"
        
        # 创建界面
        self.create_widgets()
        
        # 加载默认值
        self.load_default_contacts()
        
        # 添加调试按钮
        self.add_debug_buttons()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="发信人设置调试", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 说明文字
        instruction_label = ttk.Label(main_frame, text="请输入要监控的发信人姓名，多个发信人用逗号分隔：", 
                                    font=("Arial", 10))
        instruction_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # 示例
        example_label = ttk.Label(main_frame, text="示例：张三,李四,王五 或 张三，李四，王五", 
                                font=("Arial", 9), foreground="gray")
        example_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # 输入框标签
        input_label = ttk.Label(main_frame, text="发信人列表：", font=("Arial", 11, "bold"))
        input_label.grid(row=3, column=0, sticky="w", pady=(0, 5))
        
        # 输入框
        self.contact_text = tk.Text(main_frame, height=8, width=60, font=("Arial", 11))
        self.contact_text.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        
        # 配置文本框的滚动条
        text_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.contact_text.yview)
        text_scrollbar.grid(row=4, column=2, sticky="ns")
        self.contact_text.configure(yscrollcommand=text_scrollbar.set)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # 保存按钮
        save_button = ttk.Button(button_frame, text="保存设置", command=self.save_contacts)
        save_button.pack(side="left", padx=(0, 10))
        
        # 重置按钮
        reset_button = ttk.Button(button_frame, text="重置为默认", command=self.reset_to_default)
        reset_button.pack(side="left", padx=(0, 10))
        
        # 清空按钮
        clear_button = ttk.Button(button_frame, text="清空", command=self.clear_contacts)
        clear_button.pack(side="left", padx=(0, 10))
        
        # 退出按钮
        exit_button = ttk.Button(button_frame, text="退出", command=self.root.quit)
        exit_button.pack(side="left")
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def add_debug_buttons(self):
        """添加调试按钮"""
        debug_frame = ttk.Frame(self.root)
        debug_frame.grid(row=1, column=0, pady=(10, 0))
        
        # 测试匹配按钮
        test_match_button = ttk.Button(debug_frame, text="测试匹配", command=self.test_matching)
        test_match_button.pack(side="left", padx=(0, 10))
        
        # 检查配置按钮
        check_config_button = ttk.Button(debug_frame, text="检查配置", command=self.check_config)
        check_config_button.pack(side="left", padx=(0, 10))
        
        # 检查FUZZY_MATCHER按钮
        check_fuzzy_button = ttk.Button(debug_frame, text="检查FUZZY_MATCHER", command=self.check_fuzzy_matcher)
        check_fuzzy_button.pack(side="left", padx=(0, 10))
        
        # 测试更新按钮
        test_update_button = ttk.Button(debug_frame, text="测试更新", command=self.test_update)
        test_update_button.pack(side="left")
    
    def load_default_contacts(self):
        """从配置文件加载默认发信人"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                # 获取默认发信人
                default_contacts = config.get("chat_app", {}).get("target_contacts", [])
                
                if default_contacts:
                    # 将列表转换为逗号分隔的字符串
                    contacts_str = ", ".join(default_contacts)
                    self.contact_text.delete(1.0, tk.END)
                    self.contact_text.insert(1.0, contacts_str)
                    self.update_status(f"已加载 {len(default_contacts)} 个默认发信人")
                    debug_log(f"📋 加载的默认发信人: {default_contacts}")
                else:
                    self.update_status("未找到默认发信人配置")
            else:
                self.update_status("配置文件不存在，使用空列表")
                
        except Exception as e:
            self.update_status(f"加载配置文件失败: {str(e)}")
            debug_log(f"❌ 加载配置文件失败: {e}")
    
    def parse_contacts(self, text):
        """解析发信人文本，支持中英文逗号"""
        if not text.strip():
            return []
        
        # 使用正则表达式分割，支持中英文逗号
        contacts = re.split(r'[,，]', text)
        
        # 清理每个联系人（去除空格和换行）
        cleaned_contacts = []
        for contact in contacts:
            contact = contact.strip()
            if contact:  # 只添加非空联系人
                cleaned_contacts.append(contact)
        
        debug_log(f"🔍 解析结果: {cleaned_contacts}")
        return cleaned_contacts
    
    def save_contacts(self):
        """保存发信人设置到配置文件"""
        debug_log("🔧 开始保存发信人设置...")
        
        try:
            # 获取输入文本
            text = self.contact_text.get(1.0, tk.END).strip()
            debug_log(f"📝 输入文本: '{text}'")
            
            # 解析发信人
            contacts = self.parse_contacts(text)
            
            if not contacts:
                messagebox.showwarning("警告", "请输入至少一个发信人姓名")
                return
            
            debug_log(f"📋 解析后的发信人: {contacts}")
            
            # 读取现有配置
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                debug_log("✅ 成功读取现有配置文件")
            else:
                config = {}
                debug_log("⚠️ 配置文件不存在，创建新配置")
            
            # 更新发信人配置
            if "chat_app" not in config:
                config["chat_app"] = {}
            
            config["chat_app"]["target_contacts"] = contacts
            
            # 保存配置文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            debug_log("✅ 配置文件已保存")
            
            # 立即更新内存中的目标联系人
            try:
                # 这里我们直接模拟更新，不依赖main_monitor_dynamic
                debug_log("🔄 模拟更新内存中的目标联系人...")
                self.simulate_update_target_contacts(contacts)
            except Exception as e:
                debug_log(f"❌ 更新内存失败: {e}")
            
            self.update_status(f"已保存 {len(contacts)} 个发信人: {', '.join(contacts)}")
            messagebox.showinfo("成功", f"已保存 {len(contacts)} 个发信人设置")
            
        except Exception as e:
            error_msg = f"保存配置文件失败: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("错误", error_msg)
            debug_log(f"❌ 保存失败: {e}")
    
    def simulate_update_target_contacts(self, contacts):
        """模拟更新目标联系人"""
        debug_log(f"🔄 模拟更新TARGET_CONTACTS: {contacts}")
        # 这里只是模拟，实际应该调用main_monitor_dynamic.update_target_contacts
        debug_log("✅ 模拟更新完成")
    
    def reset_to_default(self):
        """重置为默认发信人"""
        self.load_default_contacts()
        self.update_status("已重置为默认发信人")
    
    def clear_contacts(self):
        """清空发信人列表"""
        self.contact_text.delete(1.0, tk.END)
        self.update_status("已清空发信人列表")
    
    def update_status(self, message):
        """更新状态标签"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        debug_log(f"📊 状态更新: {message}")
    
    def test_matching(self):
        """测试匹配功能"""
        debug_log("🧪 开始测试匹配功能...")
        try:
            # 这里我们只是测试解析功能
            text = self.contact_text.get(1.0, tk.END).strip()
            contacts = self.parse_contacts(text)
            
            debug_log(f"📋 当前发信人列表: {contacts}")
            
            # 测试文本
            test_texts = ["【常规】客户端项目", "客户端项目", "人事小姐姐", "js_wbmalia-研发部助理"]
            
            for text in test_texts:
                debug_log(f"🔍 测试文本: '{text}'")
                # 简单的包含匹配
                matched = False
                for contact in contacts:
                    if contact in text or text in contact:
                        debug_log(f"✅ '{text}' -> 匹配: {contact}")
                        matched = True
                        break
                if not matched:
                    debug_log(f"❌ '{text}' -> 无匹配")
                    
        except Exception as e:
            debug_log(f"❌ 测试匹配失败: {e}")
    
    def check_config(self):
        """检查配置文件"""
        debug_log("📋 检查配置文件...")
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                contacts = config.get("chat_app", {}).get("target_contacts", [])
                debug_log(f"📋 配置文件中的发信人: {contacts}")
            else:
                debug_log("❌ 配置文件不存在")
                
        except Exception as e:
            debug_log(f"❌ 检查配置失败: {e}")
    
    def check_fuzzy_matcher(self):
        """检查FUZZY_MATCHER状态"""
        debug_log("🎯 检查FUZZY_MATCHER状态...")
        try:
            # 尝试导入，但不依赖它
            debug_log("⚠️ 跳过FUZZY_MATCHER检查（避免复杂初始化）")
            debug_log("💡 建议：在VS Code中设置断点来检查")
            
        except Exception as e:
            debug_log(f"❌ 检查FUZZY_MATCHER失败: {e}")
    
    def test_update(self):
        """测试更新功能"""
        debug_log("🧪 测试更新功能...")
        try:
            # 模拟一个更新
            test_contacts = ["测试联系人1", "测试联系人2"]
            self.simulate_update_target_contacts(test_contacts)
            debug_log("✅ 测试更新完成")
            
        except Exception as e:
            debug_log(f"❌ 测试更新失败: {e}")

def main():
    """主函数"""
    debug_log("🚀 启动纯GUI调试版本...")
    
    root = tk.Tk()
    app = ContactSettingsGUI(root)
    
    # 设置窗口居中
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    debug_log("✅ GUI已创建，开始主循环...")
    
    # 启动GUI
    root.mainloop()
    
    debug_log("✅ 程序已退出")

if __name__ == "__main__":
    main() 