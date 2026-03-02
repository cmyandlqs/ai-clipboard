"""
AI Clip - 剪贴板监控
"""

import time
import threading
import pyperclip
from typing import Callable, Optional

from config import CLIPBOARD_CHECK_INTERVAL
from core.storage import Storage


class ClipboardMonitor(threading.Thread):
    """
    剪贴板后台监控线程
    定期检查剪贴板内容变化并记录到Storage
    """

    def __init__(self, storage: Storage, on_change: Callable = None):
        """
        初始化剪贴板监控

        Args:
            storage: 存储管理器
            on_change: 内容变化回调函数
        """
        super().__init__(daemon=True)  # 设置为守护线程
        self.storage = storage
        self.on_change = on_change
        self._running = False
        self._last_content = ""

    def run(self):
        """监控线程主循环"""
        self._running = True

        # 初始化当前剪贴板内容
        try:
            self._last_content = pyperclip.paste()
        except:
            self._last_content = ""

        print("[Clipboard] 开始监控剪贴板...")

        while self._running:
            try:
                # 获取当前剪贴板内容
                current_content = pyperclip.paste()

                # 检测内容变化
                if current_content and current_content != self._last_content:
                    self._last_content = current_content

                    # 添加到存储
                    record = self.storage.add(current_content)
                    if record:
                        print(f"[Clipboard] 新记录: {record['preview']}")
                        # 触发回调
                        if self.on_change:
                            self.on_change(record)

                # 等待下次检查
                time.sleep(CLIPBOARD_CHECK_INTERVAL)

            except Exception as e:
                print(f"[Clipboard] 监控错误: {e}")
                time.sleep(CLIPBOARD_CHECK_INTERVAL)

        print("[Clipboard] 停止监控")

    def stop(self):
        """停止监控"""
        self._running = False

    def is_running(self) -> bool:
        """是否正在运行"""
        return self._running
