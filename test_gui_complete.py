#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的GUI功能，包括设置按钮和声音播放
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime

class TestCompleteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("测试 - 完整GUI功能")
        self.root.geometry("500x750")
        self.root.resizable(True, True)
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # 标题标签
        self.title_label = ttk.Label(
            self.main_frame, 
            text="完整功能测试界面", 
            font=("SF Pro Display", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # 状态标签
        self.status_label = ttk.Label(
            self.main_frame,
            text="状态: 准备就绪",
            font=("SF Pro Text", 12)
        )
        self.status_label.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # 检测结果显示区
        self.result_frame = ttk.LabelFrame(self.main_frame, text="测试日志", padding="5")
        self.result_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)
        
        # 滚动文本框
        self.text_area = scrolledtext.ScrolledText(
            self.result_frame,
            width=60,
            height=20,
            font=("SF Mono", 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        # 监控开关框架
        self.switch_frame = ttk.LabelFrame(self.main_frame, text="监控开关", padding="5")
        self.switch_frame.grid(row=3, column=0, pady=(10, 0), sticky="ew")
        
        # 应用监控开关
        self.app_monitor_var = tk.BooleanVar(value=True)
        self.app_monitor_check = ttk.Checkbutton(
            self.switch_frame,
            text="应用监控",
            variable=self.app_monitor_var,
            command=self.on_app_monitor_toggle
        )
        self.app_monitor_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # 网络监控开关
        self.network_monitor_var = tk.BooleanVar(value=True)
        self.network_monitor_check = ttk.Checkbutton(
            self.switch_frame,
            text="网络监控",
            variable=self.network_monitor_var,
            command=self.on_network_monitor_toggle
        )
        self.network_monitor_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # 按钮框架
        self.control_button_frame = ttk.Frame(self.main_frame)
        self.control_button_frame.grid(row=4, column=0, pady=(10, 0))
        
        # 开始/停止按钮
        self.start_stop_button = ttk.Button(
            self.control_button_frame,
            text="开始测试",
            command=self.toggle_testing
        )
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 设置按钮
        self.settings_button = ttk.Button(
            self.control_button_frame,
            text="设置",
            command=self.open_settings
        )
        self.settings_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清空按钮
        self.clear_button = ttk.Button(
            self.control_button_frame,
            text="清空记录",
            command=self.clear_logs
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 关闭按钮
        self.close_button = ttk.Button(
            self.control_button_frame,
            text="关闭程序",
            command=self.close_program
        )
        self.close_button.pack(side=tk.LEFT)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        
        # 测试状态
        self.testing = False
        self.test_thread = None
        
        # 监控开关状态
        self.app_monitor_enabled = True
        self.network_monitor_enabled = True
        
        # 模拟设置
        self.test_contacts = ["微信", "QQ"]
        self.test_network_interval = 60
        
        self.add_log_message("完整测试界面初始化完成")
        self.update_status_label()
    
    def on_app_monitor_toggle(self):
        """应用监控开关切换"""
        self.app_monitor_enabled = self.app_monitor_var.get()
        status = "启用" if self.app_monitor_enabled else "禁用"
        self.add_log_message(f"应用监控已{status}")
        
        if self.testing:
            self.update_status_label()
    
    def on_network_monitor_toggle(self):
        """网络监控开关切换"""
        self.network_monitor_enabled = self.network_monitor_var.get()
        status = "启用" if self.network_monitor_enabled else "禁用"
        self.add_log_message(f"网络监控已{status}")
        
        if self.testing:
            self.update_status_label()
    
    def update_status_label(self):
        """更新状态标签"""
        status_parts = []
        if self.app_monitor_enabled:
            status_parts.append("应用监控")
        if self.network_monitor_enabled:
            status_parts.append("网络监控")
        
        if status_parts:
            status_text = f"状态: 测试中 ({', '.join(status_parts)})"
        else:
            status_text = "状态: 测试已停止 (所有监控已禁用)"
        
        self.status_label.config(text=status_text)
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("测试设置")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # 设置窗口框架
        settings_frame = ttk.Frame(settings_window, padding="10")
        settings_frame.grid(row=0, column=0, sticky="nsew")
        
        # 联系人设置
        contacts_frame = ttk.LabelFrame(settings_frame, text="联系人设置", padding="5")
        contacts_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(contacts_frame, text="目标联系人:").grid(row=0, column=0, sticky="w")
        self.contacts_entry = ttk.Entry(contacts_frame, width=30)
        self.contacts_entry.grid(row=0, column=1, padx=(10, 0))
        self.contacts_entry.insert(0, ", ".join(self.test_contacts))
        
        # 网络频率设置
        network_frame = ttk.LabelFrame(settings_frame, text="网络监控设置", padding="5")
        network_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(network_frame, text="检测间隔(秒):").grid(row=0, column=0, sticky="w")
        self.network_interval_entry = ttk.Entry(network_frame, width=10)
        self.network_interval_entry.grid(row=0, column=1, padx=(10, 0))
        self.network_interval_entry.insert(0, str(self.test_network_interval))
        
        # 保存按钮
        save_button = ttk.Button(settings_frame, text="保存设置", command=lambda: self.save_settings(settings_window))
        save_button.grid(row=2, column=0, pady=(10, 0))
    
    def save_settings(self, settings_window):
        """保存设置"""
        try:
            contacts_text = self.contacts_entry.get().strip()
            network_interval = int(self.network_interval_entry.get().strip())
            
            if contacts_text:
                self.test_contacts = [contact.strip() for contact in contacts_text.split(",")]
            
            self.test_network_interval = network_interval
            
            self.add_log_message(f"设置已保存: 联系人={self.test_contacts}, 网络间隔={self.test_network_interval}秒")
            settings_window.destroy()
            
        except Exception as e:
            self.add_log_message(f"保存设置失败: {str(e)}")
    
    def toggle_testing(self):
        """切换测试状态"""
        if self.testing:
            self.stop_testing()
        else:
            self.start_testing()
    
    def start_testing(self):
        """开始测试"""
        if not self.testing:
            self.testing = True
            self.test_thread = threading.Thread(target=self.run_test, daemon=True)
            self.test_thread.start()
            
            self.update_status_label()
            self.start_stop_button.config(text="停止测试")
            self.add_log_message("测试已启动")
    
    def stop_testing(self):
        """停止测试"""
        self.testing = False
        self.status_label.config(text="状态: 测试已停止")
        self.start_stop_button.config(text="开始测试")
        self.add_log_message("测试已停止")
    
    def run_test(self):
        """运行测试"""
        counter = 0
        while self.testing:
            try:
                counter += 1
                
                # 模拟应用监控
                if self.app_monitor_enabled:
                    self.add_log_message(f"应用监控测试 #{counter}")
                    # 模拟偶尔失败
                    if counter % 5 == 0:
                        self.add_log_message("模拟应用监控失败")
                        # 这里应该播放错误声音，但测试时用日志代替
                        self.add_log_message("🔊 播放错误声音")
                
                # 模拟网络监控
                if self.network_monitor_enabled:
                    self.add_log_message(f"网络监控测试 #{counter}")
                    # 模拟偶尔失败
                    if counter % 7 == 0:
                        self.add_log_message("模拟网络监控失败")
                        # 这里应该播放错误声音，但测试时用日志代替
                        self.add_log_message("🔊 播放错误声音")
                
                # 检查是否有任何监控启用
                if not self.app_monitor_enabled and not self.network_monitor_enabled:
                    self.add_log_message("所有监控已禁用，等待...")
                
                time.sleep(3)  # 3秒间隔
                
            except Exception as e:
                self.add_log_message(f"测试循环错误: {str(e)}")
                time.sleep(3)
    
    def add_log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.text_area.config(state=tk.NORMAL)
        log_text = f"[{timestamp}] {message}\n"
        self.text_area.insert("1.0", log_text)
        self.text_area.config(state=tk.DISABLED)
    
    def clear_logs(self):
        """清空检测记录"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 记录已清空")
    
    def close_program(self):
        """关闭程序"""
        if self.testing:
            self.stop_testing()
        
        self.root.quit()
        self.root.destroy()

def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置 macOS 风格
    try:
        # 尝试设置 macOS 原生风格
        root.tk.call('tk', 'scaling', 2.0)  # 高DPI支持
    except:
        pass
    
    app = TestCompleteGUI(root)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main() 