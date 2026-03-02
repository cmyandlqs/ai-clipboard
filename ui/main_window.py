"""
AI Clip - 主输入窗口
"""

import tkinter as tk
import pyperclip
import sys

from config import (
    Colors, FONTS,
    MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
)
from utils.helpers import get_window_center, ensure_window_on_screen
from core.config_manager import get_config_manager


class MainWindow(tk.Toplevel):
    """
    主输入窗口
    - 快速输入文本
    - Enter复制到剪贴板并关闭
    - Esc关闭窗口
    """

    def __init__(self, master, on_history_click=None):
        """
        初始化主窗口

        Args:
            master: 父窗口（Tk根窗口）
            on_history_click: 历史按钮点击回调
        """
        super().__init__(master)

        self.on_history_click = on_history_click
        self.visible = False
        self.config_manager = get_config_manager()
        self.master = master

        self._setup_window()
        self._create_widgets()
        self._bind_events()

        # 初始隐藏窗口
        self.withdraw()
        self.visible = False

    def _setup_window(self):
        """设置窗口属性"""
        # 尝试从配置加载位置，否则使用中心位置
        default_x, default_y = get_window_center(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        x, y = self.config_manager.get_window_position("main", default_x, default_y)
        # 确保窗口在屏幕内
        x, y = ensure_window_on_screen(x, y, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        # 设置窗口属性
        self.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}+{x}+{y}")
        self.overrideredirect(True)  # 无边框
        self.attributes("-topmost", True)  # 置顶
        self.configure(bg=Colors.BG)
        self.resizable(False, False)

        # Windows下添加圆角和阴影效果
        if sys.platform == "win32":
            try:
                self._round_window_corners(radius=12)
                self.attributes("-alpha", 0.98)
            except:
                pass

    def _round_window_corners(self, radius: int = 12):
        """设置窗口圆角（Windows）"""
        try:
            import ctypes
            from ctypes import wintypes

            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2

            hwnd = wintypes.HWND(int(self.frame(), 16))
            preference = wintypes.DWORD(DWMWCP_ROUND)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(preference),
                ctypes.sizeof(preference)
            )
        except:
            pass

    def _create_widgets(self):
        """创建界面组件"""
        # 主容器
        self.container = tk.Frame(
            self,
            bg=Colors.BG,
            highlightthickness=1,
            highlightbackground=Colors.BORDER
        )
        self.container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # 输入区域
        self.input_frame = tk.Frame(self.container, bg=Colors.BG)
        self.input_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # 输入框容器（包含输入框和历史按钮）
        self.entry_container = tk.Frame(self.input_frame, bg=Colors.INPUT_BG)
        self.entry_container.pack(fill=tk.BOTH, expand=True)

        # 输入框
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self.entry_container,
            textvariable=self.entry_var,
            font=FONTS["input"],
            bg=Colors.INPUT_BG,
            fg=Colors.INPUT_FG,
            insertbackground=Colors.ACCENT,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 8), pady=12)

        # 历史按钮
        self.history_btn = tk.Label(
            self.entry_container,
            text="📋",
            font=("Segoe UI Emoji", 16),
            bg=Colors.INPUT_BG,
            fg=Colors.FG,
            cursor="hand2"
        )
        self.history_btn.pack(side=tk.RIGHT, padx=(0, 16))
        self.history_btn.bind("<Button-1>", self._on_history_click)
        self.history_btn.bind("<Enter>", lambda e: self.history_btn.config(fg=Colors.ACCENT))
        self.history_btn.bind("<Leave>", lambda e: self.history_btn.config(fg=Colors.FG))

        # 提示文本
        self.hint_label = tk.Label(
            self.container,
            text="按 Enter 复制并关闭",
            font=FONTS["small"],
            bg=Colors.BG,
            fg=Colors.DISABLED
        )
        self.hint_label.pack(pady=(0, 8))

    def _bind_events(self):
        """绑定事件"""
        # 输入框事件绑定
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Escape>", lambda e: self.hide())
        self.entry.bind("<KP_Enter>", self._on_enter)

        # 窗口级别的事件绑定
        self.bind("<Return>", self._on_enter)
        self.bind("<Escape>", lambda e: self.hide())
        self.bind("<KP_Enter>", self._on_enter)

    def _on_history_click(self, event=None):
        """历史按钮点击事件"""
        if self.on_history_click:
            self.on_history_click()

    def _on_enter(self, event=None):
        """Enter键事件 - 复制并关闭"""
        content = self.entry_var.get().strip()

        if content:
            pyperclip.copy(content)
            self.entry_var.set("")  # 清空输入框

        self.hide()
        return 'break'  # 阻止事件传播

    def show(self):
        """显示窗口"""
        if not self.visible:
            self.deiconify()
            self.visible = True
            # 确保窗口在最前面
            self.lift()
            self.attributes("-topmost", True)
            # 聚焦输入框
            self.after(10, self._focus_entry)
            self.after(50, self._ensure_focus)

    def _ensure_focus(self):
        """确保窗口和输入框获得焦点"""
        self.focus_force()
        self.entry.focus_force()

    def hide(self):
        """隐藏窗口"""
        if self.visible:
            self._save_position()
            self.withdraw()
            self.visible = False

    def toggle(self):
        """切换显示/隐藏状态"""
        if self.visible:
            self.hide()
        else:
            self.show()

    def _focus_entry(self):
        """聚焦输入框并全选文本"""
        self.entry.focus_set()
        self.entry.select_range(0, tk.END)

    def _save_position(self):
        """保存窗口位置到配置"""
        try:
            x = self.winfo_x()
            y = self.winfo_y()
            self.config_manager.set_window_position("main", x, y)
            self.config_manager.save()
        except Exception:
            pass

    def get_input_text(self) -> str:
        """获取输入框文本"""
        return self.entry_var.get().strip()

    def set_input_text(self, text: str):
        """设置输入框文本"""
        self.entry_var.set(text)

    def clear_input(self):
        """清空输入框"""
        self.entry_var.set("")


# 现代按钮类
class ModernButton(tk.Label):
    """现代风格按钮"""

    def __init__(self, parent, text="", icon="", command=None, **kwargs):
        default_kwargs = {
            "bg": Colors.INPUT_BG,
            "fg": Colors.FG,
            "font": FONTS["default"],
            "cursor": "hand2",
            "pady": 8,
            "padx": 16
        }
        default_kwargs.update(kwargs)

        display_text = f"{icon} {text}" if icon and text else (icon or text)
        super().__init__(parent, text=display_text, **default_kwargs)

        self.command = command
        self._original_bg = self.cget("bg")

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter_hover)
        self.bind("<Leave>", self._on_leave)

    def _on_click(self, event=None):
        if self.command:
            self.command()

    def _on_enter_hover(self, event=None):
        self.config(bg=Colors.HOVER)

    def _on_leave(self, event=None):
        self.config(bg=self._original_bg)


# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    def on_history():
        print("History button clicked")

    app = MainWindow(root, on_history_click=on_history)
    app.show()

    root.mainloop()
