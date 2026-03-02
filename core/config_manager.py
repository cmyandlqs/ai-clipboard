"""
AI Clip - 配置管理器
负责加载和保存用户配置（如窗口位置）
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from config import CONFIG_FILE


class ConfigManager:
    """
    配置管理器
    """

    def __init__(self):
        """初始化配置管理器"""
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self):
        """从文件加载配置"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
            except Exception as e:
                print(f"[Config] 加载配置失败: {e}")
                self._config = {}
        else:
            self._config = {}

    def save(self):
        """保存配置到文件"""
        try:
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"[Config] 保存配置失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键（支持点号分隔的嵌套键，如 "window.main.x"）
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        设置配置值

        Args:
            key: 配置键（支持点号分隔的嵌套键）
            value: 配置值
        """
        keys = key.split(".")
        config = self._config

        # 导航到最后一级的父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value

    def get_window_position(self, window_name: str, default_x: int, default_y: int) -> tuple:
        """
        获取窗口位置

        Args:
            window_name: 窗口名称（如 "main", "history"）
            default_x: 默认X坐标
            default_y: 默认Y坐标

        Returns:
            (x, y) 坐标
        """
        x = self.get(f"window.{window_name}.x", default_x)
        y = self.get(f"window.{window_name}.y", default_y)
        return int(x), int(y)

    def set_window_position(self, window_name: str, x: int, y: int):
        """
        设置窗口位置

        Args:
            window_name: 窗口名称
            x: X坐标
            y: Y坐标
        """
        self.set(f"window.{window_name}.x", x)
        self.set(f"window.{window_name}.y", y)

    def __repr__(self):
        return f"ConfigManager({self._config})"


# 全局单例
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """获取全局配置管理器单例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
