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
        
        # 发信人设置按钮
        self.contacts_button = ttk.Button(
            self.button_frame,
            text="发信人设置",
            command=self.open_contacts_settings
        )
        self.contacts_button.grid(row=0, column=2, padx=(0, 10))
        
        # 网络监控频率设置按钮
        self.network_button = ttk.Button(
            self.button_frame,
            text="网络监控频率",
            command=self.open_network_settings
        )
        self.network_button.grid(row=0, column=3, padx=(0, 10))
        
        # 关闭按钮
        self.close_button = ttk.Button(
            self.button_frame,
            text="关闭程序",
            command=self.close_program
        )
        self.close_button.grid(row=0, column=4)
        
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
        
        # 更新初始状态
        self.update_status_label()
    
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
                    # 检查是否有任何监控启用
                    if not self.app_monitor_enabled and not self.network_monitor_enabled:
                        time.sleep(check_interval)
                        continue
                    
                    # 网络监控检查（根据开关状态）
                    if self.network_monitor_enabled:
                        try:
                            from main_monitor_dynamic import check_network_with_alert
                            check_network_with_alert()
                        except Exception as e:
                            self.safe_add_log_message(f"网络监控检查失败: {str(e)}")
                    else:
                        # 网络监控关闭时，减少日志输出
                        if self.detection_count % 20 == 0:  # 每20次检测输出一次状态
                            self.safe_add_log_message("网络监控已关闭")
                    
                    # 应用监控检查（根据开关状态）
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
                        
                        # 截图
                        img = screenshot()
                        if img is None:
                            self.safe_add_log_message("截图失败")
                            time.sleep(check_interval)
                            continue
                        
                        self.detection_count += 1
                        results = []
                        
                        # YOLO检测
                        if self.yolo_manager and self.yolo_manager.initialized:
                            results = detect_and_ocr_with_yolo(img, self.yolo_manager, ocr_lang, ocr_psm)
                            if debug_verbose and results:
                                self.safe_add_log_message(f"检测到 {len(results)} 个弹窗")
                        
                        # 处理检测结果
                        for result in results:
                            text = result['text']
                            # 重新获取最新的FUZZY_MATCHER（确保获取到最新的联系人） 要不然和保存那里的作用域都不一样
                            from main_monitor_dynamic import FUZZY_MATCHER as current_fuzzy_matcher
                            if text and current_fuzzy_matcher:
                                # 添加调试信息
                                self.safe_add_log_message(f"🔍 检测到弹窗文本: {text[:100]}...")
                                
                                first_line = text.splitlines()[0] if text else ""
                                self.safe_add_log_message(f"🔍 第一行文本: '{first_line}'")
                                
                                # 检查所有行文本
                                # all_lines = text.splitlines()
                                # self.safe_add_log_message(f"🔍 所有行数: {len(all_lines)}")
                                
                                # 检查第一行
                                match_result = current_fuzzy_matcher.match_sender(first_line)
                                if match_result:
                                    contact, sender, similarity = match_result
                                    # {contact} 
                                    self.safe_add_log_message(f"✅ 第一行匹配成功: (相似度: {similarity:.2f})")
                                    now = time.time()
                                    if now - self.last_reply_time > reply_wait:
                                        self.safe_add_detection_result(
                                            app_name, 
                                            f"目标联系人: {contact}（识别为: {sender}, 相似度: {similarity:.2f}）",
                                            result.get('confidence'),
                                            "YOLO+OCR"
                                        )
                                        play_sound("contact")
                                        self.last_reply_time = now
                                        break
                    else:
                        # 应用监控关闭时，跳过截图和检测
                        time.sleep(check_interval)
                        continue
                    
                    time.sleep(check_interval)
                    
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
    
    def open_contacts_settings(self):
        """打开发信人设置窗口"""
        try:
            # 创建设置窗口
            settings_window = tk.Toplevel(self.root)
            settings_window.title("发信人设置")
            # 不设置固定大小，让窗口自适应内容
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
            self.safe_add_log_message(f"❌ 打开发信人设置失败: {str(e)}")
            debug_log(f"[CONTACTS] 打开设置窗口失败: {str(e)}")
    
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
        """加载发信人到文本框"""
        try:
            conf = get_config()
            default_contacts = conf.get("chat_app", {}).get("target_contacts", [])
            
            if default_contacts:
                contacts_str = ", ".join(default_contacts)
                text_widget.delete(1.0, tk.END)
                text_widget.insert(1.0, contacts_str)
                self.update_settings_status_label(status_label, f"已加载 {len(default_contacts)} 个默认发信人")
            else:
                self.update_settings_status_label(status_label, "未找到默认发信人配置")
                
        except Exception as e:
            self.update_settings_status_label(status_label, f"加载配置文件失败: {str(e)}")
    
    def parse_contacts(self, text):
        """解析发信人文本，支持中英文逗号"""
        import re
        
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
        
        return cleaned_contacts
    
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
            
            # 保存配置文件 - 使用与读取相同的路径
            from main_monitor_dynamic import get_config_path
            config_path = get_config_path()
            import yaml
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(conf, f, default_flow_style=False, allow_unicode=True)
            
            # 立即更新内存中的目标联系人（这会同时更新TARGET_CONTACTS和FUZZY_MATCHER）
            from main_monitor_dynamic import update_target_contacts
            update_target_contacts(contacts)
            
            # 验证更新是否成功
            from main_monitor_dynamic import TARGET_CONTACTS, FUZZY_MATCHER
            debug_log(f"[CONTACTS] TARGET_CONTACTS已更新: {TARGET_CONTACTS}")
            if FUZZY_MATCHER and hasattr(FUZZY_MATCHER, 'target_contacts'):
                debug_log(f"[CONTACTS] FUZZY_MATCHER已更新: {FUZZY_MATCHER.target_contacts}")
            
            self.update_settings_status_label(status_label, f"已保存 {len(contacts)} 个发信人: {', '.join(contacts)}")
            self.safe_add_log_message(f"✅ 发信人设置已更新: {', '.join(contacts)}")
            
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
            # 不设置固定大小，让窗口自适应内容
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
            self.safe_add_log_message(f"❌ 打开网络监控设置失败: {str(e)}")
    
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
            from config_manager import get_config_manager
            config_manager = get_config_manager()
            network_config = config_manager.get_network_config()
            
            # 设置当前值
            self.check_interval_var.set(str(network_config.get("check_interval", 10)))
            self.timeout_var.set(str(network_config.get("timeout", 5)))
            self.consecutive_failures_var.set(str(network_config.get("consecutive_failures", 3)))
            self.tolerance_minutes_var.set(str(network_config.get("tolerance_minutes", 0.1)))
            
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
            tolerance_minutes = float(self.tolerance_minutes_var.get())
            
            # 验证输入
            if check_interval < 1 or timeout < 1 or consecutive_failures < 1 or tolerance_minutes < 0.01:
                self.update_network_status_label("❌ 参数值无效，请检查输入")
                return
            
            # 保存到配置文件
            from config_manager import get_config_manager
            config_manager = get_config_manager()
            
            # 更新网络监控配置
            config_manager.update_network_config({
                "check_interval": check_interval,
                "timeout": timeout,
                "consecutive_failures": consecutive_failures,
                "tolerance_minutes": tolerance_minutes
            })
            
            self.update_network_status_label("✅ 设置已保存，监控将立即生效")
            
            # 显示成功消息
            messagebox.showinfo("成功", "网络监控频率设置已保存，监控将立即生效")
            
            # 关闭窗口
            window.destroy()
            
        except ValueError:
            self.update_network_status_label("❌ 输入格式错误，请检查数值")
        except Exception as e:
            self.update_network_status_label(f"❌ 保存设置失败: {str(e)}")
    
    def restore_network_defaults(self):
        """恢复网络监控默认设置"""
        try:
            # 程序安装时的默认值
            default_values = {
                "check_interval": 60,      # 60秒
                "timeout": 10,             # 10秒
                "consecutive_failures": 6, # 6次
                "tolerance_minutes": 0.5   # 0.5分钟
            }
            
            # 设置默认值
            self.check_interval_var.set(str(default_values["check_interval"]))
            self.timeout_var.set(str(default_values["timeout"]))
            self.consecutive_failures_var.set(str(default_values["consecutive_failures"]))
            self.tolerance_minutes_var.set(str(default_values["tolerance_minutes"]))
            
            self.update_network_status_label("✅ 已恢复默认设置")
            
        except Exception as e:
            self.update_network_status_label(f"❌ 恢复默认设置失败: {str(e)}")
    
    def update_network_status_label(self, message):
        """更新网络设置状态标签"""
        self.network_status_label.config(text=message)
    
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