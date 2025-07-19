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
import requests  # 添加requests导入
from typing import List, Dict
from datetime import datetime
from fuzzy_matcher import FuzzyMatcher
from config_manager import init_config_manager
from network_monitor import NetworkMonitor

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  ultralytics未安装，无法使用YOLO模型")

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
        # 尝试多种可能的路径
        possible_paths = [
            filename,  # 当前目录
            os.path.join("sounds", filename),  # sounds子目录
            os.path.join(os.path.dirname(__file__), "sounds", filename),  # 脚本目录下的sounds
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", filename),  # 绝对路径
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
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
        # 首先尝试播放真实录音文件
        sound_file = sound_files[sound_type][system.lower()]
        if sound_file and os.path.exists(sound_file):
            if system == "Windows":
                # Windows - 使用playsound库
                try:
                    from playsound import playsound
                    playsound(sound_file, block=False)
                    return
                except ImportError:
                    # 备用方案：PowerShell
                    subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{sound_file}").PlaySync()'], 
                                 capture_output=True, check=True)
                    return
            elif system == "Darwin":  # macOS
                subprocess.run(['afplay', sound_file], capture_output=True, check=True)
                return
            elif system == "Linux":
                try:
                    subprocess.run(['paplay', sound_file], capture_output=True, check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    subprocess.run(['aplay', sound_file], capture_output=True, check=True)
                return
        
        # 如果真实录音文件不存在，使用系统默认提示音
        if system == "Windows":
            # Windows系统蜂鸣器
            import winsound
            if sound_type == "contact":
                winsound.Beep(800, 300)  # 较低频率，较短时间
            elif sound_type == "error":
                winsound.Beep(400, 500)  # 更低频率，较长时间
            elif sound_type == "warning":
                winsound.Beep(600, 400)  # 中等频率
            else:
                winsound.Beep(1000, 500)  # 默认
                
        elif system == "Darwin":  # macOS
            # 使用终端铃声，不同次数区分类型
            if sound_type == "contact":
                print("\a\a")  # 两声
            elif sound_type == "error":
                print("\a\a\a")  # 三声
            elif sound_type == "warning":
                print("\a\a\a\a")  # 四声
            else:
                print("\a")  # 一声
                
        elif system == "Linux":
            # 使用终端铃声
            if sound_type == "contact":
                print("\a\a")
            elif sound_type == "error":
                print("\a\a\a")
            elif sound_type == "warning":
                print("\a\a\a\a")
            else:
                print("\a")
        else:
            # 其他系统使用终端铃声
            if sound_type == "contact":
                print("\a\a")
            elif sound_type == "error":
                print("\a\a\a")
            elif sound_type == "warning":
                print("\a\a\a\a")
            else:
                print("\a")
                
    except Exception as e:
        # 所有方法都失败时，使用终端铃声作为后备方案
        print(f"音频播放失败: {e}")
        if sound_type == "contact":
            print("\a\a")
        elif sound_type == "error":
            print("\a\a\a")
        elif sound_type == "warning":
            print("\a\a\a\a")
        else:
            print("\a")

def check_process(app_name):
    for proc in psutil.process_iter(['name']):
        try:
            if app_name.lower() in proc.info['name'].lower():
                return True
        except Exception:
            pass
    return False

def check_network():
    """简单ping一下，判断网络。ping -c 1发送 1 个 ICMP 测试包； 2>&1把标准错误输出（错误信息）也重定向到标准输出（即也丢弃到 /dev/null）。 
    脚本里用来“静默”检测网络是否可达，通常后面会用 $? 判断命令是否成功（0=通，非0=不通）；
    os.system 返回的是命令的“退出码”（exit code），而不是输出内容，在 Linux/Unix/Mac 下，0 表示命令执行成功，非0表示失败。 """
    try:
        response = requests.head("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

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
        self.model = YOLO(model_path) if YOLO_AVAILABLE and os.path.exists(model_path) else None
        self.confidence = confidence
        self.initialized = self.model is not None
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
    print("✅ 动态配置监控已启动，修改 config_with_yolo.yaml 可实时生效")
    print(f"🕐 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    conf = get_config()
    app_name = conf.get("chat_app", {}).get("name", "WeChat")
    yolo_conf = conf.get("yolo", {})
    ocr_conf = conf.get("ocr", {}).get("tesseract", {})
    yolo_enabled = yolo_conf.get("enabled", True) and YOLO_AVAILABLE
    yolo_model_path = yolo_conf.get("model_path", "runs/detect/train/weights/best.pt")
    yolo_confidence = yolo_conf.get("confidence", 0.35)
    ocr_lang = ocr_conf.get("lang", "chi_sim+eng")
    ocr_psm = ocr_conf.get("config", "--psm 6").split()[-1]
    check_interval = conf.get("monitor", {}).get("check_interval", 3)
    reply_wait = conf.get("monitor", {}).get("reply_wait", 60)
    yolo_manager = YOLOModelManager(yolo_model_path, yolo_confidence) if yolo_enabled else None
    last_reply_time = 0
    debug_verbose = conf.get("debug", {}).get("verbose", False)
    
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

    # 初始化网络监控器
    network_conf = conf.get("network_monitor", {})
    net_monitor = None
    if network_conf.get("enabled", True):
        net_monitor = NetworkMonitor(
            consecutive_failures=network_conf.get("consecutive_failures", 3),
            check_interval=network_conf.get("check_interval", 60),
            timeout=network_conf.get("timeout", 10),
            tolerance_minutes=network_conf.get("tolerance_minutes", 15)
        )
        net_monitor.start_monitoring()
        print(f"🌐 网络监控已启动 - 连续失败阈值: {net_monitor.consecutive_failures}, 容错时间: {net_monitor.tolerance_minutes}分钟")

    detection_count = 0
    last_status_time = time.time()
    
    while True:
        try:
            current_time = time.time()
            conf = get_config()
            app_name = conf.get("chat_app", {}).get("name", "WeChat")
            check_interval = conf.get("monitor", {}).get("check_interval", 30)
            reply_wait = conf.get("monitor", {}).get("reply_wait", 60)

            # 检查进程
            if not check_process(app_name):
                print(f"❌ 未找到 {app_name} 进程 - {datetime.now().strftime('%H:%M:%S')}")
                play_sound("error")
                time.sleep(check_interval)
                continue

            # 检查网络（用network_monitor警报机制）
            if net_monitor:
                alert = net_monitor.get_alert()
                if alert:
                    if alert['type'] == 'network_down':
                        play_sound("warning")
                        print("网络连接异常（已连续多次失败并超过容错时间）")
                        time.sleep(check_interval)
                        continue
                    elif alert['type'] == 'network_restored':
                        print("网络恢复正常")
                        
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
    main() 