#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor GUI 版本
集成 tkinter 界面的聊天弹窗监控器
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import sys
import os
import re
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入原有的监控模块
from main_monitor_dynamic import (
    get_config, play_sound, check_process, screenshot, 
    detect_and_ocr_with_yolo, YOLOModelManager, TARGET_CONTACTS, FUZZY_MATCHER,
    config_manager
)

# 导入网络监控模块
from network_monitor import NetworkMonitor

class ChatMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatMonitor")
        self.root.geometry("600x750")
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
        self.main_frame.rowconfigure(2, weight=1)
        
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
            text="状态: 正在启动...",
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
            width=60,
            height=20,
            font=("SF Mono", 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        # 控制按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, pady=(10, 0))
        
        # 监控开关框架
        self.switch_frame = ttk.LabelFrame(self.main_frame, text="监控开关", padding="5")
        self.switch_frame.grid(row=4, column=0, pady=(10, 0), sticky="ew")
        
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
        self.control_button_frame.grid(row=5, column=0, pady=(10, 0))
        
        # 开始/停止按钮
        self.start_stop_button = ttk.Button(
            self.control_button_frame,
            text="开始监控",
            command=self.toggle_monitoring
        )
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 发信人设置按钮
        self.contacts_button = ttk.Button(
            self.control_button_frame,
            text="发信人设置",
            command=self.open_contacts_settings
        )
        self.contacts_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 网络监控频率设置按钮
        self.network_button = ttk.Button(
            self.control_button_frame,
            text="网络监控频率",
            command=self.open_network_settings
        )
        self.network_button.pack(side=tk.LEFT, padx=(0, 10))
        
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
        
        # 监控状态
        self.monitoring = False
        self.monitor_thread = None
        self.yolo_manager = None
        self.last_reply_time = 0
        self.detection_count = 0
        
        # 监控开关状态
        self.app_monitor_enabled = True
        self.network_monitor_enabled = True
        
        # 网络监控器
        self.network_monitor = None
        
        # 初始化配置
        self.init_monitoring()
        
        # 启动监控
        self.start_monitoring()
    
    def init_monitoring(self):
        """初始化监控配置"""
        try:
            conf = get_config()
            yolo_conf = conf.get("yolo", {})
            yolo_enabled = yolo_conf.get("enabled", True)
            yolo_model_path = yolo_conf.get("model_path", "models/best.pt")
            yolo_confidence = yolo_conf.get("confidence", 0.35)
            
            self.add_log_message(f"YOLO配置: enabled={yolo_enabled}, path={yolo_model_path}")
            
            if yolo_enabled:
                # 检查文件是否存在
                if not os.path.exists(yolo_model_path):
                    self.add_log_message(f"错误: YOLO模型文件不存在: {yolo_model_path}")
                    return
                
                try:
                    self.yolo_manager = YOLOModelManager(yolo_model_path, yolo_confidence)
                    success = self.yolo_manager.initialized
                    self.add_log_message(f"YOLO模型初始化: {'成功' if success else '失败'}")
                    
                    if not success:
                        self.add_log_message("YOLO模型初始化失败，可能原因:")
                        self.add_log_message("1. 模型文件损坏")
                        self.add_log_message("2. ultralytics库版本不兼容")
                        self.add_log_message("3. 模型格式不正确")
                except Exception as e:
                    self.add_log_message(f"YOLO模型初始化异常: {str(e)}")
            else:
                self.add_log_message("YOLO检测已禁用")
            
            self.add_log_message("监控配置初始化完成")
            
            # 初始化网络监控器
            try:
                self.network_monitor = NetworkMonitor(
                    consecutive_failures=3,
                    check_interval=60,
                    timeout=10,
                    tolerance_minutes=15
                )
                self.add_log_message("网络监控器初始化成功")
            except Exception as e:
                self.add_log_message(f"网络监控器初始化失败: {str(e)}")
                self.network_monitor = None
            
        except Exception as e:
            self.add_log_message(f"配置初始化失败: {str(e)}")
    
    def start_monitoring(self):
        """启动监控"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.run_monitor, daemon=True)
            self.monitor_thread.start()
            
            self.update_status_label()
            self.start_stop_button.config(text="停止监控")
            self.add_log_message("监控已启动")
    
    def run_monitor(self):
        """运行监控器"""
        try:
            conf = get_config()
            app_name = conf.get("chat_app", {}).get("name", "WeChat")
            check_interval = conf.get("monitor", {}).get("check_interval", 3)
            reply_wait = conf.get("monitor", {}).get("reply_wait", 60)
            ocr_conf = conf.get("ocr", {}).get("tesseract", {})
            ocr_lang = ocr_conf.get("lang", "chi_sim+eng")
            ocr_psm = ocr_conf.get("config", "--psm 6").split()[-1]
            debug_verbose = conf.get("debug", {}).get("verbose", False)
            
            while self.monitoring:
                try:
                    # 检查是否有任何监控启用
                    if not self.app_monitor_enabled and not self.network_monitor_enabled:
                        time.sleep(check_interval)
                        continue
                    
                    # 应用监控逻辑
                    if self.app_monitor_enabled:
                        # 检查进程
                        if not check_process(app_name):
                            self.add_log_message(f"未找到 {app_name} 进程")
                            play_sound("error")  # 播放错误声音
                            time.sleep(check_interval)
                            continue
                        
                        # 截图
                        img = screenshot()
                        if img is None:
                            self.add_log_message("截图失败")
                            play_sound("error")  # 播放错误声音
                            time.sleep(check_interval)
                            continue
                        
                        self.detection_count += 1
                        results = []
                        
                        # YOLO检测
                        if self.yolo_manager and self.yolo_manager.initialized:
                            results = detect_and_ocr_with_yolo(img, self.yolo_manager, ocr_lang, ocr_psm)
                            if debug_verbose and results:
                                self.add_log_message(f"检测到 {len(results)} 个弹窗")
                        
                        # 处理检测结果
                        for result in results:
                            text = result['text']
                            if text and FUZZY_MATCHER:
                                first_line = text.splitlines()[0] if text else ""
                                match_result = FUZZY_MATCHER.match_sender(first_line)
                                if match_result:
                                    contact, sender, similarity = match_result
                                    now = time.time()
                                    if now - self.last_reply_time > reply_wait:
                                        self.add_detection_result(
                                            app_name, 
                                            f"目标联系人: {contact}（识别为: {sender}, 相似度: {similarity:.2f}）",
                                            result.get('confidence'),
                                            "YOLO+OCR"
                                        )
                                        play_sound("contact")
                                        self.last_reply_time = now
                                        break
                    
                    # 网络监控逻辑
                    if self.network_monitor_enabled and self.network_monitor:
                        try:
                            # 执行网络检测
                            check_result = self.network_monitor.perform_network_check()
                            self.network_monitor.update_network_status(check_result)
                            
                            # 检查是否有网络警报
                            alert = self.network_monitor.get_alert()
                            if alert:
                                self.add_detection_result(
                                    "网络监控",
                                    f"网络连接异常: {alert.get('message', '未知错误')}",
                                    None,
                                    "网络检测"
                                )
                                play_sound("default")
                            
                            # 如果网络检测失败，记录日志并播放声音
                            if not check_result["success"]:
                                self.add_log_message(f"网络检测失败: 通过 {check_result['passed_tests']}/{check_result['total_tests']} 个测试")
                                play_sound("warning")  # 播放错误声音
                            
                        except Exception as e:
                            self.add_log_message(f"网络监控错误: {str(e)}")
                    
                    time.sleep(check_interval)
                    
                except Exception as e:
                    self.add_log_message(f"监控循环错误: {str(e)}")
                    time.sleep(check_interval)
                    
        except Exception as e:
            self.add_log_message(f"监控器启动失败: {str(e)}")
    
    def toggle_monitoring(self):
        """切换监控状态"""
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def on_app_monitor_toggle(self):
        """应用监控开关切换"""
        self.app_monitor_enabled = self.app_monitor_var.get()
        status = "启用" if self.app_monitor_enabled else "禁用"
        self.add_log_message(f"应用监控已{status}")
        
        if self.monitoring:
            self.update_status_label()
    
    def on_network_monitor_toggle(self):
        """网络监控开关切换"""
        self.network_monitor_enabled = self.network_monitor_var.get()
        status = "启用" if self.network_monitor_enabled else "禁用"
        self.add_log_message(f"网络监控已{status}")
        
        if self.monitoring:
            self.update_status_label()
    
    def update_status_label(self):
        """更新状态标签"""
        status_parts = []
        if self.app_monitor_enabled:
            status_parts.append("应用监控")
        if self.network_monitor_enabled:
            status_parts.append("网络监控")
        
        if status_parts:
            status_text = f"状态: 监控中 ({', '.join(status_parts)})"
        else:
            status_text = "状态: 监控已停止 (所有监控已禁用)"
        
        self.status_label.config(text=status_text)
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        self.status_label.config(text="状态: 监控已停止")
        self.start_stop_button.config(text="开始监控")
        self.add_log_message("监控已停止")
    
    def add_detection_result(self, app_name, content, confidence=None, detection_method=None):
        """添加检测结果到显示区"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 启用文本框编辑
        self.text_area.config(state=tk.NORMAL)
        
        # 插入新内容到顶部
        result_text = f"[{timestamp}] {app_name}\n"
        if detection_method:
            result_text += f"检测方法: {detection_method}\n"
        if confidence:
            result_text += f"置信度: {confidence:.2f}\n"
        result_text += f"内容: {content}\n"
        result_text += "-" * 60 + "\n\n"
        
        # 在开头插入新内容
        self.text_area.insert("1.0", result_text)
        
        # 限制显示行数（保持最近200行）
        lines = self.text_area.get("1.0", tk.END).split('\n')
        if len(lines) > 200:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", '\n'.join(lines[:200]))
        
        # 禁用文本框编辑
        self.text_area.config(state=tk.DISABLED)
        
        # 更新状态
        self.status_label.config(text=f"状态: 最后检测 {timestamp}")
    
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
    
    def open_contacts_settings(self):
        """打开发信人设置窗口"""
        try:
            # 创建设置窗口
            settings_window = tk.Toplevel(self.root)
            settings_window.title("发信人设置")
            settings_window.resizable(True, True)
            settings_window.transient(self.root)  # 设置为主窗口的子窗口
            settings_window.grab_set()  # 模态窗口
            
            # 居中显示
            settings_window.update_idletasks()
            x = (settings_window.winfo_screenwidth() // 2) - (settings_window.winfo_width() // 2)
            y = (settings_window.winfo_screenheight() // 2) - (settings_window.winfo_height() // 2)
            settings_window.geometry(f"+{x}+{y}")
            
            # 创建界面
            self.create_contacts_settings_ui(settings_window)
            
            # 确保弹框显示在主窗口之上
            settings_window.lift()  # 提升到最顶层
            settings_window.focus_force()  # 强制设置焦点
            
            # 绑定窗口关闭事件，确保关闭时释放模态
            def on_closing():
                settings_window.grab_release()
                settings_window.destroy()
            
            settings_window.protocol("WM_DELETE_WINDOW", on_closing)
            
        except Exception as e:
            self.add_log_message(f"❌ 打开发信人设置失败: {str(e)}")
    
    def create_contacts_settings_ui(self, window):
        """创建发信人设置界面"""
        # 配置窗口网格权重，确保自适应
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        # 主框架
        main_frame = ttk.Frame(window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)  # 让文本框区域可以扩展
        
        # 标题
        title_label = ttk.Label(main_frame, text="监控发信人设置", font=("Arial", 16, "bold"))
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
        contact_text = tk.Text(main_frame, height=8, width=50, font=("Arial", 11))
        contact_text.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        
        # 配置文本框的滚动条
        text_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=contact_text.yview)
        text_scrollbar.grid(row=4, column=2, sticky="ns")
        contact_text.configure(yscrollcommand=text_scrollbar.set)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # 状态标签
        status_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # 加载默认值
        self.load_contacts_to_text(contact_text, status_label)
        
        # 保存按钮
        save_button = ttk.Button(button_frame, text="保存设置", 
                                command=lambda: self.save_contacts_from_text(contact_text, status_label, window))
        save_button.pack(side="left", padx=(0, 10))
        
        # 重置按钮
        reset_button = ttk.Button(button_frame, text="重置为默认", 
                                command=lambda: self.load_contacts_to_text(contact_text, status_label))
        reset_button.pack(side="left", padx=(0, 10))
        
        # 清空按钮
        clear_button = ttk.Button(button_frame, text="清空", 
                                command=lambda: self.clear_contacts_text(contact_text, status_label))
        clear_button.pack(side="left", padx=(0, 10))
        
        # 取消按钮
        cancel_button = ttk.Button(button_frame, text="取消", command=window.destroy)
        cancel_button.pack(side="left")
        
        # 让窗口自适应内容大小
        window.update_idletasks()
        window.geometry("")  # 清除任何固定大小设置
    
    def load_contacts_to_text(self, text_widget, status_label):
        """加载联系人到文本框"""
        try:
            conf = get_config()
            contacts = conf.get("chat_app", {}).get("target_contacts", ["微信", "QQ"])
            
            if isinstance(contacts, list):
                contacts_text = ", ".join(contacts)
            else:
                contacts_text = str(contacts)
            
            text_widget.delete(1.0, tk.END)
            text_widget.insert(1.0, contacts_text)
            
            self.update_settings_status_label(status_label, f"已加载 {len(contacts) if isinstance(contacts, list) else 1} 个发信人")
            
        except Exception as e:
            self.update_settings_status_label(status_label, f"加载失败: {str(e)}")
    
    def parse_contacts(self, text):
        """解析发信人文本"""
        if not text.strip():
            return []
        
        # 分割文本，支持中英文逗号
        contacts = []
        for contact in re.split(r'[,，]', text):
            contact = contact.strip()
            if contact:
                contacts.append(contact)
        
        return contacts
    
    def save_contacts_from_text(self, text_widget, status_label, window):
        """从文本框保存发信人设置"""
        try:
            # 获取输入文本
            text = text_widget.get(1.0, tk.END).strip()
            
            # 解析发信人
            contacts = self.parse_contacts(text)
            
            if not contacts:
                from tkinter import messagebox
                messagebox.showwarning("警告", "请输入至少一个发信人姓名")
                return
            
            # 读取现有配置
            conf = get_config()
            
            # 更新发信人配置
            if "chat_app" not in conf:
                conf["chat_app"] = {}
            
            conf["chat_app"]["target_contacts"] = contacts
            
            # 保存配置文件
            config_manager.save_config(conf)
            
            # 立即更新内存中的目标联系人
            from main_monitor_dynamic import update_target_contacts
            update_target_contacts(contacts)
            
            self.update_settings_status_label(status_label, f"已保存 {len(contacts)} 个发信人: {', '.join(contacts)}")
            self.add_log_message(f"✅ 发信人设置已更新: {', '.join(contacts)}")
            
            from tkinter import messagebox
            messagebox.showinfo("成功", f"已保存 {len(contacts)} 个发信人设置，监控将立即生效")
            
            # 关闭设置窗口
            window.destroy()
            
        except Exception as e:
            error_msg = f"保存配置文件失败: {str(e)}"
            self.update_settings_status_label(status_label, error_msg)
            from tkinter import messagebox
            messagebox.showerror("错误", error_msg)
    
    def clear_contacts_text(self, text_widget, status_label):
        """清空发信人文本框"""
        text_widget.delete(1.0, tk.END)
        self.update_settings_status_label(status_label, "已清空发信人列表")
    
    def update_settings_status_label(self, status_label, message):
        """更新设置窗口状态标签"""
        status_label.config(text=message)
        status_label.winfo_toplevel().update_idletasks()
    
    def open_network_settings(self):
        """打开网络监控频率设置窗口"""
        try:
            # 创建新窗口
            settings_window = tk.Toplevel(self.root)
            settings_window.title("网络监控频率设置")
            settings_window.resizable(True, True)
            
            # 设置窗口层级
            settings_window.transient(self.root)
            settings_window.grab_set()
            settings_window.lift()
            settings_window.focus_force()
            
            # 创建界面
            self.create_network_settings_ui(settings_window)
            
            # 设置关闭事件
            def on_closing():
                settings_window.grab_release()
                settings_window.destroy()
            settings_window.protocol("WM_DELETE_WINDOW", on_closing)
            
        except Exception as e:
            self.add_log_message(f"❌ 打开网络监控设置失败: {str(e)}")
    
    def create_network_settings_ui(self, window):
        """创建网络监控设置界面"""
        # 配置窗口网格权重，确保自适应
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        # 主框架
        main_frame = ttk.Frame(window, padding="20")
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

• 容错时间：连续失败后等待的时间（分钟）
  推荐值：0.1-1分钟，值越小响应越快

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
        
        # 容错时间
        ttk.Label(params_frame, text="容错时间（分钟）:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.tolerance_minutes_var = tk.StringVar()
        tolerance_minutes_entry = ttk.Entry(params_frame, textvariable=self.tolerance_minutes_var, width=15)
        tolerance_minutes_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky="w")
        
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
            command=lambda: self.save_network_settings(window)
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
            command=window.destroy
        )
        cancel_button.pack(side=tk.RIGHT)
        
        # 让窗口自适应内容大小
        window.update_idletasks()
        window.geometry("")  # 清除任何固定大小设置
    
    def load_network_settings(self):
        """加载当前网络监控设置"""
        try:
            conf = get_config()
            network_config = conf.get("network", {})
            
            # 设置当前值
            self.check_interval_var.set(str(network_config.get("check_interval", 60)))
            self.timeout_var.set(str(network_config.get("timeout", 10)))
            self.consecutive_failures_var.set(str(network_config.get("consecutive_failures", 3)))
            self.tolerance_minutes_var.set(str(network_config.get("tolerance_minutes", 0.1)))
            
            self.update_network_settings_status_label("✅ 已加载当前设置")
            
        except Exception as e:
            self.update_network_settings_status_label(f"❌ 加载设置失败: {str(e)}")
    
    def save_network_settings(self, window):
        """保存网络监控设置"""
        try:
            # 获取输入值
            check_interval = float(self.check_interval_var.get())
            timeout = float(self.timeout_var.get())
            consecutive_failures = int(self.consecutive_failures_var.get())
            tolerance_minutes = float(self.tolerance_minutes_var.get())
            
            # 验证输入
            if check_interval < 1 or timeout < 1 or consecutive_failures < 1 or tolerance_minutes < 0.01:
                self.update_network_settings_status_label("❌ 参数值无效，请检查输入")
                return
            
            # 保存到配置文件
            conf = get_config()
            if "network" not in conf:
                conf["network"] = {}
            
            conf["network"].update({
                "check_interval": check_interval,
                "timeout": timeout,
                "consecutive_failures": consecutive_failures,
                "tolerance_minutes": tolerance_minutes
            })
            
            config_manager.save_config(conf)
            
            self.update_network_settings_status_label("✅ 设置已保存，监控将立即生效")
            
            # 显示成功消息
            from tkinter import messagebox
            messagebox.showinfo("成功", "网络监控频率设置已保存，监控将立即生效")
            
            # 关闭窗口
            window.destroy()
            
        except ValueError:
            self.update_network_settings_status_label("❌ 输入格式错误，请检查数值")
        except Exception as e:
            self.update_network_settings_status_label(f"❌ 保存设置失败: {str(e)}")
    
    def restore_network_defaults(self):
        """恢复网络监控默认设置"""
        try:
            # 设置默认值
            self.check_interval_var.set("60")
            self.timeout_var.set("10")
            self.consecutive_failures_var.set("3")
            self.tolerance_minutes_var.set("0.1")
            
            self.update_network_settings_status_label("✅ 已恢复默认设置")
            
        except Exception as e:
            self.update_network_settings_status_label(f"❌ 恢复默认设置失败: {str(e)}")
    
    def update_network_settings_status_label(self, message):
        """更新网络设置状态标签"""
        self.network_status_label.config(text=message)
        self.network_status_label.winfo_toplevel().update_idletasks()
    
    def close_program(self):
        """关闭程序"""
        if self.monitoring:
            self.stop_monitoring()
        
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
    
    app = ChatMonitorGUI(root)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main() 