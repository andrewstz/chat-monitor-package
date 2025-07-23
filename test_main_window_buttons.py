#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_window_buttons():
    """测试主界面按钮布局"""
    print("🔍 测试主界面按钮布局...")
    
    # 创建测试窗口
    root = tk.Tk()
    root.title("ChatMonitor - 按钮布局测试")
    root.resizable(True, True)
    
    # 配置网格权重
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(2, weight=1)
    
    # 标题标签
    title_label = ttk.Label(
        main_frame, 
        text="聊天弹窗监控器", 
        font=("SF Pro Display", 16, "bold")
    )
    title_label.grid(row=0, column=0, pady=(0, 10))
    
    # 状态标签
    status_label = ttk.Label(
        main_frame,
        text="状态: 正在启动...",
        font=("SF Pro Text", 12)
    )
    status_label.grid(row=1, column=0, pady=(0, 10), sticky="w")
    
    # 检测结果显示区
    result_frame = ttk.LabelFrame(main_frame, text="检测到的弹窗", padding="5")
    result_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
    result_frame.columnconfigure(0, weight=1)
    result_frame.rowconfigure(0, weight=1)
    
    # 滚动文本框
    text_area = scrolledtext.ScrolledText(
        result_frame,
        width=60,
        height=15,  # 稍微减小高度
        font=("SF Mono", 10),
        wrap=tk.WORD,
        state=tk.DISABLED
    )
    text_area.grid(row=0, column=0, sticky="nsew")
    
    # 控制按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, pady=(10, 0), sticky="ew")
    button_frame.columnconfigure(0, weight=1)
    
    # 测试按钮
    buttons = [
        ("开始监控", lambda: print("开始监控")),
        ("清空记录", lambda: print("清空记录")),
        ("发信人设置", lambda: print("发信人设置")),
        ("网络监控频率", lambda: print("网络监控频率")),
        ("关闭程序", lambda: root.quit())
    ]
    
    for i, (text, command) in enumerate(buttons):
        btn = ttk.Button(button_frame, text=text, command=command)
        btn.grid(row=0, column=i, padx=(0, 10) if i < len(buttons) - 1 else (0, 0))
    
    # 让窗口自适应内容大小
    root.update_idletasks()
    root.geometry("")
    
    print("✅ 主界面按钮布局测试窗口已创建")
    print("💡 请检查所有5个按钮是否都能正常显示")
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    test_main_window_buttons() 