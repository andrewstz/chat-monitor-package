#!/usr/bin/env python3
"""
测试窗口层级修复
验证主窗口不再置顶，弹框能正确显示在主窗口之上
"""

import tkinter as tk
from tkinter import ttk
import time

def test_window_layering():
    """测试窗口层级"""
    print("🧪 测试窗口层级修复...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("ChatMonitor - 测试")
    root.geometry("400x300")
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill="both", expand=True)
    
    # 标题
    title_label = ttk.Label(main_frame, text="聊天弹窗监控器", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # 状态标签
    status_label = ttk.Label(main_frame, text="状态: 测试中...", font=("Arial", 12))
    status_label.pack(pady=(0, 20))
    
    def open_test_popup():
        """打开测试弹框"""
        print("🔄 打开测试弹框...")
        
        # 创建弹框
        popup = tk.Toplevel(root)
        popup.title("发信人设置 - 测试")
        popup.geometry("300x200")
        popup.transient(root)  # 设置为主窗口的子窗口
        popup.grab_set()  # 模态窗口
        
        # 居中显示
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # 创建弹框内容
        popup_frame = ttk.Frame(popup, padding="20")
        popup_frame.pack(fill="both", expand=True)
        
        popup_title = ttk.Label(popup_frame, text="测试弹框", font=("Arial", 14, "bold"))
        popup_title.pack(pady=(0, 20))
        
        popup_text = ttk.Label(popup_frame, text="这个弹框应该显示在主窗口之上", font=("Arial", 10))
        popup_text.pack(pady=(0, 20))
        
        # 确保弹框显示在主窗口之上
        popup.lift()  # 提升到最顶层
        popup.focus_force()  # 强制设置焦点
        
        # 绑定窗口关闭事件
        def on_closing():
            popup.grab_release()
            popup.destroy()
            print("✅ 测试弹框已关闭")
        
        popup.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("✅ 测试弹框已打开")
    
    # 测试按钮
    test_button = ttk.Button(main_frame, text="打开测试弹框", command=open_test_popup)
    test_button.pack(pady=10)
    
    # 说明文字
    instruction_label = ttk.Label(main_frame, text="点击按钮打开测试弹框，验证层级是否正确", 
                                font=("Arial", 9), foreground="gray")
    instruction_label.pack(pady=10)
    
    # 关闭按钮
    close_button = ttk.Button(main_frame, text="关闭测试", command=root.quit)
    close_button.pack(pady=10)
    
    print("✅ 测试窗口已创建")
    print("📋 测试说明:")
    print("  1. 主窗口不应该总是置顶")
    print("  2. 点击'打开测试弹框'按钮")
    print("  3. 弹框应该显示在主窗口之上")
    print("  4. 切换到其他应用，主窗口应该正常隐藏")
    
    # 启动主循环
    root.mainloop()
    print("✅ 测试完成")

if __name__ == "__main__":
    test_window_layering() 