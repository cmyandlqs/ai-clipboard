"""
AI Clip - 配置文件
"""

import os
from pathlib import Path

# ==================== 应用信息 ====================
APP_NAME = "AI Clip"
APP_VERSION = "0.1.0"

# ==================== 窗口配置 ====================
# 主窗口尺寸
MAIN_WINDOW_WIDTH = 600
MAIN_WINDOW_HEIGHT = 120

# 历史窗口尺寸
HISTORY_WINDOW_WIDTH = 500
HISTORY_WINDOW_HEIGHT = 450

# ==================== UI颜色主题 ====================
class Colors:
    """深色主题配色方案"""
    BG = "#1e1e1e"           # 主背景
    FG = "#e0e0e0"           # 主文字
    INPUT_BG = "#2d2d2d"     # 输入框背景
    INPUT_FG = "#ffffff"     # 输入框文字
    ACCENT = "#0078d4"       # 强调色
    BORDER = "#3a3a3a"       # 边框
    HOVER = "#404040"        # 悬停效果
    DISABLED = "#555555"      # 禁用状态
    SCROLL_BG = "#2d2d2d"    # 滚动条背景
    SCROLL_BG_THUMB = "#4a4a4a"  # 滚动条滑块

# ==================== 字体配置 ====================
FONTS = {
    "default": ("Microsoft YaHei UI", 10),
    "input": ("Microsoft YaHei UI", 11),
    "small": ("Microsoft YaHei UI", 9),
    "title": ("Microsoft YaHei UI", 10, "bold"),
}

# ==================== 快捷键配置 ====================
HOTKEY_TOGGLE = "ctrl+shift+space"  # 主窗口切换
HOTKEY_SEARCH = "ctrl+f"            # 搜索框聚焦

# ==================== 剪贴板配置 ====================
MAX_HISTORY = 100           # 最大历史记录数
CLIPBOARD_CHECK_INTERVAL = 0.3  # 剪贴板检查间隔（秒）
PREVIEW_LENGTH = 30         # 预览文本长度

# ==================== 数据存储配置 ====================
# 获取用户数据目录
if os.name == "nt":  # Windows
    DATA_DIR = Path(os.environ.get("APPDATA", "~")) / "AI Clip"
else:
    DATA_DIR = Path.home() / ".ai-clip"

# 确保数据目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 数据文件路径
HISTORY_FILE = DATA_DIR / "history.json"
CONFIG_FILE = DATA_DIR / "config.json"

# 历史保留天数
HISTORY_RETENTION_DAYS = 7

# ==================== 窗口属性 ====================
WINDOW_ATTRIBUTES = {
    "overrideredirect": True,      # 无边框窗口
    "topmost": True,                # 置顶
    "bg": Colors.BG,
}

# ==================== 行为配置 ====================
SAVE_ON_EXIT = True        # 退出时保存历史
AUTO_SAVE = True           # 自动保存（每次变更）
MINIMIZE_TO_TRAY = False   # 最小化到托盘（暂未实现）
