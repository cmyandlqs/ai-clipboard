"""
AI Clip - 全局快捷键管理
"""

import keyboard
from typing import Callable, Optional


class HotkeyManager:
    """
    全局快捷键管理器
    使用 keyboard 库监听全局快捷键
    """

    def __init__(self):
        self._hotkeys = {}  # {hotkey_str: callback}
        print("[Hotkey] 快捷键管理器已初始化")

    def register(self, hotkey: str, callback: Callable):
        """
        注册快捷键

        Args:
            hotkey: 快捷键字符串，如 "ctrl+shift+space"
            callback: 回调函数
        """
        try:
            self._hotkeys[hotkey] = callback
            keyboard.add_hotkey(hotkey, callback, suppress=False)
            print(f"[Hotkey] 已注册快捷键: {hotkey}")
        except Exception as e:
            print(f"[Hotkey] 注册快捷键失败: {hotkey}, 错误: {e}")

    def unregister(self, hotkey: str):
        """
        取消注册快捷键

        Args:
            hotkey: 快捷键字符串
        """
        if hotkey in self._hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
                del self._hotkeys[hotkey]
                print(f"[Hotkey] 已取消快捷键: {hotkey}")
            except Exception as e:
                print(f"[Hotkey] 取消快捷键失败: {e}")

    def start(self):
        """启动快捷键监听"""
        # keyboard 库会自动处理钩子，无需额外操作
        print("[Hotkey] 快捷键监听已启动")

    def stop(self):
        """停止快捷键监听"""
        try:
            # 清除所有快捷键
            for hotkey in list(self._hotkeys.keys()):
                self.unregister(hotkey)
            # 移除所有钩子
            keyboard.unhook_all()
            print("[Hotkey] 快捷键监听已停止")
        except Exception as e:
            print(f"[Hotkey] 停止快捷键监听失败: {e}")

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