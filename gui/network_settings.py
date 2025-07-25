#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络监控设置GUI模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config_manager import get_config_manager

class NetworkSettingsWindow:
    def __init__(self, parent, on_save_callback=None):
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.window = None
        
    def open_network_settings(self):
        """打开网络监控设置窗口"""
        try:
            # 创建新窗口
            self.window = tk.Toplevel(self.parent)
            self.window.title("网络监控频率设置")
            self.window.resizable(True, True)
            
            # 设置窗口层级
            self.window.transient(self.parent)
            self.window.grab_set()
            self.window.lift()
            self.window.focus_force()
            
            # 创建界面
            self.create_network_settings_ui()
            
            # 设置关闭事件
            def on_closing():
                self.window.grab_release()
                self.window.destroy()
            self.window.protocol("WM_DELETE_WINDOW", on_closing)
            
        except Exception as e:
            print(f"打开网络监控设置失败: {str(e)}")
    
    def create_network_settings_ui(self):
        """创建网络监控设置界面"""
        # 配置窗口网格权重，确保自适应
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="网络监控频率设置", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # 说明文本
        description_text = """网络监控参数说明：

• 检测间隔：每次网络检测之间的时间间隔（秒）
  推荐值：10-60秒，值越小检测越频繁

• 超时时间：单次网络检测的最大等待时间（秒）
  推荐值：5-10秒，值越大越稳定但响应越慢

• 连续失败阈值：触发警报前允许的连续失败次数
  推荐值：2-5次，值越大越稳定但响应越慢

注意：重复警报间隔 = 检测间隔 × 连续失败阈值
例如：10秒间隔 × 3次失败 = 30秒重复警报

当前设置："""
        desc_label = ttk.Label(main_frame, text=description_text, justify=tk.LEFT, font=("Arial", 10))
        desc_label.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # 参数输入框架
        params_frame = ttk.LabelFrame(main_frame, text="网络监控参数", padding="10")
        params_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        params_frame.columnconfigure(1, weight=1)
        
        # 检测间隔
        ttk.Label(params_frame, text="检测间隔（秒）:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.check_interval_var = tk.StringVar()
        check_interval_entry = ttk.Entry(params_frame, textvariable=self.check_interval_var, width=15)
        check_interval_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # 超时时间
        ttk.Label(params_frame, text="超时时间（秒）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.StringVar()
        timeout_entry = ttk.Entry(params_frame, textvariable=self.timeout_var, width=15)
        timeout_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # 连续失败阈值
        ttk.Label(params_frame, text="连续失败阈值:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.consecutive_failures_var = tk.StringVar()
        consecutive_failures_entry = ttk.Entry(params_frame, textvariable=self.consecutive_failures_var, width=15)
        consecutive_failures_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # 状态标签
        self.network_status_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.network_status_label.grid(row=3, column=0, pady=(0, 20), sticky="w")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        
        # 加载当前设置
        self.load_network_settings()
        
        # 保存按钮
        save_button = ttk.Button(
            button_frame,
            text="保存设置",
            command=lambda: self.save_network_settings(self.window)
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 恢复默认按钮
        default_button = ttk.Button(
            button_frame,
            text="恢复默认",
            command=self.restore_network_defaults
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
    
    def load_network_settings(self):
        """加载当前网络监控设置"""
        try:
            config_manager = get_config_manager()
            network_config = config_manager.get_network_config()
            
            # 设置当前值
            self.check_interval_var.set(str(network_config.get("check_interval", 10)))
            self.timeout_var.set(str(network_config.get("timeout", 5)))
            self.consecutive_failures_var.set(str(network_config.get("consecutive_failures", 3)))
            
            self.update_network_status_label("✅ 已加载当前设置")
            
        except Exception as e:
            self.update_network_status_label(f"❌ 加载设置失败: {str(e)}")
    
    def save_network_settings(self, window):
        """保存网络监控设置"""
        try:
            # 获取输入值
            check_interval = float(self.check_interval_var.get())
            timeout = float(self.timeout_var.get())
            consecutive_failures = int(self.consecutive_failures_var.get())
            
            # 验证输入
            if check_interval < 1 or timeout < 1 or consecutive_failures < 1:
                self.update_network_status_label("❌ 参数值无效，请检查输入")
                return
            
            # 保存到配置文件
            config_manager = get_config_manager()
            
            # 更新网络监控配置
            config_manager.update_network_config({
                "check_interval": check_interval,
                "timeout": timeout,
                "consecutive_failures": consecutive_failures
            })
            
            # 更新状态
            self.update_network_status_label("✅ 设置已保存")
            
            # 调用回调函数
            if self.on_save_callback:
                self.on_save_callback()
            
            # 关闭窗口
            window.destroy()
            
        except ValueError:
            self.update_network_status_label("❌ 请输入有效的数字")
        except Exception as e:
            self.update_network_status_label(f"❌ 保存设置失败: {str(e)}")
    
    def restore_network_defaults(self):
        """恢复网络监控默认设置"""
        try:
            # 设置默认值
            default_values = {
                "check_interval": 10,
                "timeout": 5,
                "consecutive_failures": 3
            }
            
            self.check_interval_var.set(str(default_values["check_interval"]))
            self.timeout_var.set(str(default_values["timeout"]))
            self.consecutive_failures_var.set(str(default_values["consecutive_failures"]))
            
            self.update_network_status_label("✅ 已恢复默认设置")
            
        except Exception as e:
            self.update_network_status_label(f"❌ 恢复默认设置失败: {str(e)}")
    
    def update_network_status_label(self, message):
        """更新网络设置状态标签"""
        try:
            self.network_status_label.config(text=message)
        except:
            pass 