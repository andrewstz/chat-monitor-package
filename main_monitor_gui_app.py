#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatMonitor GUI 版本 - 用于打包成 .app
集成 tkinter 界面的聊天弹窗监控器
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
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
        
        # 设置窗口置顶
        self.root.lift()
        self.root.attributes('-topmost', True)
        
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
        self.root.geometry("500x600")
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
        
        # 开始/停止按钮
        self.start_stop_button = ttk.Button(
            self.button_frame,
            text="开始监控",
            command=self.toggle_monitoring
        )
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
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
        
        # 初始化配置
        self.init_monitoring()
        
        # 不自动启动监控，让用户手动点击开始
        # self.start_monitoring()
    
    def init_monitoring(self):
        """初始化监控配置"""
        debug_log("[INIT] 开始初始化监控配置")
        try:
            conf = get_config()
            yolo_conf = conf.get("yolo", {})
            yolo_enabled = yolo_conf.get("enabled", True)
            yolo_model_path = yolo_conf.get("model_path", "models/best.pt")
            yolo_confidence = yolo_conf.get("confidence", 0.35)
            
            debug_log(f"[INIT] YOLO配置: enabled={yolo_enabled}, model_path={yolo_model_path}, confidence={yolo_confidence}")
            
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
            
            self.status_label.config(text="状态: 监控已启动")
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
            
            # 检查目标应用进程
            if not check_process(app_name):
                self.safe_add_log_message(f"⚠️ 未找到目标应用: {app_name}")
                self.safe_add_log_message("请确保目标应用正在运行")
                return
            
            self.safe_add_log_message(f"✅ 开始监控应用: {app_name}")
            
            while self.monitoring:
                try:
                    # 检查进程
                    if not check_process(app_name):
                        self.safe_add_log_message(f"未找到 {app_name} 进程")
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
                        if text and FUZZY_MATCHER:
                            first_line = text.splitlines()[0] if text else ""
                            match_result = FUZZY_MATCHER.match_sender(first_line)
                            if match_result:
                                contact, sender, similarity = match_result
                                now = time.time()
                                if now - self.last_reply_time > reply_wait:
                                    self.safe_add_detection_result(
                                        app_name, 
                                        f"目标联系人: {contact}（识别为: {sender}, 相似度: {similarity:.2f}）",
                                        result.get('confidence'),
                                        "YOLO+OCR"
                                    )
                                    # 添加声音播放调试信息
                                    self.safe_add_log_message("🔊 播放联系提醒音...")
                                    try:
                                        play_sound("contact")
                                        self.safe_add_log_message("✅ 声音播放完成")
                                    except Exception as e:
                                        self.safe_add_log_message(f"❌ 声音播放失败: {str(e)}")
                                    self.last_reply_time = now
                                    break
                    
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