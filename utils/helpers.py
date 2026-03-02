"""
AI Clip - 工具函数
"""

import time
import tkinter as tk
from datetime import datetime
from typing import Tuple, Optional


def get_mouse_position() -> Tuple[int, int]:
    """
    获取当前鼠标指针位置

    Returns:
        (x, y) 鼠标坐标
    """
    root = tk.Tk()
    root.withdraw()
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    root.destroy()
    return x, y


def get_window_near_mouse(window_width: int, window_height: int, offset_x: int = 20, offset_y: int = 20) -> Tuple[int, int]:
    """
    计算窗口在鼠标附近的位置
    
    Args:
        window_width: 窗口宽度
        window_height: 窗口高度
        offset_x: 鼠标 X 偏移量
        offset_y: 鼠标 Y 偏移量
    
    Returns:
        (x, y) 窗口左上角坐标
    """
    mouse_x, mouse_y = get_mouse_position()
    
    # 窗口出现在鼠标右下方
    x = mouse_x + offset_x
    y = mouse_y + offset_y
    
    # 确保窗口在屏幕内
    x, y = ensure_window_on_screen(x, y, window_width, window_height)
    
    return x, y


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
        x: 窗口 x 坐标
        y: 窗口 y 坐标
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

    # 边距
    margin = 10
    taskbar_height = 60  # 预留任务栏高度

    # 确保 x 在屏幕范围内
    if x < margin:
        x = margin
    elif x + width > screen_width - margin:
        x = screen_width - width - margin

    # 确保 y 在屏幕范围内（考虑任务栏）
    if y < margin:
        y = margin
    elif y + height > screen_height - taskbar_height:
        y = screen_height - height - taskbar_height

    return x, y
