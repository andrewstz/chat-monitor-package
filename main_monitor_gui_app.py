#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor GUI 版本 - 用于打包成 .app
集成 tkinter 界面的聊天弹窗监控器
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import sys
import os
from datetime import datetime

# 导入原有的监控模块
from main_monitor_dynamic import (
    get_config, play_sound, check_process, screenshot, 
    detect_and_ocr_with_yolo, YOLOModelManager, TARGET_CONTACTS, FUZZY_MATCHER,
    config_manager
)

# 导入配置管理器
from config_manager import get_config_manager

# 导入GUI设置模块
from gui.contacts_settings import ContactsSettingsWindow
from gui.network_settings import NetworkSettingsWindow
from gui.popup_settings import PopupSettingsWindow

def debug_log(msg):
    try:
        with open("/tmp/chatmonitor_debug.log", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        pass  # 避免日志写入影响主流程

def clear_debug_log():
    """清空调试日志文件"""
    try:
        with open("/tmp/chatmonitor_debug.log", "w", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] === GUI程序启动，日志已清空 ===\n")
        print("✅ 调试日志已清空")
    except Exception as e:
        print(f"清空调试日志失败: {e}")

def configure_tesseract():
    """配置tesseract路径"""
    import subprocess
    
    debug_log("[TESSERACT] 开始配置tesseract路径")
    
    # 可能的tesseract路径
    possible_paths = [
        "/usr/local/bin/tesseract",  # Homebrew安装
        "/opt/homebrew/bin/tesseract",  # Apple Silicon Homebrew
        "/usr/bin/tesseract",  # 系统安装
        "tesseract",  # PATH中的tesseract
    ]
    
    # 如果是打包后的应用程序，尝试从系统PATH查找
    if getattr(sys, 'frozen', False):
        try:
            # 尝试使用which命令查找tesseract
            result = subprocess.run(['which', 'tesseract'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                tesseract_path = result.stdout.strip()
                possible_paths.insert(0, tesseract_path)
                debug_log(f"[TESSERACT] 通过which找到tesseract: {tesseract_path}")
        except Exception as e:
            debug_log(f"[TESSERACT] which命令失败: {str(e)}")
    
    # 测试每个路径
    for path in possible_paths:
        try:
            if path == "tesseract":
                # 测试PATH中的tesseract
                result = subprocess.run(['tesseract', '--version'], 
                                      capture_output=True, text=True, timeout=5)
            else:
                # 测试具体路径
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                debug_log(f"[TESSERACT] ✅ 找到可用的tesseract: {path}")
                import pytesseract
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        except Exception as e:
            debug_log(f"[TESSERACT] 测试路径失败 {path}: {str(e)}")
            continue
    
    debug_log("[TESSERACT] ❌ 未找到可用的tesseract")
    return False

class LoadingWindow:
    """启动加载窗口"""
    def __init__(self, root):
        self.root = root
        self.root.title("ChatMonitor - 启动中")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # 居中显示
        self.root.geometry("+%d+%d" % (
            (self.root.winfo_screenwidth() // 2) - 200,
            (self.root.winfo_screenheight() // 2) - 100
        ))
        
        # 主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text="ChatMonitor",
            font=("SF Pro Display", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 加载提示
        self.loading_label = ttk.Label(
            main_frame,
            text="正在初始化...",
            font=("SF Pro Text", 12)
        )
        self.loading_label.pack(pady=(0, 10))
        
        # 进度条
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=(0, 10))
        self.progress.start()
        
        # 详细状态
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=("SF Mono", 10),
            foreground="gray"
        )
        self.status_label.pack()
        
        # 设置窗口层级（移除置顶，让窗口行为更正常）
        self.root.lift()
        
    def update_status(self, message):
        """更新状态信息"""
        self.status_label.config(text=message)
        self.root.update()
        
    def update_loading(self, message):
        """更新加载提示"""
        self.loading_label.config(text=message)
        self.root.update()

class ChatMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatMonitor")
        # 不设置固定大小，让窗口自适应内容
        self.root.resizable(True, True)
        
        # 设置窗口图标
        self.set_window_icon()
        
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
        self.button_frame.grid(row=3, column=0, pady=(10, 0), sticky="ew")
        self.button_frame.columnconfigure(0, weight=1)  # 让按钮框架可以扩展
        
        # 开始/停止按钮
        self.start_stop_button = ttk.Button(
            self.button_frame,
            text="开始监控",
            command=self.toggle_monitoring
        )
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # 清空按钮
        self.clear_button = ttk.Button(
            self.button_frame,
            text="清空记录",
            command=self.clear_logs
        )
        self.clear_button.grid(row=0, column=1, padx=(0, 10))
        
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
        
        # 初始化设置窗口（必须在按钮创建之前）
        self.contacts_settings = ContactsSettingsWindow(self.root, self.on_contacts_saved)
        self.network_settings = NetworkSettingsWindow(self.root, self.on_network_saved)
        self.popup_settings = PopupSettingsWindow(self.root, self.on_popup_saved)
        
        # 发信人设置按钮
        self.contacts_button = ttk.Button(
            self.button_frame,
            text="发信人设置",
            command=self.contacts_settings.open_contacts_settings
        )
        self.contacts_button.grid(row=0, column=2, padx=(0, 10))
        
        # 网络监控频率设置按钮
        self.network_button = ttk.Button(
            self.button_frame,
            text="网络监控频率",
            command=self.network_settings.open_network_settings
        )
        self.network_button.grid(row=0, column=3, padx=(0, 10))
        
        # 弹框监控设置按钮
        self.popup_button = ttk.Button(
            self.button_frame,
            text="弹框监控设置",
            command=self.popup_settings.open_popup_settings
        )
        self.popup_button.grid(row=0, column=4, padx=(0, 10))
        
        # 关闭按钮
        self.close_button = ttk.Button(
            self.button_frame,
            text="关闭程序",
            command=self.close_program
        )
        self.close_button.grid(row=0, column=5)
        
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
        

        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        
        # 让窗口自适应内容大小
        self.root.update_idletasks()
        self.root.geometry("")  # 清除任何固定大小设置
        
        # 初始化配置
        self.init_monitoring()
        
        # 更新初始状态
        self.update_status_label()
        
        # 自动启动监控
        self.auto_start_monitoring()
    
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 尝试多种图标路径（优先 assets 目录）
            icon_paths = [
                "assets/icons/icon.png",  # assets/icons 目录 PNG
                "assets/icons/icon_256x256.png",  # 高分辨率 PNG
                "assets/icons/icon.icns",  # assets/icons 目录 ICNS
                "assets/icon.png",  # assets 目录 PNG
                "assets/icon.icns",  # assets 目录 ICNS
                "icons/icon.png",  # icons 目录 PNG
                "icons/icon.icns",  # icons 目录 ICNS
                "icon.png",  # 当前目录 PNG（兼容性）
                "icon.icns",  # 当前目录 ICNS（兼容性）
                os.path.join(os.path.dirname(__file__), "assets", "icons", "icon.png"),
                os.path.join(os.path.dirname(__file__), "assets", "icons", "icon.icns"),
                os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
                os.path.join(os.path.dirname(__file__), "assets", "icon.icns"),
                os.path.join(os.path.dirname(__file__), "icons", "icon.png"),
                os.path.join(os.path.dirname(__file__), "icons", "icon.icns"),
                os.path.join(os.path.dirname(__file__), "icon.png"),
                os.path.join(os.path.dirname(__file__), "icon.icns"),
            ]
            
            # 如果是打包后的应用，尝试从Resources目录加载
            if getattr(sys, 'frozen', False):
                # PyInstaller 临时目录
                if hasattr(sys, '_MEIPASS'):
                    meipass_icon = os.path.join(sys._MEIPASS, "icon.icns")
                    icon_paths.insert(0, meipass_icon)
                
                # macOS .app Resources 目录
                app_dir = os.path.dirname(sys.executable)
                resources_icon = os.path.join(app_dir, "..", "Resources", "icon.icns")
                icon_paths.insert(0, resources_icon)
            
            # 尝试设置图标
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        # 方法1: 使用 iconphoto (适用于 PNG 文件，在 macOS 上效果更好)
                        if icon_path.lower().endswith('.png'):
                            from PIL import Image, ImageTk
                            img = Image.open(icon_path)
                            photo = ImageTk.PhotoImage(img)
                            self.root.iconphoto(True, photo)
                            # 强制刷新窗口
                            self.root.update_idletasks()
                            debug_log(f"[ICON] 成功设置图标 (iconphoto): {icon_path}")
                            break
                        else:
                            # 方法2: 使用 iconbitmap (适用于 .icns 文件)
                            self.root.iconbitmap(icon_path)
                            debug_log(f"[ICON] 成功设置图标 (iconbitmap): {icon_path}")
                            break
                    except Exception as e:
                        debug_log(f"[ICON] 设置图标失败 {icon_path}: {str(e)}")
                        continue
            
            # 如果没有找到图标文件，尝试使用系统默认图标
            debug_log("[ICON] 未找到图标文件，使用系统默认图标")
            
        except Exception as e:
            debug_log(f"[ICON] 设置图标失败: {str(e)}")
            # 图标设置失败不影响程序运行
        
        # 无论图标设置是否成功，都要绑定窗口事件
        debug_log("[ICON] 开始绑定窗口事件")
        
        # 绑定窗口显示完成事件，确保 GUI 完全加载后再启动监控。 <Map> 事件绑定
        debug_log("[ICON] 绑定窗口显示事件")
        self.root.bind('<Map>', self.on_window_ready)
        # 如果窗口已经显示，直接启动
        if self.root.winfo_viewable():
            debug_log("[ICON] 窗口已可见，延迟100ms启动监控")
            # 双重保障 如果窗口已经可见，延迟 100ms 启动
            self.root.after(100, self.auto_start_monitoring)
        else:
            debug_log("[ICON] 窗口未可见，等待Map事件")
    
    def on_window_ready(self, event):
        """窗口显示完成事件回调"""
        debug_log("[WINDOW_READY] 窗口显示完成事件触发")
        # 解绑事件，避免重复调用
        self.root.unbind('<Map>')
        # 延迟一小段时间确保 GUI 完全渲染
        # 双重保障 如果窗口还未显示，等待 <Map> 事件后延迟 500ms 启动
        debug_log("[WINDOW_READY] 延迟500ms启动监控")
        self.root.after(500, self.auto_start_monitoring)
    
    def init_monitoring(self):
        """初始化监控配置"""
        debug_log("[INIT] 开始初始化监控配置")
        try:
            # 使用统一的配置管理
            from config_manager import get_config_manager
            config_manager = get_config_manager()
            yolo_config = config_manager.get_yolo_config()
            
            yolo_enabled = yolo_config["enabled"]
            yolo_model_path = yolo_config["model_path"]
            yolo_confidence = yolo_config["confidence"]
            disable_reason = yolo_config["disable_reason"]
            
            debug_log(f"[INIT] YOLO配置: enabled={yolo_enabled}, model_path={yolo_model_path}, confidence={yolo_confidence}")
            if disable_reason:
                debug_log(f"[INIT] YOLO禁用原因: {disable_reason}")
            
            self.add_log_message(f"YOLO配置: enabled={yolo_enabled}, path={yolo_model_path}")
            
            if yolo_enabled:
                debug_log(f"[INIT] 开始初始化YOLO模型: {yolo_model_path}")
                
                # 解析模型路径
                resolved_model_path = self._resolve_model_path(yolo_model_path)
                if not resolved_model_path:
                    debug_log(f"[INIT] ❌ 无法解析YOLO模型路径: {yolo_model_path}")
                    self.add_log_message(f"错误: 无法找到YOLO模型文件: {yolo_model_path}")
                    return
                
                debug_log(f"[INIT] ✅ 解析后的模型路径: {resolved_model_path}")
                # 检查文件是否存在
                if not os.path.exists(resolved_model_path):
                    debug_log(f"[INIT] ❌ YOLO模型文件不存在: {resolved_model_path}")
                    self.add_log_message(f"错误: YOLO模型文件不存在: {resolved_model_path}")
                    return
                
                debug_log(f"[INIT] ✅ YOLO模型文件存在: {resolved_model_path}")
                try:
                    debug_log("[INIT] 创建YOLOModelManager实例...")
                    self.yolo_manager = YOLOModelManager(resolved_model_path, yolo_confidence)
                    success = self.yolo_manager.initialized
                    debug_log(f"[INIT] YOLO模型初始化结果: {'成功' if success else '失败'}")
                    self.add_log_message(f"YOLO模型初始化: {'成功' if success else '失败'}")
                    
                    if not success:
                        debug_log("[INIT] YOLO模型初始化失败")
                        self.add_log_message("YOLO模型初始化失败，可能原因:")
                        self.add_log_message("1. 模型文件损坏")
                        self.add_log_message("2. ultralytics库版本不兼容")
                        self.add_log_message("3. 模型格式不正确")
                except Exception as e:
                    debug_log(f"[INIT] YOLO模型初始化异常: {str(e)}")
                    self.add_log_message(f"YOLO模型初始化异常: {str(e)}")
            else:
                self.add_log_message("YOLO检测已禁用")
            
            self.add_log_message("监控配置初始化完成")
            
        except Exception as e:
            self.add_log_message(f"配置初始化失败: {str(e)}")
    
    def _resolve_model_path(self, model_path):
        """解析模型路径，支持打包后的应用程序"""
        debug_log(f"[路径解析] 开始解析模型路径: {model_path}")
        possible_paths = []
        
        # 1. PyInstaller专用临时目录
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            meipass_path = os.path.join(sys._MEIPASS, model_path)
            possible_paths.append(meipass_path)
            debug_log(f"[路径解析] 尝试_MEIPASS路径: {meipass_path}")
        
        # 2. macOS .app Resources
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
            resources_path = os.path.join(app_dir, "..", "Resources", model_path)
            possible_paths.append(resources_path)
            debug_log(f"[路径解析] 尝试Resources路径: {resources_path}")
        
        # 3. 用户目录
        user_home = os.path.expanduser("~")
        user_models_path = os.path.join(user_home, "ChatMonitor", "models", os.path.basename(model_path))
        possible_paths.append(user_models_path)
        debug_log(f"[路径解析] 尝试用户目录: {user_models_path}")
        
        # 4. 当前工作目录
        cwd_path = os.path.join(os.getcwd(), model_path)
        possible_paths.append(cwd_path)
        debug_log(f"[路径解析] 尝试当前工作目录: {cwd_path}")
        
        # 5. 脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_models_path = os.path.join(script_dir, model_path)
        possible_paths.append(script_models_path)
        debug_log(f"[路径解析] 尝试脚本目录: {script_models_path}")
        
        # 6. 绝对路径
        abs_path = os.path.abspath(model_path)
        possible_paths.append(abs_path)
        debug_log(f"[路径解析] 尝试绝对路径: {abs_path}")
        
        # 检查所有路径
        for path in possible_paths:
            exists = os.path.exists(path)
            debug_log(f"[路径解析] 检查: {path} - {'存在' if exists else '不存在'}")
            if exists:
                debug_log(f"[路径解析] ✅ 找到模型文件: {path}")
                return path
        
        debug_log(f"[路径解析] ❌ 未找到模型文件: {model_path}")
        return None
    
    def start_monitoring(self):
        """启动监控"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.run_monitor, daemon=True)
            self.monitor_thread.start()
            
            self.start_stop_button.config(text="停止监控")
            self.add_log_message("监控已启动")
            self.update_status_label()
    
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
            
            # 检查权限
            self.safe_add_log_message("检查系统权限...")
            
            # 检查屏幕录制权限
            try:
                test_img = screenshot()
                if test_img is None:
                    self.safe_add_log_message("⚠️ 屏幕录制权限不足，请在系统偏好设置中允许屏幕录制")
                    self.safe_add_log_message("路径：系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制")
                    return
                else:
                    self.safe_add_log_message("✅ 屏幕录制权限正常")
            except Exception as e:
                self.safe_add_log_message(f"⚠️ 屏幕录制权限检查失败: {str(e)}")
                return
            
            # 检查目标应用进程（启动时检查，但不阻止程序运行）
            if not check_process(app_name):
                self.safe_add_log_message(f"⚠️ 未找到目标应用: {app_name}")
                self.safe_add_log_message("请确保目标应用正在运行")
                # 播放进程不存在的提醒音
                try:
                    play_sound("error")
                    self.safe_add_log_message("🔊 播放进程不存在提醒音")
                except Exception as e:
                    self.safe_add_log_message(f"❌ 进程不存在提醒音播放失败: {str(e)}")
                self.safe_add_log_message("程序将继续运行，等待目标应用启动...")
            else:
                self.safe_add_log_message(f"✅ 目标应用已运行: {app_name}")
            
            self.safe_add_log_message(f"✅ 开始监控应用: {app_name}")
            
            while self.monitoring:
                try:
                    # 独立监控逻辑 - 每个监控功能独立运行
                    
                    # 1. 网络监控（独立运行）
                    if self.network_monitor_enabled:
                        try:
                            from main_monitor_dynamic import check_network_with_alert
                            check_network_with_alert()
                        except Exception as e:
                            self.safe_add_log_message(f"网络监控检查失败: {str(e)}")
                    
                    # 2. 应用监控（独立运行）
                    if self.app_monitor_enabled:
                        # 检查进程
                        if not check_process(app_name):
                            self.safe_add_log_message(f"未找到 {app_name} 进程")
                            # 添加进程退出的声音提醒
                            try:
                                play_sound("error")
                                self.safe_add_log_message("🔊 播放进程退出提醒音")
                            except Exception as e:
                                self.safe_add_log_message(f"❌ 进程退出提醒音播放失败: {str(e)}")
                            time.sleep(check_interval)
                            continue
                    
                    # 3. 弹框监控（默认运行）
                    # 读取弹框设置
                    try:
                        conf = config_manager.load_config()
                        monitor_conf = conf.get("monitor", {})
                        popup_conf = conf.get("popup_settings", {})
                        
                        # 获取检测间隔
                        current_check_interval = monitor_conf.get("check_interval", 1)
                        fast_mode = popup_conf.get("fast_mode", False)
                        if fast_mode:
                            current_check_interval = 0.5
                        
                        # 获取提醒等待时间
                        current_reply_wait = monitor_conf.get("reply_wait", 5)
                        if fast_mode:
                            current_reply_wait = 3
                    except:
                        current_check_interval = check_interval
                        current_reply_wait = reply_wait
                    
                    # 截图
                    img = screenshot()
                    if img is None:
                        self.safe_add_log_message("截图失败")
                        time.sleep(current_check_interval)
                        continue
                    
                    self.detection_count += 1
                    results = []
                    
                    # YOLO检测
                    if self.yolo_manager and self.yolo_manager.initialized:
                        results = detect_and_ocr_with_yolo(img, self.yolo_manager, ocr_lang, ocr_psm)
                        if results:
                            self.safe_add_log_message(f"🔍 检测到 {len(results)} 个弹窗")
                            # 添加详细的检测信息
                            for i, result in enumerate(results):
                                self.safe_add_log_message(f"🔍 弹窗 {i+1}: 置信度={result.get('confidence', 0):.2f}, 文本长度={len(result.get('text', ''))}")
                        elif self.detection_count % 10 == 0:
                            self.safe_add_log_message(f"🔍 第 {self.detection_count} 次检测：未发现弹窗")
                    else:
                        if self.detection_count % 10 == 0:
                            self.safe_add_log_message(f"⚠️ YOLO模型未初始化，跳过弹窗检测")
                            # 添加YOLO状态信息
                            if self.yolo_manager:
                                self.safe_add_log_message(f"⚠️ YOLO管理器状态: initialized={self.yolo_manager.initialized}")
                            else:
                                self.safe_add_log_message(f"⚠️ YOLO管理器为None")
                    
                    # 处理检测结果
                    for result in results:
                        text = result['text']
                        from main_monitor_dynamic import FUZZY_MATCHER as current_fuzzy_matcher
                        if text and current_fuzzy_matcher:
                            self.safe_add_log_message(f"🔍 检测到弹窗文本: {text[:100]}...")
                            first_line = text.splitlines()[0] if text else ""
                            self.safe_add_log_message(f"🔍 第一行文本: '{first_line}'")
                            
                            # 添加详细的匹配调试信息
                            self.safe_add_log_message(f"🔍 开始模糊匹配: '{first_line}'")
                            if current_fuzzy_matcher:
                                self.safe_add_log_message(f"🔍 模糊匹配器已初始化")
                                # 获取当前联系人列表
                                config_manager = get_config_manager()
                                conf = config_manager.load_config()
                                target_contacts = conf.get("chat_app", {}).get("target_contacts", [])
                                self.safe_add_log_message(f"🔍 当前联系人列表: {target_contacts}")
                            else:
                                self.safe_add_log_message(f"⚠️ 模糊匹配器未初始化")
                            
                            match_result = current_fuzzy_matcher.match_sender(first_line)
                            if match_result:
                                contact, sender, similarity = match_result
                                self.safe_add_log_message(f"✅ 第一行匹配成功: (相似度: {similarity:.2f})")
                            else:
                                self.safe_add_log_message(f"❌ 第一行匹配失败: '{first_line}'")
                                now = time.time()
                                time_since_last = now - self.last_reply_time
                                
                                if time_since_last > current_reply_wait:
                                    self.safe_add_detection_result(
                                        app_name, 
                                        f"目标联系人: {contact}（识别为: {sender}, 相似度: {similarity:.2f}）",
                                        result.get('confidence'),
                                        "YOLO+OCR"
                                    )
                                    self.safe_add_log_message(f"🔊 播放联系人提醒音")
                                    play_sound("contact")
                                    self.last_reply_time = now
                                    break
                                else:
                                    remaining_time = current_reply_wait - time_since_last
                                    self.safe_add_log_message(f"⏰ 距离上次提醒还有 {remaining_time:.1f} 秒，跳过本次提醒")
                        
                        # 4. 状态日志（定期输出监控状态）
                        if self.detection_count % 30 == 0:
                            status_msg = []
                            if self.app_monitor_enabled:
                                status_msg.append("应用监控: 开启")
                            else:
                                status_msg.append("应用监控: 关闭")
                            
                            if self.network_monitor_enabled:
                                status_msg.append("网络监控: 开启")
                            else:
                                status_msg.append("网络监控: 关闭")
                            
                            status_msg.append("弹框监控: 开启")  # 弹框监控始终开启
                            
                            if status_msg:
                                self.safe_add_log_message(f"📊 监控状态: {' | '.join(status_msg)}")
                        
                        # 4. 状态日志（定期输出监控状态）
                        if self.detection_count % 30 == 0:  # 每30次检测输出一次状态
                            status_msg = []
                            if self.app_monitor_enabled:
                                status_msg.append("应用监控: 开启")
                            else:
                                status_msg.append("应用监控: 关闭")
                            
                            if self.network_monitor_enabled:
                                status_msg.append("网络监控: 开启")
                            else:
                                status_msg.append("网络监控: 关闭")
                            
                            status_msg.append("弹框监控: 开启")  # 弹框监控始终开启
                            
                            if status_msg:
                                self.safe_add_log_message(f"📊 监控状态: {' | '.join(status_msg)}")
                        
                        # 5. 检查是否所有监控都关闭
                        if not self.app_monitor_enabled and not self.network_monitor_enabled:
                            if self.detection_count % 10 == 0:  # 每10次检测输出一次状态
                                self.safe_add_log_message("⚠️ 应用和网络监控已关闭，弹框监控仍在运行")
                    
                    # 使用动态检测间隔
                    final_sleep_time = current_check_interval if 'current_check_interval' in locals() else check_interval
                    time.sleep(final_sleep_time)
                    
                except Exception as e:
                    self.safe_add_log_message(f"监控循环错误: {str(e)}")
                    time.sleep(check_interval)
                    
        except Exception as e:
            self.safe_add_log_message(f"监控器启动失败: {str(e)}")
    
    def toggle_monitoring(self):
        """切换监控状态"""
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        self.start_stop_button.config(text="开始监控")
        self.add_log_message("监控已停止")
        self.update_status_label()
    
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
    
    def safe_add_log_message(self, message):
        """线程安全的日志消息添加"""
        try:
            # 使用 after 方法在主线程中执行 GUI 更新
            self.root.after(0, lambda: self.add_log_message(message))
        except Exception as e:
            # 如果 GUI 更新失败，至少记录到调试日志
            debug_log(f"[GUI_ERROR] 日志更新失败: {str(e)}")
    
    def safe_add_detection_result(self, app_name, content, confidence=None, detection_method=None):
        """线程安全的检测结果添加"""
        try:
            # 使用 after 方法在主线程中执行 GUI 更新
            self.root.after(0, lambda: self.add_detection_result(app_name, content, confidence, detection_method))
        except Exception as e:
            # 如果 GUI 更新失败，至少记录到调试日志
            debug_log(f"[GUI_ERROR] 检测结果更新失败: {str(e)}")
    
    def clear_logs(self):
        """清空检测记录"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 记录已清空")
    
    def auto_start_monitoring(self):
        """自动启动监控（确保 GUI 完全加载后执行）"""
        try:
            # 确保 GUI 完全更新
            self.root.update_idletasks()
            
            self.safe_add_log_message("🔄 准备自动启动监控...")
            debug_log("[AUTO_START] 开始自动启动监控")
            
            # 检查 GUI 是否完全加载
            if not self.root.winfo_exists():
                debug_log("[AUTO_START] 窗口不存在，取消自动启动")
                return
                
            self.start_monitoring()
            self.safe_add_log_message("✅ 监控已自动启动")
            debug_log("[AUTO_START] 监控自动启动成功")
        except Exception as e:
            self.safe_add_log_message(f"❌ 自动启动监控失败: {str(e)}")
            debug_log(f"[AUTO_START] 自动启动监控失败: {str(e)}")
    

    

    

    

    

    
    def update_status_label(self):
        """更新主状态标签，显示监控开关状态"""
        try:
            app_status = "开启" if self.app_monitor_enabled else "关闭"
            network_status = "开启" if self.network_monitor_enabled else "关闭"
            monitoring_status = "运行中" if self.monitoring else "已停止"
            
            status_text = f"状态: {monitoring_status} | 应用监控: {app_status} | 网络监控: {network_status}"
            self.status_label.config(text=status_text)
        except Exception as e:
            debug_log(f"[STATUS] 更新状态标签失败: {str(e)}")
    
    def on_app_monitor_toggle(self):
        """应用监控开关状态改变时触发"""
        self.app_monitor_enabled = self.app_monitor_var.get()
        debug_log(f"[SWITCH] 应用监控开关状态: {self.app_monitor_enabled}")
        self.safe_add_log_message(f"应用监控开关状态: {'开启' if self.app_monitor_enabled else '关闭'}")
        
        # 更新状态标签
        self.update_status_label()
    
    def on_network_monitor_toggle(self):
        """网络监控开关状态改变时触发"""
        self.network_monitor_enabled = self.network_monitor_var.get()
        debug_log(f"[SWITCH] 网络监控开关状态: {self.network_monitor_enabled}")
        self.safe_add_log_message(f"网络监控开关状态: {'开启' if self.network_monitor_enabled else '关闭'}")
        
        # 更新状态标签
        self.update_status_label()
    
    def on_contacts_saved(self):
        """联系人设置保存后的回调"""
        try:
            # 重新加载FUZZY_MATCHER以确保使用最新的联系人列表
            from main_monitor_dynamic import update_target_contacts
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            target_contacts = conf.get("chat_app", {}).get("target_contacts", [])
            
            # 更新FUZZY_MATCHER
            update_target_contacts(target_contacts)
            
            # 在日志中用逗号分隔显示联系人
            contacts_display = ", ".join(target_contacts) if target_contacts else "无"
            self.safe_add_log_message(f"✅ 联系人设置已更新，FUZZY_MATCHER已重新加载 ({len(target_contacts)} 个联系人): {contacts_display}")
        except Exception as e:
            self.safe_add_log_message(f"❌ 更新FUZZY_MATCHER失败: {str(e)}")
    
    def on_network_saved(self):
        """网络监控设置保存后的回调"""
        try:
            # 重新加载网络监控配置
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            network_conf = conf.get("network_monitor", {})
            self.safe_add_log_message(f"✅ 网络监控设置已更新 (检测间隔: {network_conf.get('check_interval', 10)}秒)")
        except Exception as e:
            self.safe_add_log_message(f"❌ 更新网络监控设置失败: {str(e)}")
    
    def on_popup_saved(self):
        """弹框监控设置保存后的回调"""
        try:
            # 重新加载弹框监控配置
            config_manager = get_config_manager()
            conf = config_manager.load_config()
            monitor_conf = conf.get("monitor", {})
            popup_conf = conf.get("popup_settings", {})
            
            check_interval = monitor_conf.get("check_interval", 1)
            reply_wait = monitor_conf.get("reply_wait", 5)
            fast_mode = popup_conf.get("fast_mode", False)
            
            if fast_mode:
                check_interval = 0.5
                reply_wait = 3
            
            self.safe_add_log_message(f"✅ 弹框监控设置已更新 (检测间隔: {check_interval}秒, 等待时间: {reply_wait}秒, 快速模式: {'开启' if fast_mode else '关闭'})")
        except Exception as e:
            self.safe_add_log_message(f"❌ 更新弹框监控设置失败: {str(e)}")
    

    
    def close_program(self):
        """关闭程序"""
        if self.monitoring:
            self.stop_monitoring()
        
        self.root.quit()
        self.root.destroy()

def main():
    """主函数"""
    # 清空调试日志
    clear_debug_log()
    
    # 立即写入启动日志
    try:
        with open("/tmp/chatmonitor_start.log", "w") as f:
            f.write("应用程序开始启动\n")
    except:
        pass
    
    try:
        debug_log("[MAIN] 应用程序启动")
        debug_log(f"[MAIN] 当前工作目录: {os.getcwd()}")
        debug_log(f"[MAIN] sys.frozen: {getattr(sys, 'frozen', False)}")
        debug_log(f"[MAIN] sys.executable: {sys.executable}")
        
        # 配置tesseract
        debug_log("[MAIN] 开始配置tesseract...")
        configure_tesseract()
        debug_log("[MAIN] tesseract配置完成")
        
        debug_log("[MAIN] 创建tkinter根窗口...")
        root = tk.Tk()
        debug_log("[MAIN] tkinter根窗口创建成功")
    except Exception as e:
        debug_log(f"[MAIN] 启动失败: {str(e)}")
        import traceback
        debug_log(f"[MAIN] 错误详情: {traceback.format_exc()}")
        raise
    
    # 设置 macOS 风格
    try:
        # 尝试设置 macOS 原生风格
        root.tk.call('tk', 'scaling', 2.0)  # 高DPI支持
    except:
        pass
    
    # 创建加载窗口
    loading = LoadingWindow(root)
    
    # 在后台线程中初始化
    def init_app():
        try:
            # 模拟初始化步骤
            loading.update_loading("正在加载配置...")
            loading.update_status("读取配置文件")
            time.sleep(0.5)
            
            loading.update_loading("正在初始化YOLO模型...")
            loading.update_status("加载深度学习模型")
            time.sleep(1.0)
            
            loading.update_loading("正在启动监控...")
            loading.update_status("初始化监控组件")
            time.sleep(0.5)
            
            # 销毁加载窗口，创建主窗口
            root.after(0, lambda: create_main_window(root))
            
        except Exception as e:
            loading.update_status(f"初始化失败: {str(e)}")
    
    # 启动初始化线程
    init_thread = threading.Thread(target=init_app, daemon=True)
    init_thread.start()
    
    # 启动主循环
    root.mainloop()

def create_main_window(root):
    """创建主窗口"""
    # 清除加载窗口
    for widget in root.winfo_children():
        widget.destroy()
    
    # 创建主应用
    app = ChatMonitorGUI(root)

if __name__ == "__main__":
    main() 