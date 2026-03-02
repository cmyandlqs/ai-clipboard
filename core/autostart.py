"""
AI Clip - 开机自启动模块
"""

import sys
import os
from pathlib import Path

if sys.platform == "win32":
    import winreg


class AutoStart:
    """开机自启动管理"""

    APP_NAME = "AI Clip"

    def __init__(self):
        self._exe_path = self._get_exe_path()

    def _get_exe_path(self) -> str:
        """获取可执行文件路径"""
        if getattr(sys, 'frozen', False):
            # PyInstaller 打包后
            return sys.executable
        else:
            # 开发环境
            return os.path.abspath("main.py")

    def is_enabled(self) -> bool:
        """检查是否已启用开机自启动"""
        if sys.platform != "win32":
            return False

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, self.APP_NAME)
                winreg.CloseKey(key)
                return self._exe_path in value
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            print(f"[AutoStart] 检查自启动状态失败: {e}")
            return False

    def enable(self) -> bool:
        """启用开机自启动"""
        if sys.platform != "win32":
            print("[AutoStart] 仅支持 Windows 系统")
            return False

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )

            # 设置注册表值
            winreg.SetValueEx(
                key,
                self.APP_NAME,
                0,
                winreg.REG_SZ,
                f'"{self._exe_path}"'
            )
            winreg.CloseKey(key)
            print(f"[AutoStart] 已启用开机自启动: {self._exe_path}")
            return True

        except Exception as e:
            print(f"[AutoStart] 启用自启动失败: {e}")
            return False

    def disable(self) -> bool:
        """禁用开机自启动"""
        if sys.platform != "win32":
            return False

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )

            try:
                winreg.DeleteValue(key, self.APP_NAME)
                print("[AutoStart] 已禁用开机自启动")
                result = True
            except FileNotFoundError:
                result = True  # 本来就没有

            winreg.CloseKey(key)
            return result

        except Exception as e:
            print(f"[AutoStart] 禁用自启动失败: {e}")
            return False

    def toggle(self) -> bool:
        """切换开机自启动状态"""
        if self.is_enabled():
            return self.disable()
        else:
            return self.enable()