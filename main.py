"""
AI Clip - 主程序入口
一款专注于提升与AI对话效率的轻量级剪贴板增强工具

核心功能：
- Ctrl+Shift+Space 快速唤起输入框
- Enter 复制内容到剪贴板并关闭
- 自动监控剪贴板变化
- 历史记录管理
- 系统托盘常驻
"""

import sys
import ctypes

# ============================================
# 启用 Windows 高 DPI 感知（必须在导入 tkinter 之前）
# ============================================
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass

import tkinter as tk

from config import (
    APP_NAME, APP_VERSION,
    HOTKEY_TOGGLE, Colors,
    MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT,
    SAVE_ON_EXIT, AUTO_SAVE
)
from core.hotkey import HotkeyManager
from core.clipboard import ClipboardMonitor
from core.storage import Storage
from core.tray import SystemTray
from core.autostart import AutoStart
from ui.main_window import ModernWindow
from ui.history_window import HistoryWindow


class AIClipApp:
    """AI Clip 主应用类"""

    def __init__(self):
        """初始化应用"""
        # 创建隐藏的根窗口
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.configure(bg=Colors.BG)

        # 初始化存储
        self.storage = Storage()

        # 初始化窗口
        self.main_window = ModernWindow(self.root, on_history_click=self.show_history_window)
        self.history_window = None

        # 初始化剪贴板监控
        self.clipboard_monitor = ClipboardMonitor(
            self.storage,
            on_change=self._on_clipboard_change
        )

        # 初始化快捷键管理
        self.hotkey_manager = HotkeyManager()
        self._setup_hotkeys()

        # 初始化开机自启动
        self.autostart = AutoStart()

        # 初始化系统托盘
        self.tray = SystemTray(
            app_name=APP_NAME,
            on_show=self._on_tray_show,
            on_quit=self.quit_app,
            on_toggle_autostart=self._on_toggle_autostart,
            is_autostart_enabled=self.autostart.is_enabled
        )

        print(f"[{APP_NAME}] v{APP_VERSION} 启动成功")
        print(f"[{APP_NAME}] 历史记录数: {len(self.storage)}")

    def _setup_hotkeys(self):
        """设置快捷键"""
        self.hotkey_manager.register(
            HOTKEY_TOGGLE,
            self._toggle_main_window
        )

    def _toggle_main_window(self):
        """切换主窗口显示/隐藏"""
        if self.main_window.visible:
            self.main_window.hide()
        else:
            self.main_window.show()

    def _on_tray_show(self):
        """托盘点击显示窗口"""
        self.main_window.show()

    def _on_toggle_autostart(self):
        """切换开机自启动"""
        if self.autostart.toggle():
            status = "已启用" if self.autostart.is_enabled() else "已禁用"
            print(f"[{APP_NAME}] 开机自启动: {status}")

    def show_history_window(self):
        """显示历史记录窗口"""
        if self.history_window is None or not self.history_window.winfo_exists():
            self.history_window = HistoryWindow(
                self.main_window,
                self.storage
            )

        if not self.history_window.visible:
            self.history_window.show()

    def _on_clipboard_change(self, record):
        """剪贴板内容变化回调"""
        if AUTO_SAVE:
            self.storage.save_to_file()

    def run(self):
        """运行应用"""
        try:
            # 启动剪贴板监控
            self.clipboard_monitor.start()

            # 启动系统托盘
            self.tray.start()

            # 启动 Tkinter 主循环
            self.root.mainloop()

        except KeyboardInterrupt:
            print(f"\n[{APP_NAME}] 收到退出信号")
        finally:
            self._cleanup()

    def quit_app(self):
        """退出应用"""
        print(f"[{APP_NAME}] 正在退出...")
        self._cleanup()
        self.root.quit()

    def _cleanup(self):
        """清理资源"""
        # 停止剪贴板监控
        self.clipboard_monitor.stop()

        # 停止快捷键监听
        self.hotkey_manager.stop()

        # 停止系统托盘
        self.tray.stop()

        # 保存历史记录
        if SAVE_ON_EXIT:
            self.storage.save_to_file()
            print(f"[{APP_NAME}] 已保存 {len(self.storage)} 条历史记录")


def main():
    """程序入口"""
    print("=" * 40)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("  按 Ctrl+Shift+Space 唤起输入框")
    print("  系统托盘运行中...")
    print("=" * 40)

    app = AIClipApp()
    app.run()


if __name__ == "__main__":
    main()