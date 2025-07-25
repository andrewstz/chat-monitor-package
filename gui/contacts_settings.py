#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
联系人设置GUI模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config_manager import get_config_manager

class ContactsSettingsWindow:
    def __init__(self, parent, on_save_callback=None):
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.window = None
        
    def open_contacts_settings(self):
        """打开联系人设置窗口"""
        try:
            # 创建新窗口
            self.window = tk.Toplevel(self.parent)
            self.window.title("发信人设置")
            self.window.geometry("600x500")
            self.window.resizable(True, True)
            
            # 设置窗口图标
            try:
                self.window.iconbitmap("assets/icons/icon.icns")
            except:
                pass
            
            # 创建界面
            self.create_contacts_settings_ui()
            
            # 设置窗口关闭事件
            def on_closing():
                self.window.destroy()
            
            self.window.protocol("WM_DELETE_WINDOW", on_closing)
            
            # 居中显示窗口
            self.window.transient(self.parent)
            self.window.grab_set()
            
        except Exception as e:
            print(f"打开联系人设置失败: {str(e)}")
    
    def create_contacts_settings_ui(self):
        """创建联系人设置界面"""
        # 配置窗口网格权重，确保自适应
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="发信人设置", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # 说明文本
        description_text = """联系人设置说明：

• 每行输入一个联系人姓名
• 支持模糊匹配，相似度达到阈值即可触发提醒
• 建议添加常用的联系人姓名
• 修改后点击保存即可生效

当前联系人列表："""
        desc_label = ttk.Label(main_frame, text=description_text, justify=tk.LEFT, font=("Arial", 10))
        desc_label.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # 文本输入区域
        text_frame = ttk.LabelFrame(main_frame, text="联系人列表", padding="10")
        text_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 创建文本框和滚动条
        self.text_widget = tk.Text(text_frame, height=15, width=60, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.status_label.grid(row=3, column=0, pady=(0, 20), sticky="w")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        
        # 保存按钮
        save_button = ttk.Button(
            button_frame,
            text="保存联系人",
            command=lambda: self.save_contacts_from_text(self.text_widget, self.status_label, self.window)
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清空按钮
        clear_button = ttk.Button(
            button_frame,
            text="清空列表",
            command=lambda: self.clear_contacts_text(self.text_widget, self.status_label)
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 取消按钮
        cancel_button = ttk.Button(
            button_frame,
            text="取消",
            command=self.window.destroy
        )
        cancel_button.pack(side=tk.RIGHT)
        
        # 加载当前联系人
        self.load_contacts_to_text(self.text_widget, self.status_label)
        
        # 让窗口自适应内容大小
        self.window.update_idletasks()
        self.window.geometry("")  # 清除任何固定大小设置
    
    def load_contacts_to_text(self, text_widget, status_label):
        """加载联系人到文本框"""
        try:
            # 从配置文件加载联系人
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            target_contacts = conf.get("chat_app", {}).get("target_contacts", [])
            
            # 清空文本框
            text_widget.delete("1.0", tk.END)
            
            # 插入联系人
            if target_contacts:
                # 使用换行分隔显示联系人（每行一个）
                contacts_text = "\n".join(target_contacts)
                text_widget.insert("1.0", contacts_text)
                self.update_settings_status_label(status_label, f"✅ 已加载 {len(target_contacts)} 个联系人")
            else:
                self.update_settings_status_label(status_label, "⚠️ 未找到联系人，请添加联系人")
                
        except Exception as e:
            self.update_settings_status_label(status_label, f"❌ 加载联系人失败: {str(e)}")
    
    def parse_contacts(self, text):
        """解析联系人文本"""
        contacts = []
        # 优先支持换行分隔，也支持逗号分隔
        text = text.strip()
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line:  # 忽略空行
                # 如果行内包含逗号，则按逗号分割
                if ',' in line:
                    items = line.split(',')
                    for item in items:
                        item = item.strip()
                        if item:  # 忽略空项
                            contacts.append(item)
                else:
                    contacts.append(line)
        
        return contacts
    
    def save_contacts_from_text(self, text_widget, status_label, window):
        """从文本框保存联系人"""
        try:
            # 获取文本框内容
            text = text_widget.get("1.0", tk.END).strip()
            
            if not text:
                self.update_settings_status_label(status_label, "❌ 请输入至少一个联系人")
                return
            
            # 解析联系人
            contacts = self.parse_contacts(text)
            
            if not contacts:
                self.update_settings_status_label(status_label, "❌ 未找到有效的联系人")
                return
            
            # 保存到配置文件
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            if "chat_app" not in conf:
                conf["chat_app"] = {}
            
            conf["chat_app"]["target_contacts"] = contacts
            config_manager.save_config(conf)
            
            # 更新状态
            self.update_settings_status_label(status_label, f"✅ 已保存 {len(contacts)} 个联系人")
            
            # 显示确认弹框
            import tkinter.messagebox as messagebox
            messagebox.showinfo("保存成功", f"已成功保存 {len(contacts)} 个联系人！")
            
            # 调用回调函数
            if self.on_save_callback:
                self.on_save_callback()
            
            # 关闭窗口
            window.destroy()
            
        except Exception as e:
            self.update_settings_status_label(status_label, f"❌ 保存联系人失败: {str(e)}")
    
    def clear_contacts_text(self, text_widget, status_label):
        """清空联系人文本框"""
        text_widget.delete("1.0", tk.END)
        self.update_settings_status_label(status_label, "✅ 联系人列表已清空")
    
    def update_settings_status_label(self, status_label, message):
        """更新设置状态标签"""
        try:
            status_label.config(text=message)
        except:
            pass 