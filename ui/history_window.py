"""
AI Clip - 历史记录窗口
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import pyperclip
import time

from config import (
    Colors, FONTS,
    HISTORY_WINDOW_WIDTH, HISTORY_WINDOW_HEIGHT,
    HOTKEY_SEARCH
)
from utils.helpers import format_timestamp, ensure_window_on_screen
from core.config_manager import get_config_manager


class HistoryWindow(tk.Toplevel):
    """
    历史记录窗口
    - 显示剪贴板历史
    - 搜索过滤
    - 点击复制
    """

    def __init__(self, parent, storage):
        """
        初始化历史窗口

        Args:
            parent: 父窗口
            storage: 存储管理器
        """
        super().__init__(parent)

        self.storage = storage
        self.visible = False
        self.current_items = []  # 当前显示的记录
        self.config_manager = get_config_manager()

        self._setup_window()
        self._create_widgets()
        self._bind_events()
        self._setup_scrollbar_style()

        # 加载历史记录
        self.refresh_history()

        # 初始隐藏
        self.withdraw()

    def _setup_window(self):
        """设置窗口属性"""
        # 尝试从配置加载位置，否则在父窗口下方显示
        default_x = self.master.winfo_x()
        default_y = self.master.winfo_y() + 150
        x, y = self.config_manager.get_window_position("history", default_x, default_y)

        # 确保在屏幕内
        x, y = ensure_window_on_screen(x, y, HISTORY_WINDOW_WIDTH, HISTORY_WINDOW_HEIGHT)

        # 设置窗口属性
        self.geometry(f"{HISTORY_WINDOW_WIDTH}x{HISTORY_WINDOW_HEIGHT}+{x}+{y}")
        self.overrideredirect(True)  # 无边框
        self.attributes("-topmost", True)  # 置顶
        self.configure(bg=Colors.BG)
        self.resizable(False, False)

        # 圆角效果（Windows）
        if self.master.tk.call("tk", "windowingsystem") == "win32":
            try:
                self._round_window_corners(radius=12)
                self.attributes("-alpha", 0.98)
            except:
                pass

    def _round_window_corners(self, radius: int = 12):
        """设置窗口圆角"""
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

    def _setup_scrollbar_style(self):
        """设置滚动条样式"""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Vertical.TScrollbar",
            background=Colors.SCROLL_BG_THUMB,
            troughcolor=Colors.SCROLL_BG,
            bordercolor=Colors.BG,
            arrowcolor=Colors.FG,
            width=8
        )

    def _create_widgets(self):
        """创建界面组件"""
        # 主容器
        self.container = tk.Frame(
            self,
            bg=Colors.BG,
            highlightthickness=1,
            highlightbackground=Colors.BORDER
        )
        self.container.pack(fill=tk.BOTH, expand=True)

        # 标题栏（搜索框 + 关闭按钮）
        self._create_header()

        # 历史列表容器
        self.list_container = tk.Frame(self.container, bg=Colors.BG)
        self.list_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # 创建Canvas + Scrollbar的列表
        self.canvas = tk.Canvas(
            self.list_container,
            bg=Colors.BG,
            highlightthickness=0,
            borderwidth=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.canvas,
            orient="vertical",
            command=self.canvas.yview
        )

        # 可滚动区域
        self.scrollable_frame = tk.Frame(self.canvas, bg=Colors.BG)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 创建窗口
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=HISTORY_WINDOW_WIDTH - 30
        )

        # 配置滚动
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 鼠标滚轮支持
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _create_header(self):
        """创建标题栏"""
        header = tk.Frame(self.container, bg=Colors.BG)
        header.pack(fill=tk.X, padx=12, pady=(12, 8))

        # 左侧：搜索框
        search_frame = tk.Frame(header, bg=Colors.INPUT_BG)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS["default"],
            bg=Colors.INPUT_BG,
            fg=Colors.INPUT_FG,
            insertbackground=Colors.ACCENT,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 8), pady=8)
        self.search_entry.bind("<KeyRelease-Escape>", lambda e: self.hide())

        # 搜索图标
        search_label = tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI Emoji", 12),
            bg=Colors.INPUT_BG,
            fg=Colors.DISABLED
        )
        search_label.pack(side=tk.RIGHT, padx=(0, 12))

        # 右侧：关闭按钮
        close_btn = tk.Label(
            header,
            text="✕",
            font=FONTS["title"],
            bg=Colors.BG,
            fg=Colors.FG,
            cursor="hand2",
            padx=8
        )
        close_btn.pack(side=tk.RIGHT, padx=(8, 0))
        close_btn.bind("<Button-1>", lambda e: self.hide())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=Colors.ACCENT))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=Colors.FG))

    def _bind_events(self):
        """绑定事件"""
        # 点击外部关闭
        self.bind("<FocusOut>", self._on_focus_out)
        # 搜索快捷键
        self.bind("<Control-f>", lambda e: self.search_entry.focus_set())

    def _on_focus_out(self, event):
        """失去焦点时隐藏"""
        # 延迟检查，避免点击列表项时关闭
        self.after(100, self._check_focus)

    def _check_focus(self):
        """检查是否应该关闭"""
        try:
            if self.focus_get() is None:
                self.hide()
        except:
            pass

    def _on_mousewheel(self, event):
        """鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_search_change(self, *args):
        """搜索内容变化"""
        keyword = self.search_var.get().strip()
        self._render_history(self.storage.search(keyword))

    def refresh_history(self):
        """刷新历史记录"""
        self._render_history(self.storage.get_latest())

    def _render_history(self, items):
        """
        渲染历史记录列表

        Args:
            items: 记录列表
        """
        self.current_items = items

        # 清空现有内容
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not items:
            # 无记录提示
            no_result = tk.Label(
                self.scrollable_frame,
                text="没有找到历史记录",
                font=FONTS["small"],
                bg=Colors.BG,
                fg=Colors.DISABLED
            )
            no_result.pack(pady=40)
            return

        # 渲染每条记录
        for i, record in enumerate(items):
            self._create_history_item(record, i)

        # 更新滚动区域
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _create_history_item(self, record, index):
        """
        创建历史记录项

        Args:
            record: 记录字典
            index: 索引
        """
        # 容器
        item_frame = tk.Frame(
            self.scrollable_frame,
            bg=Colors.INPUT_BG,
            highlightthickness=1,
            highlightbackground=Colors.BORDER
        )
        item_frame.pack(fill=tk.X, padx=8, pady=4)

        # 绑定点击事件
        item_frame.bind("<Button-1>", lambda e, r=record: self._on_item_click(r))
        item_frame.bind("<Enter>", lambda e, f=item_frame: self._on_item_enter(f))
        item_frame.bind("<Leave>", lambda e, f=item_frame: self._on_item_leave(f))

        # 内容区域
        content_frame = tk.Frame(item_frame, bg=Colors.INPUT_BG)
        content_frame.pack(fill=tk.X, padx=12, pady=10)

        # 图标 + 时间 + 预览
        header_frame = tk.Frame(content_frame, bg=Colors.INPUT_BG)
        header_frame.pack(fill=tk.X)

        # 图标
        icon = tk.Label(
            header_frame,
            text="📋",
            font=("Segoe UI Emoji", 10),
            bg=Colors.INPUT_BG,
            fg=Colors.FG
        )
        icon.pack(side=tk.LEFT)

        # 时间
        time_str = format_timestamp(record["timestamp"])
        time_label = tk.Label(
            header_frame,
            text=time_str,
            font=FONTS["small"],
            bg=Colors.INPUT_BG,
            fg=Colors.DISABLED
        )
        time_label.pack(side=tk.LEFT, padx=(6, 0))

        # 预览文本
        preview_text = record["preview"]
        preview_label = tk.Label(
            header_frame,
            text=preview_text,
            font=FONTS["default"],
            bg=Colors.INPUT_BG,
            fg=Colors.FG,
            anchor="w"
        )
        preview_label.pack(side=tk.LEFT, padx=(8, 0))

        # 绑定点击事件到子组件
        for widget in [icon, time_label, preview_label, content_frame]:
            widget.bind("<Button-1>", lambda e, r=record: self._on_item_click(r))
            widget.bind("<Enter>", lambda e, f=item_frame: self._on_item_enter(f))
            widget.bind("<Leave>", lambda e, f=item_frame: self._on_item_leave(f))

    def _on_item_enter(self, frame):
        """鼠标悬停事件"""
        frame.config(highlightbackground=Colors.ACCENT)

    def _on_item_leave(self, frame):
        """鼠标离开事件"""
        frame.config(highlightbackground=Colors.BORDER)

    def _on_item_click(self, record):
        """
        点击历史记录项

        Args:
            record: 记录字典
        """
        # 复制到剪贴板
        pyperclip.copy(record["content"])
        print(f"[History] 已复制: {record['preview']}")

        # 关闭窗口
        self.hide()

        # 如果主窗口可见，也关闭主窗口
        if hasattr(self.master, "visible") and self.master.visible:
            self.master.hide()

    def show(self):
        """显示窗口"""
        self.deiconify()
        self.visible = True
        # 聚焦搜索框
        self.after(10, lambda: self.search_entry.focus_set())

    def hide(self):
        """隐藏窗口"""
        # 保存窗口位置
        try:
            x = self.winfo_x()
            y = self.winfo_y()
            self.config_manager.set_window_position("history", x, y)
            self.config_manager.save()
        except Exception:
            pass

        self.withdraw()
        self.visible = False


# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    from core.storage import Storage

    storage = Storage()
    # 添加测试数据
    import time
    storage.add("def hello_world():\n    print('Hello, World!')")
    storage.add("https://github.com/example/project")
    storage.add("请帮我解释这段代码的执行流程")

    history = HistoryWindow(root, storage)
    history.show()

    root.mainloop()
