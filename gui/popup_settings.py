#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弹框监控设置GUI模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config_manager import get_config_manager

class PopupSettingsWindow:
    def __init__(self, parent, on_save_callback=None):
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.window = None
        
    def open_popup_settings(self):
        """打开弹框监控设置窗口"""
        try:
            # 创建新窗口
            self.window = tk.Toplevel(self.parent)
            self.window.title("弹框监控设置")
            self.window.resizable(True, True)
            
            # 设置窗口层级
            self.window.transient(self.parent)
            self.window.grab_set()
            self.window.lift()
            self.window.focus_force()
            
            # 创建界面
            self.create_popup_settings_ui()
            
            # 设置关闭事件
            def on_closing():
                self.window.grab_release()
                self.window.destroy()
            self.window.protocol("WM_DELETE_WINDOW", on_closing)
            
        except Exception as e:
            print(f"打开弹框监控设置失败: {str(e)}")
    
    def create_popup_settings_ui(self):
        """创建弹框监控设置界面"""
        # 配置窗口网格权重，确保自适应
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="弹框监控设置", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # 说明文本
        description_text = """弹框监控参数说明：

• 检测间隔：每次弹框检测之间的时间间隔（秒）
  推荐值：1-3秒，值越小检测越频繁，但CPU占用越高
  对于短时间弹框（3秒内），建议设置为1秒

• 提醒等待时间：两次声音提醒之间的最小间隔（秒）
  推荐值：3-10秒，值越小提醒越频繁
  避免重复弹框时声音过于频繁

• 快速模式：检测间隔自动调整为0.5秒，提醒等待时间调整为3秒
  适用于需要快速响应的场景，但会增加CPU占用

当前设置："""
        desc_label = ttk.Label(main_frame, text=description_text, justify=tk.LEFT, font=("Arial", 10))
        desc_label.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # 参数输入框架
        params_frame = ttk.LabelFrame(main_frame, text="弹框监控参数", padding="10")
        params_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        params_frame.columnconfigure(1, weight=1)
        
        # 检测间隔
        ttk.Label(params_frame, text="检测间隔（秒）:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.popup_check_interval_var = tk.StringVar()
        popup_check_interval_entry = ttk.Entry(params_frame, textvariable=self.popup_check_interval_var, width=15)
        popup_check_interval_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # 提醒等待时间
        ttk.Label(params_frame, text="提醒等待时间（秒）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.popup_reply_wait_var = tk.StringVar()
        popup_reply_wait_entry = ttk.Entry(params_frame, textvariable=self.popup_reply_wait_var, width=15)
        popup_reply_wait_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # 快速模式
        self.popup_fast_mode_var = tk.BooleanVar()
        popup_fast_mode_check = ttk.Checkbutton(
            params_frame,
            text="快速模式（0.5秒检测间隔，3秒提醒间隔）",
            variable=self.popup_fast_mode_var
        )
        popup_fast_mode_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # YOLO置信度设置
        ttk.Label(params_frame, text="YOLO检测置信度:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.yolo_confidence_var = tk.StringVar()
        yolo_confidence_entry = ttk.Entry(params_frame, textvariable=self.yolo_confidence_var, width=15)
        yolo_confidence_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # 置信度说明
        confidence_desc = ttk.Label(params_frame, text="(0.1-1.0，值越小检测越敏感，但误报越多)", font=("Arial", 8))
        confidence_desc.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 状态标签
        self.popup_status_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.popup_status_label.grid(row=3, column=0, pady=(0, 20), sticky="w")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        
        # 加载当前设置
        self.load_popup_settings()
        
        # 保存按钮
        save_button = ttk.Button(
            button_frame,
            text="保存设置",
            command=lambda: self.save_popup_settings(self.window)
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 恢复默认按钮
        default_button = ttk.Button(
            button_frame,
            text="恢复默认",
            command=self.restore_popup_defaults
        )
        default_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 取消按钮
        cancel_button = ttk.Button(
            button_frame,
            text="取消",
            command=self.window.destroy
        )
        cancel_button.pack(side=tk.RIGHT)
        
        # 让窗口自适应内容大小
        self.window.update_idletasks()
        self.window.geometry("")  # 清除任何固定大小设置
    
    def load_popup_settings(self):
        """加载弹框监控设置"""
        try:
            # 从配置文件加载设置
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            monitor_conf = conf.get("monitor", {})
            popup_conf = conf.get("popup_settings", {})
            yolo_conf = conf.get("yolo", {})
            
            # 设置默认值
            check_interval = monitor_conf.get("check_interval", 1)
            reply_wait = monitor_conf.get("reply_wait", 5)
            fast_mode = popup_conf.get("fast_mode", False)
            yolo_confidence = yolo_conf.get("confidence", 0.3)
            
            # 更新UI
            self.popup_check_interval_var.set(str(check_interval))
            self.popup_reply_wait_var.set(str(reply_wait))
            self.popup_fast_mode_var.set(fast_mode)
            self.yolo_confidence_var.set(str(yolo_confidence))
            
            # 更新状态
            self.update_popup_status_label("✅ 设置已加载")
            
        except Exception as e:
            self.update_popup_status_label(f"❌ 加载设置失败: {str(e)}")
    
    def save_popup_settings(self, window):
        """保存弹框监控设置"""
        try:
            # 获取输入值
            check_interval = float(self.popup_check_interval_var.get())
            reply_wait = float(self.popup_reply_wait_var.get())
            fast_mode = self.popup_fast_mode_var.get()
            yolo_confidence = float(self.yolo_confidence_var.get())
            
            # 验证输入
            if check_interval < 0.1 or check_interval > 10:
                self.update_popup_status_label("❌ 检测间隔必须在0.1-10秒之间")
                return
            
            if reply_wait < 1 or reply_wait > 60:
                self.update_popup_status_label("❌ 提醒等待时间必须在1-60秒之间")
                return
            
            if yolo_confidence < 0.1 or yolo_confidence > 1.0:
                self.update_popup_status_label("❌ YOLO置信度必须在0.1-1.0之间")
                return
            
            # 保存到配置文件
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            
            if "monitor" not in conf:
                conf["monitor"] = {}
            
            conf["monitor"]["check_interval"] = check_interval
            conf["monitor"]["reply_wait"] = reply_wait
            
            # 保存快速模式设置
            if "popup_settings" not in conf:
                conf["popup_settings"] = {}
            
            conf["popup_settings"]["fast_mode"] = fast_mode
            
            # 保存YOLO置信度设置
            if "yolo" not in conf:
                conf["yolo"] = {}
            
            conf["yolo"]["confidence"] = yolo_confidence
            
            config_manager.save_config(conf)
            
            # 更新状态
            self.update_popup_status_label("✅ 设置已保存")
            
            # 调用回调函数
            if self.on_save_callback:
                self.on_save_callback()
            
            # 关闭窗口
            window.destroy()
            
        except ValueError:
            self.update_popup_status_label("❌ 请输入有效的数字")
        except Exception as e:
            self.update_popup_status_label(f"❌ 保存设置失败: {str(e)}")
    
    def restore_popup_defaults(self):
        """恢复弹框监控默认设置"""
        try:
            # 设置默认值
            self.popup_check_interval_var.set("1")
            self.popup_reply_wait_var.set("5")
            self.popup_fast_mode_var.set(False)
            self.yolo_confidence_var.set("0.3")
            
            # 更新状态
            self.update_popup_status_label("✅ 已恢复默认设置")
            
        except Exception as e:
            self.update_popup_status_label(f"❌ 恢复默认设置失败: {str(e)}")
    
    def update_popup_status_label(self, message):
        """更新弹框设置状态标签"""
        try:
            self.popup_status_label.config(text=message)
        except:
            pass 