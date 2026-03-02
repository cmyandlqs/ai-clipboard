"""
AI Clip - 全局快捷键管理
"""

import keyboard
import threading
from typing import Callable, Optional


class HotkeyManager:
    """
    全局快捷键管理器
    使用keyboard库监听全局快捷键
    """

    def __init__(self):
        self._hotkeys = {}  # {hotkey_str: callback}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def register(self, hotkey: str, callback: Callable):
        """
        注册快捷键

        Args:
            hotkey: 快捷键字符串，如 "ctrl+shift+space"
            callback: 回调函数
        """
        self._hotkeys[hotkey] = callback
        keyboard.add_hotkey(hotkey, callback)
        print(f"[Hotkey] 已注册快捷键: {hotkey}")

    def unregister(self, hotkey: str):
        """
        取消注册快捷键

        Args:
            hotkey: 快捷键字符串
        """
        if hotkey in self._hotkeys:
            keyboard.remove_hotkey(hotkey)
            del self._hotkeys[hotkey]
            print(f"[Hotkey] 已取消快捷键: {hotkey}")

    def start(self):
        """启动快捷键监听（阻塞）"""
        self._running = True
        keyboard.wait()

    def stop(self):
        """停止快捷键监听"""
        self._running = False
        # 清除所有快捷键
        for hotkey in list(self._hotkeys.keys()):
            self.unregister(hotkey)

    def is_pressed(self, hotkey: str) -> bool:
        """
        检查快捷键是否被按下

        Args:
            hotkey: 快捷键字符串

        Returns:
            是否被按下
        """
        return keyboard.is_pressed(hotkey)

    @staticmethod
    def write(text: str, delay: float = 0):
        """
        模拟键盘输入

        Args:
            text: 要输入的文本
            delay: 每个字符间的延迟（秒）
        """
        keyboard.write(text, delay=delay)

    @staticmethod
    def press(hotkey: str):
        """
        模拟按键

        Args:
            hotkey: 按键字符串
        """
        keyboard.press_and_release(hotkey)
