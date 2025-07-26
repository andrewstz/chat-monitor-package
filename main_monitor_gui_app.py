#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor GUI 应用程序
支持守护进程模式和普通模式
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import sys
import os
from datetime import datetime
import argparse

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入必要的模块
from gui.contacts_settings import ContactsSettingsWindow
from gui.network_settings import NetworkSettingsWindow
from gui.popup_settings import PopupSettingsWindow
from config_manager import get_config_manager
from main_monitor_dynamic import update_target_contacts

# 导入原有的监控模块
from main_monitor_dynamic import (
    get_config, play_sound, check_process, screenshot, 
    detect_and_ocr_with_yolo, YOLOModelManager, TARGET_CONTACTS, FUZZY_MATCHER,
    config_manager
)

# 导入配置管理器
# from config_manager import get_config_manager # This line is now redundant as it's imported directly

# 导入GUI设置模块
# from gui.contacts_settings import ContactsSettingsWindow # This line is now redundant as it's imported directly
# from gui.network_settings import NetworkSettingsWindow # This line is now redundant as it's imported directly
# from gui.popup_settings import PopupSettingsWindow # This line is now redundant as it's imported directly

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
    def __init__(self, daemon_mode=False, enable_daemon=True):
        self.daemon_mode = daemon_mode
        self.enable_daemon = enable_daemon
        self.root = tk.Tk()
        self.root.title("ChatMonitor 弹框监控")
        self.root.geometry("700x600")
        
        # 设置窗口图标
        try:
            if hasattr(sys, '_MEIPASS'):  # PyInstaller 打包
                icon_path = os.path.join(sys._MEIPASS, "assets", "icons", "icon.icns")
            else:
                icon_path = "assets/icons/icon.icns"
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"设置图标失败: {e}")
        
        # 初始化配置管理器
        self.config_manager = get_config_manager()
        
        # 初始化设置窗口
        self.contacts_settings = ContactsSettingsWindow(self.root, self.on_contacts_saved)
        self.network_settings = NetworkSettingsWindow(self.root, self.on_network_saved)
        self.popup_settings = PopupSettingsWindow(self.root, self.on_popup_saved)
        
        # 初始化监控状态
        self.monitoring = False
        self.monitor_thread = None
        
        # 初始化监控开关状态
        self.app_monitor_enabled = True
        self.network_monitor_enabled = True
        
        # 初始化守护进程
        self.daemon = None
        self.daemon_thread = None
        
        # 初始化YOLO管理器（后台初始化）
        self.yolo_manager = None
        self.root.after(1000, self._init_yolo_manager)  # 1秒后后台初始化
        
        # 创建 GUI
        self.create_gui()
        
        # 守护进程模式下的特殊处理
        if self.daemon_mode:
            self.setup_daemon_mode()
        
        # 如果启用守护进程，启动内部守护进程（延迟启动，避免界面卡顿）
        if self.enable_daemon and not self.daemon_mode:
            # 默认不启动内部守护进程，避免界面问题
            # self.root.after(2000, self.start_internal_daemon)  # 2秒后启动
            pass
    
    def _init_yolo_manager(self):
        """初始化YOLO管理器"""
        try:
            from main_monitor_dynamic import YOLOModelManager
            
            # 获取配置
            config = self.config_manager.load_config()
            yolo_config = config.get("yolo_model", {})
            yolo_enabled = yolo_config.get("enabled", True)
            
            if not yolo_enabled:
                self.log_message("⚠️ YOLO模型已禁用")
                return
            
            yolo_model_path = yolo_config.get("model_path", "models/best.pt")
            yolo_confidence = yolo_config.get("confidence", 0.35)
            
            # 解析模型路径
            resolved_model_path = self._resolve_model_path(yolo_model_path)
            
            if resolved_model_path:
                debug_log("[INIT] 创建YOLOModelManager实例...")
                
                # 在后台线程中初始化YOLO管理器
                def init_yolo():
                    try:
                        debug_log("[INIT] 开始加载YOLO模型...")
                        self.yolo_manager = YOLOModelManager(resolved_model_path, yolo_confidence)
                        
                        if self.yolo_manager.initialized:
                            self.log_message("✅ YOLO模型初始化成功")
                            debug_log("[INIT] YOLO模型初始化成功")
                        else:
                            self.log_message("❌ YOLO模型初始化失败")
                            debug_log("[INIT] YOLO模型初始化失败")
                    except Exception as e:
                        error_msg = f"❌ YOLO模型初始化失败: {e}"
                        self.log_message(error_msg)
                        debug_log(f"[INIT] {error_msg}")
                        import traceback
                        debug_log(f"[INIT] 错误详情: {traceback.format_exc()}")
                
                # 启动后台线程
                threading.Thread(target=init_yolo, daemon=True).start()
            else:
                self.log_message("❌ 未找到YOLO模型文件")
                
        except Exception as e:
            self.log_message(f"❌ YOLO管理器初始化失败: {e}")
    
    def _resolve_model_path(self, model_path):
        """解析模型路径"""
        import sys
        import os
        
        # 如果是绝对路径且存在，直接返回
        if os.path.isabs(model_path) and os.path.exists(model_path):
            return model_path
        
        # 可能的路径列表
        possible_paths = []
        
        # 如果是打包后的应用程序
        if getattr(sys, 'frozen', False):
            # 尝试 _MEIPASS 路径
            meipass_path = os.path.join(sys._MEIPASS, model_path)
            possible_paths.append(meipass_path)
            
            # 尝试 Resources 路径
            resources_path = os.path.join(sys._MEIPASS, "Resources", model_path)
            possible_paths.append(resources_path)
        
        # 尝试用户目录
        user_models_path = os.path.expanduser(f"~/models/{model_path}")
        possible_paths.append(user_models_path)
        
        # 尝试当前工作目录
        cwd_path = os.path.join(os.getcwd(), model_path)
        possible_paths.append(cwd_path)
        
        # 尝试脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_models_path = os.path.join(script_dir, model_path)
        possible_paths.append(script_models_path)
        
        # 尝试绝对路径
        possible_paths.append(model_path)
        
        # 检查每个路径
        for path in possible_paths:
            if os.path.exists(path):
                debug_log(f"[INIT] ✅ 找到模型文件: {path}")
                return path
        
        debug_log(f"[INIT] ❌ 未找到模型文件: {model_path}")
        return None
    
    def setup_daemon_mode(self):
        """设置守护进程模式"""
        # 隐藏主窗口，只显示系统托盘
        self.root.withdraw()
        
        # 创建系统托盘图标
        self.create_system_tray()
        
        # 自动开始监控
        self.start_monitoring()
    
    def create_system_tray(self):
        """创建系统托盘图标"""
        try:
            import pystray
            from PIL import Image
            
            # 创建托盘图标
            if hasattr(sys, '_MEIPASS'):  # PyInstaller 打包
                icon_path = os.path.join(sys._MEIPASS, "assets", "icons", "icon.png")
            else:
                icon_path = "assets/icons/icon.png"
            
            if not os.path.exists(icon_path):
                # 创建一个简单的图标
                img = Image.new('RGB', (64, 64), color='blue')
                img.save(icon_path)
            
            image = Image.open(icon_path)
            
            # 创建托盘菜单
            menu = pystray.Menu(
                pystray.MenuItem("显示主窗口", self.show_main_window),
                pystray.MenuItem("开始监控", self.start_monitoring),
                pystray.MenuItem("停止监控", self.stop_monitoring),
                pystray.MenuItem("设置", self.show_settings),
                pystray.MenuItem("退出", self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("ChatMonitor", image, "ChatMonitor", menu)
            
            # 启动托盘图标
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            
        except ImportError:
            print("警告: 缺少 pystray 模块，无法创建系统托盘")
        except Exception as e:
            print(f"创建系统托盘失败: {e}")
    
    def show_main_window(self):
        """显示主窗口"""
        self.root.deiconify()
        self.root.lift()
    
    def show_settings(self):
        """显示设置窗口"""
        # 这里可以添加一个设置选择窗口
        pass
    
    def quit_app(self):
        """退出应用"""
        self.stop_monitoring()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.root.quit()
    
    def create_gui(self):
        """创建 GUI 界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="ChatMonitor 弹框监控", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 监控状态
        self.status_var = tk.StringVar(value="⏸️ 监控已停止")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 12))
        status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # 开始/停止按钮
        self.start_stop_button = ttk.Button(button_frame, text="开始监控", command=self.toggle_monitoring)
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # 设置按钮
        settings_frame = ttk.Frame(main_frame)
        settings_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Button(settings_frame, text="发信人设置", command=self.open_contacts_settings).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(settings_frame, text="网络监控设置", command=self.open_network_settings).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(settings_frame, text="弹框监控设置", command=self.open_popup_settings).grid(row=0, column=2)
        
        # 日志显示区域
        log_frame = ttk.LabelFrame(main_frame, text="监控日志", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 监控开关框架
        switch_frame = ttk.LabelFrame(main_frame, text="监控开关", padding="5")
        switch_frame.grid(row=5, column=0, pady=(10, 0), sticky="ew")
        
        # 应用监控开关
        self.app_monitor_var = tk.BooleanVar(value=True)
        self.app_monitor_check = ttk.Checkbutton(
            switch_frame,
            text="应用监控",
            variable=self.app_monitor_var,
            command=self.on_app_monitor_toggle
        )
        self.app_monitor_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # 网络监控开关
        self.network_monitor_var = tk.BooleanVar(value=True)
        self.network_monitor_check = ttk.Checkbutton(
            switch_frame,
            text="网络监控",
            variable=self.network_monitor_var,
            command=self.on_network_monitor_toggle
        )
        self.network_monitor_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """窗口关闭事件处理"""
        if self.daemon_mode:
            # 守护进程模式下，隐藏窗口而不是关闭
            self.root.withdraw()
        else:
            # 普通模式下，停止监控并关闭
            self.stop_monitoring()
            self.root.destroy()
    
    def toggle_monitoring(self):
        """切换监控状态"""
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        """开始监控"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.start_stop_button.config(text="停止监控")
        self.status_var.set("🟢 监控运行中...")
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self.run_monitor, daemon=True)
        self.monitor_thread.start()
        
        self.log_message("✅ 监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        if not self.monitoring:
            return
        
        self.monitoring = False
        self.start_stop_button.config(text="开始监控")
        self.status_var.set("⏸️ 监控已停止")
        
        self.log_message("⏸️ 监控已停止")
    
    def on_app_monitor_toggle(self):
        """应用监控开关状态改变时触发"""
        self.app_monitor_enabled = self.app_monitor_var.get()
        self.log_message(f"应用监控开关状态: {'开启' if self.app_monitor_enabled else '关闭'}")
    
    def on_network_monitor_toggle(self):
        """网络监控开关状态改变时触发"""
        self.network_monitor_enabled = self.network_monitor_var.get()
        self.log_message(f"网络监控开关状态: {'开启' if self.network_monitor_enabled else '关闭'}")
    
    def log_message(self, message):
        """记录日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # 在 GUI 线程中更新日志
        self.root.after(0, self._update_log, log_entry)
    
    def _update_log(self, log_entry):
        """更新日志显示（线程安全）"""
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # 限制日志行数
        lines = self.log_text.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete("1.0", f"{len(lines)-50}.0")
    
    def open_contacts_settings(self):
        """打开发信人设置"""
        self.contacts_settings.open_contacts_settings()
    
    def open_network_settings(self):
        """打开网络监控设置"""
        self.network_settings.open_network_settings()
    
    def open_popup_settings(self):
        """打开弹框监控设置"""
        self.popup_settings.open_popup_settings()
    
    def on_contacts_saved(self):
        """联系人保存回调"""
        try:
            # 获取当前联系人列表
            config_manager = get_config_manager()
            config = config_manager.load_config()
            target_contacts = config.get("chat_app", {}).get("target_contacts", [])
            
            # 更新目标联系人
            update_target_contacts(target_contacts)
            
            # 记录日志（逗号分隔）
            contacts_str = ", ".join(target_contacts) if target_contacts else "无"
            self.log_message(f"✅ 联系人设置已更新: {contacts_str}")
            
        except Exception as e:
            self.log_message(f"❌ 更新联系人设置失败: {e}")
    
    def on_network_saved(self):
        """网络设置保存回调"""
        try:
            config_manager = get_config_manager()
            config = config_manager.load_config()
            network_config = config.get("network_monitor", {})
            
            check_interval = network_config.get("check_interval", 10)
            timeout = network_config.get("timeout", 5)
            consecutive_failures = network_config.get("consecutive_failures", 3)
            
            self.log_message(f"✅ 网络监控设置已更新: 检测间隔{check_interval}s, 超时{timeout}s, 连续失败阈值{consecutive_failures}次")
            
        except Exception as e:
            self.log_message(f"❌ 更新网络监控设置失败: {e}")
    
    def on_popup_saved(self):
        """弹框设置保存回调"""
        try:
            config_manager = get_config_manager()
            config = config_manager.load_config()
            popup_config = config.get("popup_monitor", {})
            
            check_interval = popup_config.get("check_interval", 1)
            reply_wait = popup_config.get("reply_wait", 5)
            fast_mode = popup_config.get("fast_mode", False)
            
            mode_str = "快速模式" if fast_mode else "普通模式"
            self.log_message(f"✅ 弹框监控设置已更新: {mode_str}, 检测间隔{check_interval}s, 等待时间{reply_wait}s")
            
        except Exception as e:
            self.log_message(f"❌ 更新弹框监控设置失败: {e}")
    
    def run_monitor(self):
        """监控主循环"""
        # 导入监控模块
        from main_monitor_dynamic import (
            get_config, check_network_with_alert, 
            check_process, screenshot, 
            detect_and_ocr_with_yolo, FUZZY_MATCHER, play_sound
        )
        
        # 初始化时间变量
        last_network_check_time = 0
        last_popup_check_time = 0
        
        self.log_message("🚀 监控线程已启动")
        
        while self.monitoring:
            try:
                current_time = time.time()
                config = get_config()
                
                # 网络监控
                network_config = config.get("network_monitor", {})
                network_enabled = network_config.get("enabled", True)
                network_check_interval = network_config.get("check_interval", 10)
                
                if network_enabled and (current_time - last_network_check_time) >= network_check_interval:
                    check_network_with_alert()
                    last_network_check_time = current_time
                
                # 弹框监控（始终启用）
                popup_config = config.get("popup_monitor", {})
                check_interval = popup_config.get("check_interval", 1)
                
                if (current_time - last_popup_check_time) >= check_interval:
                    # 截图
                    img = screenshot()
                    if img is not None:
                        # YOLO 检测弹框
                        if hasattr(self, 'yolo_manager') and self.yolo_manager and self.yolo_manager.initialized:
                            results = detect_and_ocr_with_yolo(img, self.yolo_manager, "chi_sim+eng", "6")
                            
                            if results:
                                for result in results:
                                    text = result.get('text', '')
                                    if text:
                                        # 模糊匹配
                                        if FUZZY_MATCHER:
                                            match_result = FUZZY_MATCHER.match_sender(text)
                                            if match_result:
                                                contact, sender, similarity = match_result
                                                self.log_message(f"🎯 检测到弹框: {text[:50]}... -> 匹配: {contact} (相似度: {similarity:.2f})")
                                                play_sound("contact")
                                            else:
                                                self.log_message(f"📝 检测到弹框但无匹配: {text[:50]}...")
                                        else:
                                            self.log_message(f"📝 检测到弹框: {text[:50]}...")
                    
                    last_popup_check_time = current_time
                
                # 短暂休眠
                time.sleep(0.5)
                
            except Exception as e:
                self.log_message(f"❌ 监控过程中发生错误: {e}")
                time.sleep(5)
    
    def start_internal_daemon(self):
        """启动内部守护进程"""
        try:
            # 检查是否已经启动
            if hasattr(self, 'daemon') and self.daemon:
                return
            
            from daemon_monitor import ChatMonitorDaemon
            
            self.daemon = ChatMonitorDaemon()
            self.daemon_thread = threading.Thread(target=self._run_daemon, daemon=True)
            self.daemon_thread.start()
            
            self.log_message("🛡️ 内部守护进程已启动")
        except Exception as e:
            self.log_message(f"❌ 启动内部守护进程失败: {e}")
    
    def _run_daemon(self):
        """运行守护进程"""
        try:
            self.daemon.start()
            while self.daemon.running:
                time.sleep(1)
        except Exception as e:
            self.log_message(f"❌ 守护进程运行失败: {e}")
    
    def stop_internal_daemon(self):
        """停止内部守护进程"""
        if self.daemon:
            try:
                self.daemon.stop()
                self.log_message("🛡️ 内部守护进程已停止")
            except Exception as e:
                self.log_message(f"❌ 停止内部守护进程失败: {e}")
    
    def run(self):
        """运行 GUI 应用"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"GUI 运行失败: {e}")
        finally:
            # 确保停止内部守护进程
            if self.enable_daemon:
                self.stop_internal_daemon()

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="ChatMonitor 弹框监控程序")
    parser.add_argument("--daemon", action="store_true", help="以守护进程模式运行")
    parser.add_argument("--daemon-monitor", action="store_true", help="启动守护进程监控器")
    parser.add_argument("--no-daemon", action="store_true", help="禁用守护进程功能")
    
    args = parser.parse_args()
    
    if args.daemon_monitor:
        # 启动守护进程监控器
        from daemon_monitor import ChatMonitorDaemon
        
        print("🚀 启动 ChatMonitor 守护进程监控器...")
        daemon = ChatMonitorDaemon()
        
        try:
            daemon.start()
            while daemon.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 收到中断信号")
        finally:
            daemon.stop()
    else:
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
            debug_log("[MAIN] tkinter根窗口创建成功")
        except Exception as e:
            debug_log(f"[MAIN] 启动失败: {str(e)}")
            import traceback
            debug_log(f"[MAIN] 错误详情: {traceback.format_exc()}")
            raise
        
        # 启动 GUI 应用
        app = ChatMonitorGUI(daemon_mode=args.daemon, enable_daemon=not args.no_daemon)
        app.run()

def create_main_window(root):
    """创建主窗口"""
    # 清除加载窗口
    for widget in root.winfo_children():
        widget.destroy()
    
    # 创建主应用
    app = ChatMonitorGUI(daemon_mode=False) # This line is now handled by main()

if __name__ == "__main__":
    main() 