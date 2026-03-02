"""
AI Clip - 历史记录存储
"""

import json
import time
from typing import List, Dict, Optional
from pathlib import Path

from config import (
    MAX_HISTORY, HISTORY_FILE,
    PREVIEW_LENGTH, HISTORY_RETENTION_DAYS
)
from utils.helpers import format_timestamp, truncate_text


class Storage:
    """
    历史记录存储管理
    """

    def __init__(self):
        """初始化存储"""
        self.history: List[Dict] = []  # [{id, content, timestamp, preview}]
        self._load_from_file()

    def add(self, content: str) -> Optional[Dict]:
        """
        添加新的历史记录

        Args:
            content: 复制的内容

        Returns:
            添加的记录，如果内容为空或重复则返回None
        """
        if not content or not content.strip():
            return None

        content = content.strip()

        # 检查是否与最新记录重复
        if self.history and self.history[0].get("content") == content:
            return None

        # 创建新记录
        record = {
            "id": str(int(time.time() * 1000)),
            "content": content,
            "timestamp": time.time(),
            "preview": truncate_text(content, PREVIEW_LENGTH)
        }

        # 添加到列表开头
        self.history.insert(0, record)

        # 限制历史记录数量
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[:MAX_HISTORY]

        return record

    def get_latest(self, n: int = None) -> List[Dict]:
        """
        获取最新的n条记录

        Args:
            n: 记录数量，None表示全部

        Returns:
            记录列表
        """
        if n is None:
            return self.history
        return self.history[:n]

    def search(self, keyword: str) -> List[Dict]:
        """
        搜索历史记录

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的记录列表
        """
        if not keyword:
            return self.history

        keyword_lower = keyword.lower()
        return [
            record for record in self.history
            if keyword_lower in record["content"].lower()
        ]

    def get_by_id(self, record_id: str) -> Optional[Dict]:
        """
        根据ID获取记录

        Args:
            record_id: 记录ID

        Returns:
            记录或None
        """
        for record in self.history:
            if record["id"] == record_id:
                return record
        return None

    def clear(self):
        """清空所有历史记录"""
        self.history = []

    def clear_old(self, days: int = None):
        """
        清除指定天数之前的记录

        Args:
            days: 天数，None表示使用配置值
        """
        if days is None:
            days = HISTORY_RETENTION_DAYS

        cutoff_time = time.time() - (days * 24 * 60 * 60)
        self.history = [
            record for record in self.history
            if record["timestamp"] > cutoff_time
        ]

    def _load_from_file(self):
        """从文件加载历史记录"""
        if not HISTORY_FILE.exists():
            return

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.history = data.get("history", [])
                # 清除过期记录
                self.clear_old()
        except Exception as e:
            print(f"[Storage] 加载历史记录失败: {e}")
            self.history = []

    def save_to_file(self):
        """保存历史记录到文件"""
        try:
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "history": self.history,
                    "version": "1.0"
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Storage] 保存历史记录失败: {e}")

    def __len__(self):
        """返回历史记录数量"""
        return len(self.history)

    def __getitem__(self, index):
        """支持索引访问"""
        return self.history[index]
