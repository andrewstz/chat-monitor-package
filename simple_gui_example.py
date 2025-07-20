#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 ChatMonitor GUI 界面示例
使用 tkinter 创建原生 macOS 风格的界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime

class ChatMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatMonitor")
        self.root.geometry("400x500")
        self.root.resizable(True, True)
        
        # 设置窗口图标（可选）
        # self.root.iconbitmap('icon.icns')
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # 标题标签
        self.title_label = ttk.Label(
            self.main_frame, 
            text="聊天弹窗监控器", 
            font=("SF Pro Display", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # 状态标签
        self.status_label = ttk.Label(
            self.main_frame,
            text="状态: 正在监控...",
            font=("SF Pro Text", 12)
        )
        self.status_label.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # 检测结果显示区
        self.result_frame = ttk.LabelFrame(self.main_frame, text="检测到的弹窗", padding="5")
        self.result_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)
        
        # 滚动文本框
        self.text_area = scrolledtext.ScrolledText(
            self.result_frame,
            width=50,
            height=15,
            font=("SF Mono", 11),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        # 按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, pady=(10, 0))
        
        # 清空按钮
        self.clear_button = ttk.Button(
            self.button_frame,
            text="清空记录",
            command=self.clear_logs
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 关闭按钮
        self.close_button = ttk.Button(
            self.button_frame,
            text="关闭程序",
            command=self.close_program,
            style="Accent.TButton"
        )
        self.close_button.pack(side=tk.LEFT)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        
        # 模拟检测线程
        self.running = True
        self.simulation_thread = threading.Thread(target=self.simulate_detection, daemon=True)
        self.simulation_thread.start()
    
    def add_detection_result(self, app_name, content, confidence=None):
        """添加检测结果到显示区"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 启用文本框编辑
        self.text_area.config(state=tk.NORMAL)
        
        # 插入新内容到顶部
        result_text = f"[{timestamp}] {app_name}\n"
        if confidence:
            result_text += f"置信度: {confidence:.2f}\n"
        result_text += f"内容: {content}\n"
        result_text += "-" * 50 + "\n\n"
        
        # 在开头插入新内容
        self.text_area.insert("1.0", result_text)
        
        # 限制显示行数（保持最近100行）
        lines = self.text_area.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", '\n'.join(lines[:100]))
        
        # 禁用文本框编辑
        self.text_area.config(state=tk.DISABLED)
        
        # 更新状态
        self.status_label.config(text=f"状态: 最后检测 {timestamp}")
    
    def clear_logs(self):
        """清空检测记录"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 记录已清空")
    
    def close_program(self):
        """关闭程序"""
        self.running = False
        self.root.quit()
        self.root.destroy()
    
    def simulate_detection(self):
        """模拟检测过程（用于演示）"""
        import random
        
        sample_messages = [
            "新消息提醒",
            "有人@了你",
            "群聊消息",
            "私聊消息",
            "系统通知"
        ]
        
        sample_apps = ["WeChat", "QQ", "钉钉", "企业微信", "Mango"]
        
        while self.running:
            time.sleep(3)  # 每3秒模拟一次检测
            
            if not self.running:
                break
                
            app = random.choice(sample_apps)
            message = random.choice(sample_messages)
            confidence = random.uniform(0.7, 0.95)
            
            # 在主线程中更新UI
            self.root.after(0, self.add_detection_result, app, message, confidence)

def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置 macOS 风格
    try:
        # 尝试设置 macOS 原生风格
        root.tk.call('tk', 'scaling', 2.0)  # 高DPI支持
    except:
        pass
    
    app = ChatMonitorGUI(root)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main() 