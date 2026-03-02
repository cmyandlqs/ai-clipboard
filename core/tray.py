"""
AI Clip - 系统托盘模块
"""

import sys
import os
from typing import Callable, Optional

from PIL import Image, ImageDraw

try:
    import pystray
    from pystray import MenuItem, Menu
except ImportError:
    pystray = None


class SystemTray:
    """系统托盘管理器"""

    def __init__(
        self,
        app_name: str = "AI Clip",
        on_show: Optional[Callable] = None,
        on_quit: Optional[Callable] = None,
        on_toggle_autostart: Optional[Callable] = None,
        is_autostart_enabled: Optional[Callable] = None
    ):
        self.app_name = app_name
        self.on_show = on_show
        self.on_quit = on_quit
        self.on_toggle_autostart = on_toggle_autostart
        self.is_autostart_enabled = is_autostart_enabled

        self._tray = None
        self._running = False

    def _create_icon(self) -> Image.Image:
        """创建托盘图标"""
        # 创建一个 64x64 的图标
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 绘制圆角矩形背景
        margin = 4
        corner_radius = 12
        bg_color = (30, 30, 46, 255)  # 深色背景

        # 绘制圆角矩形
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=corner_radius,
            fill=bg_color
        )

        # 绘制 "AI" 文字
        text_color = (137, 180, 250, 255)  # 蓝色
        # 使用简单的方式绘制文字
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()

        # 居中绘制文字
        text = "AI"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 2
        draw.text((x, y), text, fill=text_color, font=font)

        return img

    def _create_menu(self):
        """创建托盘菜单"""
        items = [
            MenuItem(
                text="显示窗口",
                action=self._on_show_clicked,
                default=True
            ),
            Menu.SEPARATOR,
        ]

        # 开机自启动选项
        if self.on_toggle_autostart and self.is_autostart_enabled:
            items.append(
                MenuItem(
                    text="开机自启动",
                    action=self._on_toggle_autostart_clicked,
                    checked=lambda item: self.is_autostart_enabled()
                )
            )

        items.extend([
            Menu.SEPARATOR,
            MenuItem(
                text="退出",
                action=self._on_quit_clicked
            )
        ])

        return Menu(*items)

    def _on_show_clicked(self):
        """显示窗口"""
        if self.on_show:
            self.on_show()

    def _on_toggle_autostart_clicked(self):
        """切换开机自启动"""
        if self.on_toggle_autostart:
            self.on_toggle_autostart()

    def _on_quit_clicked(self):
        """退出程序"""
        if self.on_quit:
            self.on_quit()
        self.stop()

    def start(self):
        """启动托盘"""
        if pystray is None:
            print("[Tray] pystray 未安装，跳过托盘功能")
            return

        if self._running:
            return

        icon = self._create_icon()
        menu = self._create_menu()

        self._tray = pystray.Icon(
            self.app_name,
            icon,
            self.app_name,
            menu
        )

        self._running = True
        self._tray.run_detached()
        print(f"[Tray] {self.app_name} 已启动托盘")

    def stop(self):
        """停止托盘"""
        if self._tray:
            self._tray.stop()
            self._running = False
            print("[Tray] 托盘已停止")

    def update_icon(self, icon: Image.Image):
        """更新托盘图标"""
        if self._tray:
            self._tray.icon = icon

    def notify(self, title: str, message: str):
        """显示通知"""
        if self._tray:
            self._tray.notify(message, title)


def get_resource_path(relative_path: str) -> str:
    """获取资源文件路径（支持 PyInstaller 打包）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的路径
        base_path = sys._MEIPASS
    else:
        # 开发环境路径
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)