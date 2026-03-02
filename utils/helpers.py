"""
AI Clip - 工具函数
"""

import time
from datetime import datetime
from typing import Tuple


def format_timestamp(ts: float = None) -> str:
    """
    格式化时间戳为 HH:MM 格式

    Args:
        ts: Unix时间戳，如果为None则使用当前时间

    Returns:
        格式化后的时间字符串
    """
    if ts is None:
        ts = time.time()
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%H:%M")


def truncate_text(text: str, max_length: int = 30, suffix: str = "...") -> str:
    """
    截断文本到指定长度

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀（如省略号）

    Returns:
        截断后的文本
    """
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_window_center(window_width: int, window_height: int) -> Tuple[int, int]:
    """
    计算窗口屏幕中心位置

    Args:
        window_width: 窗口宽度
        window_height: 窗口高度

    Returns:
        (x, y) 坐标
    """
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # 隐藏临时窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    return x, y


def ensure_window_on_screen(x: int, y: int, width: int, height: int) -> Tuple[int, int]:
    """
    确保窗口坐标在屏幕可见范围内

    Args:
        x: 窗口x坐标
        y: 窗口y坐标
        width: 窗口宽度
        height: 窗口高度

    Returns:
        调整后的 (x, y) 坐标
    """
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    # 确保窗口不完全超出屏幕
    if x + width < 50:
        x = 50
    elif x > screen_width - 50:
        x = screen_width - width - 50

    if y + height < 50:
        y = 50
    elif y > screen_height - 50:
        y = screen_height - height - 50

    return x, y
