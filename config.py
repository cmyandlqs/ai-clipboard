"""
AI Clip - 配置文件
"""

import os
from pathlib import Path

# ==================== 应用信息 ====================
APP_NAME = "AI Clip"
APP_VERSION = "0.1.0"

# ==================== 窗口配置 ====================
MAIN_WINDOW_WIDTH = 520
MAIN_WINDOW_HEIGHT = 120

HISTORY_WINDOW_WIDTH = 480
HISTORY_WINDOW_HEIGHT = 420

# ==================== UI 颜色主题 (macOS Style) ====================
class Colors:
    """macOS 风格配色方案"""
    # 背景色 - macOS 毛玻璃效果色
    BG = "#1c1c1e"                    # 深灰黑背景
    
    # 文字颜色
    FG = "#ffffff"                    # 主文字（白色）
    FG_SECONDARY = "#8e8e93"          # 次要文字（灰色）
    INPUT_FG = "#ffffff"              # 输入框文字
    
    # 输入框背景 - 略浅的灰色
    INPUT_BG = "#2c2c2e"              # 输入框背景
    
    # 强调色 - macOS 蓝
    ACCENT = "#0a84ff"                # macOS 系统蓝
    ACCENT_HOVER = "#409cff"          # 悬停时的蓝色
    
    # 边框
    BORDER = "#3a3a3c"                # 边框色
    
    # 状态色
    SUCCESS = "#30d158"               # 绿色
    WARNING = "#ff9f0a"               # 橙色
    ERROR = "#ff453a"                 # 红色
    
    # 交互
    HOVER = "#3a3a3c"                 # 悬停背景
    DISABLED = "#48484a"              # 禁用状态
    
    # 滚动条
    SCROLL_BG = "#1c1c1e"
    SCROLL_BG_THUMB = "#3a3a3c"
    SCROLL_BG_THUMB_HOVER = "#48484a"
    
    # 历史记录项
    ITEM_BG = "#2c2c2e"
    ITEM_BG_HOVER = "#3a3a3c"

# ==================== 字体配置 ====================
FONTS = {
    "default": ("Microsoft YaHei UI", 10),
    "input": ("Microsoft YaHei UI", 13),
    "small": ("Microsoft YaHei UI", 9),
    "title": ("Microsoft YaHei UI", 11, "bold"),
}

# ==================== 快捷键配置 ====================
HOTKEY_TOGGLE = "ctrl+shift+space"
HOTKEY_SEARCH = "ctrl+f"

# ==================== 剪贴板配置 ====================
MAX_HISTORY = 100
CLIPBOARD_CHECK_INTERVAL = 0.3
PREVIEW_LENGTH = 30

# ==================== 数据存储配置 ====================
if os.name == "nt":
    DATA_DIR = Path(os.environ.get("APPDATA", "~")) / "AI Clip"
else:
    DATA_DIR = Path.home() / ".ai-clip"

DATA_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_FILE = DATA_DIR / "history.json"
CONFIG_FILE = DATA_DIR / "config.json"
HISTORY_RETENTION_DAYS = 7

# ==================== 行为配置 ====================
SAVE_ON_EXIT = True
AUTO_SAVE = True