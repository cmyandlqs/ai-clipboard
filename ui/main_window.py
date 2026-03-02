"""
AI Clip - 主输入窗口
macOS 风格圆角设计 + 可拖动
"""

import tkinter as tk
import pyperclip
import sys
import ctypes
from typing import Optional, Callable

from config import Colors, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
from utils.helpers import get_window_near_mouse, ensure_window_on_screen
from core.config_manager import get_config_manager


class ModernWindow(tk.Toplevel):
    """macOS 风格主输入窗口"""

    def __init__(self, master, on_history_click: Optional[Callable] = None):
        super().__init__(master)

        self.on_history_click = on_history_click
        self.visible = False
        self.config_manager = get_config_manager()
        self.master = master
        self._animating = False

        # 拖动状态
        self._drag_start_x = 0
        self._drag_start_y = 0

        self._setup_window()
        self._create_widgets()
        self._bind_events()

        self.withdraw()
        self.visible = False

    def _setup_window(self):
        """设置窗口属性"""
        try:
            self._dpi_scale = self.winfo_fpixels('1i') / 96.0
        except:
            self._dpi_scale = 1.0

        width = int(MAIN_WINDOW_WIDTH * self._dpi_scale)
        height = int(MAIN_WINDOW_HEIGHT * self._dpi_scale)

        x, y = get_window_near_mouse(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        x, y = ensure_window_on_screen(x, y, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg=Colors.BG)

        if sys.platform == "win32":
            self._apply_rounded_corners()

        self.resizable(False, False)

    def _apply_rounded_corners(self):
        """应用 Windows 圆角效果"""
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            if hwnd == 0:
                hwnd = int(self.frame(), 16)

            # DWMWCP_ROUND = 2 (圆角), DWMWCP_ROUNDSMALL = 3 (小圆角)
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            preference = ctypes.c_int(2)  # 圆角
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(preference), ctypes.sizeof(preference)
            )

            self.attributes("-alpha", 0.0)
        except Exception as e:
            print(f"[Window] 圆角设置: {e}")

    def _create_widgets(self):
        """创建界面组件"""
        # 主容器（可拖动）
        self.container = tk.Frame(self, bg=Colors.BG, cursor="fleur")
        self.container.pack(fill=tk.BOTH, expand=True)

        # 绑定拖动事件到容器
        self._bind_drag(self.container)

        # 输入区域
        self._create_input_area()

        # 底部提示
        self._create_hint_area()

    def _create_input_area(self):
        """创建输入区域"""
        # 外层容器
        input_wrapper = tk.Frame(self.container, bg=Colors.BG)
        input_wrapper.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 6))
        self._bind_drag(input_wrapper)

        # 输入框容器
        self.entry_frame = tk.Frame(
            input_wrapper,
            bg=Colors.INPUT_BG,
            highlightthickness=1,
            highlightbackground=Colors.BORDER
        )
        self.entry_frame.pack(fill=tk.BOTH, expand=True)
        self._bind_drag(self.entry_frame)

        # 输入框
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self.entry_frame,
            textvariable=self.entry_var,
            font=("Microsoft YaHei UI", 13),
            bg=Colors.INPUT_BG,
            fg=Colors.INPUT_FG,
            insertbackground=Colors.ACCENT,
            insertwidth=2,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            selectbackground=Colors.ACCENT,
            selectforeground="#ffffff",
            cursor="xterm"  # 输入框内显示文本光标
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=14, pady=12)

        # 历史按钮
        self.history_btn = tk.Label(
            self.entry_frame,
            text="⏱",
            font=("Segoe UI Symbol", 16),
            bg=Colors.INPUT_BG,
            fg=Colors.FG_SECONDARY,
            cursor="hand2"
        )
        self.history_btn.pack(side=tk.RIGHT, padx=(0, 12))
        self.history_btn.bind("<Button-1>", self._on_history_click)
        self.history_btn.bind("<Enter>", lambda e: self.history_btn.config(fg=Colors.ACCENT))
        self.history_btn.bind("<Leave>", lambda e: self.history_btn.config(fg=Colors.FG_SECONDARY))

        # 聚焦效果
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _create_hint_area(self):
        """创建底部提示区域"""
        hint_frame = tk.Frame(self.container, bg=Colors.BG)
        hint_frame.pack(fill=tk.X, padx=12, pady=(0, 10))
        self._bind_drag(hint_frame)

        # 左侧 - 作者署名
        author_label = tk.Label(
            hint_frame,
            text="✦ Crafted by 最菜灰夫人",
            font=("Microsoft YaHei UI", 8),
            bg=Colors.BG,
            fg=Colors.FG_SECONDARY,
            cursor="fleur"
        )
        author_label.pack(side=tk.LEFT)
        self._bind_drag(author_label)

        # 右侧 - 快捷键提示
        hint_label = tk.Label(
            hint_frame,
            text="Enter 复制  ·  Esc 关闭",
            font=("Microsoft YaHei UI", 8),
            bg=Colors.BG,
            fg=Colors.FG_SECONDARY,
            cursor="fleur"
        )
        hint_label.pack(side=tk.RIGHT)
        self._bind_drag(hint_label)

    def _bind_drag(self, widget):
        """绑定拖动事件到组件"""
        widget.bind("<Button-1>", self._start_drag)
        widget.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        """开始拖动"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _do_drag(self, event):
        """执行拖动"""
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def _on_focus_in(self, event=None):
        """聚焦效果"""
        self.entry_frame.config(highlightbackground=Colors.ACCENT)

    def _on_focus_out(self, event=None):
        """失焦效果"""
        self.entry_frame.config(highlightbackground=Colors.BORDER)

    def _bind_events(self):
        """绑定事件"""
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<KP_Enter>", self._on_enter)
        self.entry.bind("<Escape>", self._on_escape)
        self.bind("<Escape>", self._on_escape)

    def _on_escape(self, event=None):
        """Esc 关闭窗口"""
        self.hide()
        return 'break'

    def _on_history_click(self, event=None):
        """历史按钮点击"""
        if self.on_history_click:
            self.hide()
            self.on_history_click()

    def _on_enter(self, event=None):
        """Enter 复制并关闭"""
        content = self.entry_var.get().strip()
        if content:
            pyperclip.copy(content)
            self.entry_var.set("")
        self.hide()
        return 'break'

    def show(self, at_mouse: bool = True):
        """显示窗口"""
        if self.visible:
            return

        if at_mouse:
            x, y = get_window_near_mouse(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
            self.geometry(f"+{x}+{y}")

        self.deiconify()
        self.visible = True
        self.lift()
        self.attributes("-topmost", True)

        self._animating = True
        self._fade_in(0.0)

    def _fade_in(self, alpha: float):
        """淡入动画"""
        if not self.visible:
            return
        if alpha >= 1.0:
            self.attributes("-alpha", 1.0)
            self._animating = False
            self.after(30, self._focus_entry)
            return
        self.attributes("-alpha", alpha)
        self.after(15, lambda: self._fade_in(alpha + 0.12))

    def hide(self):
        """隐藏窗口"""
        if not self.visible:
            return
        self.visible = False
        self._animating = False
        self.attributes("-alpha", 0.0)
        self.withdraw()
        self.update()
        self._save_position()

    def _focus_entry(self):
        """聚焦输入框"""
        if self.visible:
            self.focus_force()
            self.entry.focus_force()
            self.entry.select_range(0, tk.END)
            self.entry.icursor(tk.END)

    def _save_position(self):
        """保存位置"""
        try:
            x, y = self.winfo_x(), self.winfo_y()
            self.config_manager.set_window_position("main", x, y)
            self.config_manager.save()
        except:
            pass

    def toggle(self):
        """切换显示"""
        if self.visible:
            self.hide()
        else:
            self.show(at_mouse=True)

    def get_input_text(self) -> str:
        return self.entry_var.get().strip()

    def set_input_text(self, text: str):
        self.entry_var.set(text)

    def clear_input(self):
        self.entry_var.set("")


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            pass

    root = tk.Tk()
    root.withdraw()
    app = ModernWindow(root, on_history_click=lambda: print("History"))
    root.after(500, app.show)
    root.mainloop()