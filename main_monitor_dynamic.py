#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态配置聊天监控主控脚本
- 支持 config_with_yolo.yaml 热更新
- 支持联系人和模糊匹配参数动态调整
- 集成 YOLO 检测、Tesseract OCR、FuzzyMatcher
"""
import time
import os
import psutil
import pyautogui
import cv2
import numpy as np
import pytesseract

# 配置tesseract路径，支持打包后的应用程序
def configure_tesseract():
    """配置tesseract路径"""
    import sys
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
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        except Exception as e:
            debug_log(f"[TESSERACT] 测试路径失败 {path}: {str(e)}")
            continue
    
    debug_log("[TESSERACT] ❌ 未找到可用的tesseract")
    return False

# 初始化时配置tesseract（移到函数定义之后）
import requests  # 添加requests导入
from typing import List, Dict
from datetime import datetime
from fuzzy_matcher import FuzzyMatcher
from config_manager import init_config_manager
# 网络监控已简化为函数，不再需要NetworkMonitor类

# 网络监控全局变量
last_network_check_time = time.time()
network_failure_count = 0
network_alert_sent = False

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  ultralytics未安装，无法使用YOLO模型")

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
            f.write(f"[{timestamp}] === 程序启动，日志已清空 ===\n")
        print("✅ 调试日志已清空")
    except Exception as e:
        print(f"清空调试日志失败: {e}")

def get_config_path():
    """获取配置文件路径，支持 .app 包和开发环境"""
    import os
    import sys
    
    # 可能的配置文件路径
    possible_paths = [
        "config_with_yolo.yaml",  # 当前目录
        os.path.join(os.path.dirname(__file__), "config_with_yolo.yaml"),  # 脚本目录
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_with_yolo.yaml"),  # 绝对路径
    ]
    
    # 如果是 .app 包，尝试从 Resources 目录加载
    if getattr(sys, 'frozen', False):
        # 打包后的应用
        app_dir = os.path.dirname(sys.executable)
        resources_dir = os.path.join(app_dir, "..", "Resources")
        possible_paths.insert(0, os.path.join(resources_dir, "config_with_yolo.yaml"))
        # 也尝试从用户目录加载
        user_config = os.path.expanduser("~/ChatMonitor/config_with_yolo.yaml")
        possible_paths.insert(0, user_config)
    
    # 查找存在的配置文件
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到配置文件: {path}")
            return path
    
    # 如果都找不到，返回默认路径
    default_path = "config_with_yolo.yaml"
    print(f"⚠️  未找到配置文件，使用默认路径: {default_path}")
    return default_path

# 初始化配置管理器
config_path = get_config_path()
config_manager = init_config_manager(config_path)

# 全局变量
TARGET_CONTACTS = []
FUZZY_MATCHER = None

def update_target_contacts(new_contacts, old_contacts=None):
    global TARGET_CONTACTS, FUZZY_MATCHER
    TARGET_CONTACTS = new_contacts
    fuzzy_conf = config_manager.get_config().get("chat_app", {}).get("fuzzy_match", {})
    FUZZY_MATCHER = FuzzyMatcher(
        TARGET_CONTACTS,
        similarity_threshold=fuzzy_conf.get("similarity_threshold", 0.5),
        min_length=fuzzy_conf.get("min_length", 2)
    )
    print(f"🔄 目标联系人/模糊参数已更新: {TARGET_CONTACTS}, 阈值={fuzzy_conf.get('similarity_threshold', 0.5)}")

def update_fuzzy_config(new_config, old_config=None):
    global FUZZY_MATCHER
    fuzzy_conf = new_config or {}
    FUZZY_MATCHER = FuzzyMatcher(
        TARGET_CONTACTS,
        similarity_threshold=fuzzy_conf.get("similarity_threshold", 0.5),
        min_length=fuzzy_conf.get("min_length", 2)
    )
    print(f"🔄 模糊匹配参数已更新: 阈值={fuzzy_conf.get('similarity_threshold', 0.5)}")

# 注册回调
config_manager.register_callback("chat_app.target_contacts", update_target_contacts)
config_manager.register_callback("chat_app.fuzzy_match", update_fuzzy_config)

# 初始加载
init_conf = config_manager.get_config()
update_target_contacts(init_conf.get("chat_app", {}).get("target_contacts", []))

# 工具函数
def get_config():
    return config_manager.get_config()

def play_sound(sound_type="default"):
    """
    跨平台音频播放，支持真实录音和TTS语音
    sound_type: "default", "contact", "error", "warning"
    """
    import platform
    import subprocess
    import os
    
    system = platform.system()
    
    # 获取资源文件路径
    def get_resource_path(filename):
        """获取资源文件路径，支持打包后的路径"""
        import sys
        
        # 尝试多种可能的路径
        possible_paths = [
            filename,  # 当前目录
            os.path.join("sounds", filename),  # sounds子目录
            os.path.join(os.path.dirname(__file__), "sounds", filename),  # 脚本目录下的sounds
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", filename),  # 绝对路径
        ]
        
        # 如果是打包后的应用，尝试从 Resources 目录加载
        if getattr(sys, 'frozen', False):
            # PyInstaller 临时目录
            if hasattr(sys, '_MEIPASS'):
                meipass_sounds = os.path.join(sys._MEIPASS, "sounds", filename)
                possible_paths.insert(0, meipass_sounds)
                debug_log(f"[SOUND] 尝试_MEIPASS路径: {meipass_sounds}")
            
            # macOS .app Resources 目录
            app_dir = os.path.dirname(sys.executable)
            resources_sounds = os.path.join(app_dir, "..", "Resources", "sounds", filename)
            possible_paths.insert(0, resources_sounds)
            debug_log(f"[SOUND] 尝试Resources路径: {resources_sounds}")
        
        for path in possible_paths:
            exists = os.path.exists(path)
            debug_log(f"[SOUND] 检查音频文件: {path} - {'存在' if exists else '不存在'}")
            if exists:
                debug_log(f"[SOUND] ✅ 找到音频文件: {path}")
                return path
        
        debug_log(f"[SOUND] ❌ 未找到音频文件: {filename}")
        return None
    
    # 根据提示音类型选择音频文件 - 优先使用真实录音
    sound_files = {
        "default": {
            "windows": "sounds/default.wav",
            "darwin": "sounds/default.wav",
            "linux": "sounds/default.wav"
        },
        "contact": {
            "windows": "sounds/contact_alert_pitch_speed_volume.wav",
            "darwin": "sounds/contact_alert_pitch_speed_volume.wav",
            "linux": "sounds/contact_alert_pitch_speed_volume.wav"
        },
        "error": {
            "windows": "sounds/normal_tip_pitch_speed_volume.wav",
            "darwin": "sounds/normal_tip_pitch_speed_volume.wav", 
            "linux": "sounds/normal_tip_pitch_speed_volume.wav"
        },
        "warning": {
            "windows": "sounds/error_alert_pitch_speed_volume.wav", 
            "darwin": "sounds/error_alert_pitch_speed_volume.wav",
            "linux": "sounds/error_alert_pitch_speed_volume.wav"
        }
    }
    
    try:
        # 尝试播放真实录音文件
        sound_file_name = sound_files[sound_type][system.lower()]
        if sound_file_name:
            # 使用改进的路径解析
            sound_file = get_resource_path(os.path.basename(sound_file_name))
            if sound_file:
                if system == "Windows":
                    # Windows - 使用playsound库
                    try:
                        from playsound import playsound
                        playsound(sound_file, block=False)
                        debug_log(f"[SOUND] ✅ Windows playsound播放成功: {sound_file}")
                        return
                    except ImportError:
                        # 备用方案：PowerShell
                        subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{sound_file}").PlaySync()'], 
                                     capture_output=True, check=True)
                        debug_log(f"[SOUND] ✅ Windows PowerShell播放成功: {sound_file}")
                        return
                elif system == "Darwin":  # macOS
                    # 只使用 afplay 播放指定音频文件
                    try:
                        debug_log(f"[SOUND] 尝试afplay播放: {sound_file}")
                        result = subprocess.run(['afplay', sound_file], capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            debug_log(f"[SOUND] ✅ afplay播放成功: {sound_file}")
                            return
                        else:
                            debug_log(f"[SOUND] ❌ afplay播放失败: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        debug_log(f"[SOUND] ⚠️ afplay播放超时: {sound_file}")
                    except Exception as e:
                        debug_log(f"[SOUND] ❌ afplay播放异常: {str(e)}")
                    
                    # 如果 afplay 失败，记录错误但不使用系统提示音
                    debug_log(f"[SOUND] ❌ 无法播放指定音频文件: {sound_file}")
                    return
                    
                elif system == "Linux":
                    try:
                        subprocess.run(['paplay', sound_file], capture_output=True, check=True)
                        debug_log(f"[SOUND] ✅ Linux paplay播放成功: {sound_file}")
                        return
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        subprocess.run(['aplay', sound_file], capture_output=True, check=True)
                        debug_log(f"[SOUND] ✅ Linux aplay播放成功: {sound_file}")
                        return
            else:
                debug_log(f"[SOUND] ❌ 未找到音频文件: {sound_file_name}")
                return
        
        # 如果没有找到音频文件，记录错误但不播放系统提示音
        debug_log(f"[SOUND] ❌ 未找到音频文件配置: {sound_type}")
                
    except Exception as e:
        # 所有方法都失败时，记录错误但不播放系统提示音
        debug_log(f"[SOUND] ❌ 音频播放失败: {e}")
        return

def check_process(app_name):
    for proc in psutil.process_iter(['name']):
        try:
            if app_name.lower() in proc.info['name'].lower():
                return True
        except Exception:
            pass
    return False

def check_network():
    """简单网络检测"""
    try:
        response = requests.head("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_network_with_alert():
    """网络检测带警报功能"""
    global last_network_check_time, network_failure_count, network_alert_sent
    
    current_time = time.time()
    
    # 从配置中获取参数
    conf = get_config()
    network_conf = conf.get("network_monitor", {})
    check_interval = network_conf.get("check_interval", 60)  # 默认60秒
    consecutive_failures = network_conf.get("consecutive_failures", 3)  # 默认3次
    tolerance_minutes = network_conf.get("tolerance_minutes", 1)  # 默认1分钟
    
    # 检查网络
    network_ok = check_network()
    
    if network_ok:
        # 网络正常，重置计数器
        if network_failure_count > 0:
            print(f"✅ 网络恢复正常 - {datetime.now().strftime('%H:%M:%S')}")
        network_failure_count = 0
        network_alert_sent = False
        last_network_check_time = current_time
        return True
    else:
        # 网络异常
        network_failure_count += 1
        print(f"❌ 网络检测失败 ({network_failure_count}/{consecutive_failures}) - {datetime.now().strftime('%H:%M:%S')}")
        
        # 检查是否达到连续失败阈值和时间阈值
        time_since_last_check = current_time - last_network_check_time
        if (network_failure_count >= consecutive_failures and 
            time_since_last_check >= tolerance_minutes * 60):
            
            print(f"🚨 网络异常警报 - 连续失败{network_failure_count}次，超过{tolerance_minutes}分钟")
            play_sound("warning")
            return True  # 继续运行，不中断程序
        
        return True  # 继续运行，不中断程序

def screenshot():
    try:
        img = pyautogui.screenshot()
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"截图失败: {e}")
        return None

def detect_and_ocr_with_yolo(image, yolo_manager, ocr_lang, ocr_psm):
    results = []
    detections = yolo_manager.detect_popups(image)
    for i, det in enumerate(detections):
        x1, y1, x2, y2 = det['bbox']
        popup_img = image[y1:y2, x1:x2]
        text = pytesseract.image_to_string(popup_img, lang=ocr_lang, config=f"--psm {ocr_psm}")
        results.append({'text': text, 'bbox': det['bbox'], 'confidence': det['confidence']})
    return results

class YOLOModelManager:
    def __init__(self, model_path, confidence=0.35):
        # 处理模型路径，支持 .app 包和开发环境
        resolved_model_path = self._resolve_model_path(model_path)
        self.model = YOLO(resolved_model_path) if YOLO_AVAILABLE and os.path.exists(resolved_model_path) else None
        self.confidence = confidence
        self.initialized = self.model is not None
        
    def _resolve_model_path(self, model_path):
        """解析模型路径，支持 .app 包和开发环境"""
        import sys
        
        debug_log(f"[YOLOModelManager._resolve_model_path] 启动, model_path={model_path}")
        print(f"🔍 当前工作目录: {os.getcwd()}")
        print(f"🔍 sys.frozen: {getattr(sys, 'frozen', False)}")
        if getattr(sys, 'frozen', False):
            print(f"🔍 sys.executable: {sys.executable}")
            print(f"🔍 可执行文件目录: {os.path.dirname(sys.executable)}")
        
        # 调试断点 - 可以通过环境变量启用
        if os.environ.get('CHATMONITOR_DEBUG') == '1':
            import pdb; pdb.set_trace()
        
        # 远程调试支持
        if os.environ.get('CHATMONITOR_REMOTE_DEBUG') == '1':
            try:
                import debugpy
                debugpy.listen(("0.0.0.0", 5678))
                print("🔗 远程调试器已启动，等待连接...")
                debugpy.wait_for_client()
                print("🔗 远程调试器已连接")
            except ImportError:
                print("⚠️  debugpy未安装，跳过远程调试")
            except Exception as e:
                print(f"⚠️  远程调试启动失败: {e}")
        
        # 如果路径已经是绝对路径且存在，直接返回
        if os.path.isabs(model_path) and os.path.exists(model_path):
            print(f"✅ 绝对路径存在: {model_path}")
            debug_log(f"[YOLOModelManager._resolve_model_path] ✅ 绝对路径存在: {model_path}")
            return model_path
            
        # 可能的模型路径
        possible_paths = []
        debug_log(f"[YOLOModelManager._resolve_model_path] 尝试路径列表:")
        # 1. PyInstaller专用临时目录
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            meipass_path = os.path.join(sys._MEIPASS, model_path)
            possible_paths.append(meipass_path)
            debug_log(f"[YOLOModelManager._resolve_model_path] 尝试_MEIPASS路径: {meipass_path}")
        # 2. macOS .app Resources
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
            resources_path = os.path.join(app_dir, "..", "Resources", model_path)
            possible_paths.append(resources_path)
            debug_log(f"[YOLOModelManager._resolve_model_path] 尝试Resources路径: {resources_path}")
        # 3. 用户目录
        user_home = os.path.expanduser("~")
        user_models_path = os.path.join(user_home, "ChatMonitor", "models", os.path.basename(model_path))
        possible_paths.append(user_models_path)
        debug_log(f"[YOLOModelManager._resolve_model_path] 尝试用户目录: {user_models_path}")
        # 4. 当前工作目录
        cwd_path = os.path.join(os.getcwd(), model_path)
        possible_paths.append(cwd_path)
        debug_log(f"[YOLOModelManager._resolve_model_path] 尝试当前工作目录: {cwd_path}")
        # 5. 脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_models_path = os.path.join(script_dir, model_path)
        possible_paths.append(script_models_path)
        debug_log(f"[YOLOModelManager._resolve_model_path] 尝试脚本目录: {script_models_path}")
        # 6. 绝对路径
        abs_path = os.path.abspath(model_path)
        possible_paths.append(abs_path)
        debug_log(f"[YOLOModelManager._resolve_model_path] 尝试绝对路径: {abs_path}")
        
        # 检查所有路径
        for i, path in enumerate(possible_paths):
            exists = os.path.exists(path)
            debug_log(f"[YOLOModelManager._resolve_model_path] 检查: {path} - {'存在' if exists else '不存在'}")
            if exists:
                debug_log(f"[YOLOModelManager._resolve_model_path] ✅ 找到模型文件: {path}")
                return path
        
        debug_log(f"[YOLOModelManager._resolve_model_path] ❌ 未找到模型文件: {model_path}")
        return model_path
    def detect_popups(self, image):
        if not self.initialized:
            return []
        results = self.model(image, conf=self.confidence)
        detections = []
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                for box, conf in zip(boxes, confs):
                    x1, y1, x2, y2 = map(int, box[:4])
                    detections.append({'bbox': (x1, y1, x2, y2), 'confidence': float(conf)})
        return detections

def main():
    # 清空调试日志
    clear_debug_log()
    
    print("✅ 动态配置监控已启动，修改 config_with_yolo.yaml 可实时生效")
    print(f"🕐 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 使用统一的配置管理
    from config_manager import get_config_manager
    config_manager = get_config_manager()
    
    yolo_config = config_manager.get_yolo_config()
    ocr_config = config_manager.get_ocr_config()
    monitor_config = config_manager.get_monitor_config()
    debug_config = config_manager.get_debug_config()
    chat_config = config_manager.get_chat_app_config()
    network_config = config_manager.get_network_config()
    
    app_name = chat_config["name"]
    yolo_enabled = yolo_config["enabled"] and YOLO_AVAILABLE
    yolo_model_path = yolo_config["model_path"]
    yolo_confidence = yolo_config["confidence"]
    ocr_lang = ocr_config["lang"]
    ocr_psm = ocr_config["psm"]
    check_interval = monitor_config["check_interval"]
    reply_wait = monitor_config["reply_wait"]
    debug_verbose = debug_config["verbose"]
    
    yolo_manager = YOLOModelManager(yolo_model_path, yolo_confidence) if yolo_enabled else None
    last_reply_time = 0
    
    # 打印初始配置
    print(f"🎯 目标应用: {app_name}")
    print(f"🤖 YOLO检测: {'启用' if yolo_enabled else '禁用'}")
    if yolo_enabled:
        print(f"📁 YOLO模型: {yolo_model_path}")
        print(f"🎯 置信度阈值: {yolo_confidence}")
    print(f"📝 OCR语言: {ocr_lang}")
    print(f"⏱️  检测间隔: {check_interval} 秒")
    print(f"🎯 目标联系人: {TARGET_CONTACTS}")
    print(f"🔍 调试模式: {'开启' if debug_verbose else '关闭'}")
    print("-" * 50)

    # 初始化网络监控
    network_enabled = network_config["enabled"]
    if network_enabled:
        consecutive_failures = network_config["consecutive_failures"]
        tolerance_minutes = network_config["tolerance_minutes"]
        print(f"🌐 网络监控已启用 - 连续失败阈值: {consecutive_failures}, 容错时间: {tolerance_minutes}分钟")

    detection_count = 0
    last_status_time = time.time()
    
    while True:
        try:
            current_time = time.time()
            # 在循环中重新获取配置（支持热更新）
            yolo_config = get_yolo_config()
            monitor_config = get_monitor_config()
            chat_config = get_chat_app_config()
            
            app_name = chat_config["name"]
            check_interval = monitor_config["check_interval"]
            reply_wait = monitor_config["reply_wait"]

            # 检查进程
            if not check_process(app_name):
                print(f"❌ 未找到 {app_name} 进程 - {datetime.now().strftime('%H:%M:%S')}")
                play_sound("error")
                time.sleep(check_interval)
                continue

            # 检查网络（简单函数判断）
            if network_enabled:
                check_network_with_alert()  # 每次检测都调用，不暂停程序
                        
            # 定期输出状态信息
            if current_time - last_status_time > 60:  # 每分钟输出一次状态
                print(f"📊 状态更新 - {datetime.now().strftime('%H:%M:%S')} - 检测次数: {detection_count}")
                last_status_time = current_time
            
            img = screenshot()
            if img is None:
                print(f"❌ 截图失败 - {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(check_interval)
                continue
            
            detection_count += 1
            results = []
            if yolo_manager and yolo_manager.initialized:
                results = detect_and_ocr_with_yolo(img, yolo_manager, ocr_lang, ocr_psm)
                if debug_verbose and results:
                    print(f"🔍 检测到 {len(results)} 个弹窗 - {datetime.now().strftime('%H:%M:%S')}")
            else:
                if debug_verbose:
                    print(f"⚠️  YOLO检测未启用或初始化失败 - {datetime.now().strftime('%H:%M:%S')}")
            for result in results:
                text = result['text']
                if debug_verbose:
                    # 添加详细的调试信息
                    print(f"🔍 调试信息:")
                    print(f"  text类型: {type(text)}")
                    print(f"  text内容: '{text}'")
                    print(f"  text长度: {len(text) if text else 0}")
                    print(f"  text布尔值: {bool(text)}")
                    print(f"  FUZZY_MATCHER: {FUZZY_MATCHER}")
                    print(f"  FUZZY_MATCHER布尔值: {bool(FUZZY_MATCHER)}")
                    print(f"  条件判断结果: {bool(text and FUZZY_MATCHER)}")
                
                if text and FUZZY_MATCHER:
                    # print(f"✅ 进入条件分支")
                    first_line = text.splitlines()[0] if text else ""
                    # print(f"  第一行内容: '{first_line}'")
                    match_result = FUZZY_MATCHER.match_sender(first_line)
                    if match_result:
                        contact, sender, similarity = match_result
                        now = time.time()
                        if now - last_reply_time > reply_wait:
                            print(f"检测到目标联系人: {contact}（识别为: {sender}, 相似度: {similarity:.2f}）")
                            play_sound("contact")
                            last_reply_time = now
                            break
                elif debug_verbose:
                    print(f"❌ 条件判断失败，跳过处理")
            time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n程序已停止")
            break
        except Exception as e:
            print(f"运行出错: {e}")
            time.sleep(check_interval)

if __name__ == "__main__":
    # 初始化时配置tesseract
    configure_tesseract()
    main() 