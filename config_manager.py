import os
import yaml
import time
import threading
from typing import Dict, Any, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        new_config = yaml.safe_load(f)
                        if new_config:
                            old_config = self.config.copy()
                            self.config = new_config
                            self.last_modified = current_modified
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
        if self.is_watching:
            return
        try:
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

class ConfigFileHandler(FileSystemEventHandler):
    """配置文件变更处理器"""
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.last_modified = 0
    def on_modified(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) == os.path.abspath(self.config_manager.config_path):
            # 避免重复触发
            current_time = time.time()
            if current_time - self.last_modified > 1:  # 1秒内只触发一次
                self.last_modified = current_time
                print(f"🔄 检测到配置文件变更: {event.src_path}")
                # 延迟加载，确保文件写入完成
                threading.Timer(0.5, self.config_manager.load_config).start()

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