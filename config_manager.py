import os
import yaml
import time
import threading
from typing import Dict, Any, Callable

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️  watchdog未安装，文件监控功能不可用")

class ConfigManager:
    """配置管理器，支持热更新"""
    def __init__(self, config_path: str = "config_with_yolo.yaml"):
        self.config_path = config_path
        self.config = {}
        self.last_modified = 0
        self.callbacks = {}  # 存储配置变更的回调函数
        self.observer = None
        self.is_watching = False
        # 初始加载配置
        self.load_config()
        # 启动文件监控
        self.start_watching()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                current_modified = os.path.getmtime(self.config_path)
                # 检查文件是否被修改
                if current_modified > self.last_modified:
                    # 添加延迟，确保文件写入完成
                    time.sleep(0.1)
                    
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        new_config = yaml.safe_load(f)
                        if new_config:
                            old_config = self.config.copy()
                            self.config = new_config
                            self.last_modified = current_modified
                            
                            # 添加调试信息
                            # print(f"🔄 配置更新调试信息:")
                            # print(f"  旧配置中的target_contacts: {old_config.get('chat_app', {}).get('target_contacts', [])}")
                            # print(f"  新配置中的target_contacts: {new_config.get('chat_app', {}).get('target_contacts', [])}")
                            
                            # 通知配置变更
                            self._notify_config_changed(old_config, new_config)
                            print(f"✅ 配置文件已更新: {self.config_path}")
                            return new_config
            else:
                print(f"⚠️  配置文件不存在: {self.config_path}")
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
        return self.config

    def get_config(self, key_path: str = None, default: Any = None) -> Any:
        """获取配置值"""
        if key_path is None:
            return self.config
        keys = key_path.split('.')
        current = self.config
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def register_callback(self, config_key: str, callback: Callable[[Any, Any], None]):
        """注册配置变更回调函数"""
        if config_key not in self.callbacks:
            self.callbacks[config_key] = []
        self.callbacks[config_key].append(callback)
        print(f"✅ 已注册配置变更回调: {config_key}")

    def _notify_config_changed(self, old_config: Dict, new_config: Dict):
        """通知配置变更"""
        for config_key, callbacks in self.callbacks.items():
            old_value = self._get_nested_value(old_config, config_key)
            new_value = self._get_nested_value(new_config, config_key)
            if old_value != new_value:
                print(f"🔄 配置变更: {config_key}")
                print(f"旧值: {old_value}")
                print(f"新值: {new_value}")
                for callback in callbacks:
                    try:
                        callback(new_value, old_value)
                    except Exception as e:
                        print(f"❌ 配置变更回调执行失败: {e}")

    def _get_nested_value(self, config: Dict, key_path: str) -> Any:
        """获取嵌套配置值"""
        keys = key_path.split('.')
        current = config
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return None

    def start_watching(self):
        """启动文件监控"""
        if not WATCHDOG_AVAILABLE:
            print("⚠️  watchdog不可用，跳过文件监控")
            return
        if self.is_watching:
            return
        try:
            # Observer：watchdog 检测文件变更
            self.observer = Observer()
            event_handler = ConfigFileHandler(self)
            self.observer.schedule(event_handler, path=os.path.dirname(self.config_path) or '.', recursive=False)
            self.observer.start()
            self.is_watching = True
            print(f"✅ 开始监控配置文件: {self.config_path}")
        except Exception as e:
            print(f"❌ 启动文件监控失败: {e}")

    def stop_watching(self):
        """停止文件监控"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.is_watching = False
            print("✅ 已停止文件监控")

    # 便捷配置获取方法
    def get_yolo_config(self) -> Dict[str, Any]:
        """获取YOLO配置"""
        yolo_conf = self.get_config("yolo", {})
        
        # 检查是否禁用YOLO
        disable_yolo = os.environ.get('CHATMONITOR_DISABLE_YOLO') == '1'
        
        config = {
            "enabled": False if disable_yolo else yolo_conf.get("enabled", True),
            "model_path": yolo_conf.get("model_path", "models/best.pt"),
            "confidence": yolo_conf.get("confidence", 0.35),
            "disable_reason": "环境变量禁用" if disable_yolo else None
        }
        
        return config

    def get_ocr_config(self) -> Dict[str, Any]:
        """获取OCR配置"""
        ocr_conf = self.get_config("ocr.tesseract", {})
        
        return {
            "lang": ocr_conf.get("lang", "chi_sim+eng"),
            "psm": ocr_conf.get("config", "--psm 6").split()[-1]
        }

    def get_monitor_config(self) -> Dict[str, Any]:
        """获取监控配置"""
        monitor_conf = self.get_config("monitor", {})
        
        return {
            "check_interval": monitor_conf.get("check_interval", 3),
            "reply_wait": monitor_conf.get("reply_wait", 60)
        }

    def get_debug_config(self) -> Dict[str, Any]:
        """获取调试配置"""
        debug_conf = self.get_config("debug", {})
        
        return {
            "verbose": debug_conf.get("verbose", False),
            "debug_log": os.environ.get('CHATMONITOR_DEBUG') == '1',
            "remote_debug": os.environ.get('CHATMONITOR_REMOTE_DEBUG') == '1'
        }

    def get_chat_app_config(self) -> Dict[str, Any]:
        """获取聊天应用配置"""
        chat_conf = self.get_config("chat_app", {})
        
        return {
            "name": chat_conf.get("name", "WeChat"),
            "target_contacts": chat_conf.get("target_contacts", [])
        }

    def get_network_config(self) -> Dict[str, Any]:
        """获取网络监控配置"""
        network_conf = self.get_config("network_monitor", {})
        
        return {
            "enabled": network_conf.get("enabled", True),
            "check_interval": network_conf.get("check_interval", 10),
            "timeout": network_conf.get("timeout", 5),
            "consecutive_failures": network_conf.get("consecutive_failures", 3),
            "tolerance_minutes": network_conf.get("tolerance_minutes", 0.1)
        }
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            # 重新加载配置
            self.load_config()
            
            print(f"✅ 配置已保存: {self.config_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False

    def update_network_config(self, new_config: Dict[str, Any]) -> bool:
        """更新网络监控配置"""
        try:
            # 读取当前配置
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 确保 network_monitor 部分存在
            if "network_monitor" not in config:
                config["network_monitor"] = {}
            
            # 更新网络监控配置
            config["network_monitor"].update(new_config)
            
            # 保存配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            # 重新加载配置
            self.load_config()
            
            print(f"✅ 网络监控配置已更新: {new_config}")
            return True
            
        except Exception as e:
            print(f"❌ 更新网络监控配置失败: {e}")
            return False

    def get_monitor_states(self) -> Dict[str, bool]:
        """获取监控开关状态"""
        monitor_conf = self.get_config("monitor", {})
        return {
            "process_monitor_on": monitor_conf.get("process_monitor_on", True),
            "network_monitor_on": monitor_conf.get("network_monitor_on", True)
        }

    def set_monitor_states(self, states: Dict[str, bool]) -> bool:
        """设置监控开关状态"""
        try:
            # 读取当前配置
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 确保 monitor 部分存在
            if "monitor" not in config:
                config["monitor"] = {}
            
            # 更新监控开关状态
            for key, value in states.items():
                config["monitor"][key] = value
            
            # 保存配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            # 重新加载配置
            self.load_config()
            
            print(f"✅ 监控开关状态已更新: {states}")
            return True
            
        except Exception as e:
            print(f"❌ 更新监控开关状态失败: {e}")
            return False

if WATCHDOG_AVAILABLE:
    class ConfigFileHandler(FileSystemEventHandler):
        """配置文件变更处理器"""
        def __init__(self, config_manager: ConfigManager):
            self.config_manager = config_manager
            self.last_modified = 0
        def on_modified(self, event):
            if not event.is_directory and os.path.abspath(event.src_path) == os.path.abspath(self.config_manager.config_path):
                # 避免重复触发
                current_time = time.time()
                if current_time - self.last_modified > 2:  # 2秒内只触发一次，增加延迟
                    self.last_modified = current_time
                    print(f"🔄 检测到配置文件变更: {event.src_path}")
                    # 延迟加载，确保文件写入完成
                    threading.Timer(1.0, self.config_manager.load_config).start()

# 全局配置管理器实例
config_manager = None

def init_config_manager(config_path: str = "config_with_yolo.yaml") -> ConfigManager:
    """初始化全局配置管理器"""
    global config_manager
    if config_manager is None:
        config_manager = ConfigManager(config_path)
    return config_manager

def get_config_manager() -> ConfigManager:
    """获取全局配置管理器"""
    return config_manager 