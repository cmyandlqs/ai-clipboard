"""
AI Clip - 主窗口测试用例
用于验证Enter键复制、Esc关闭等功能
"""

import tkinter as tk
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pyperclip
from ui.main_window import MainWindow


class TestMainWindow:
    """主窗口测试类"""

    def setup_method(self):
        """每个测试前设置"""
        # 创建隐藏的根窗口
        self.root = tk.Tk()
        self.root.withdraw()
        # 创建主窗口
        self.window = MainWindow()

    def teardown_method(self):
        """每个测试后清理"""
        try:
            self.window.destroy()
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass

    def test_window_initially_hidden(self):
        """测试窗口初始状态为隐藏"""
        assert not self.window.visible, "窗口初始应该是隐藏状态"

    def test_show_window(self):
        """测试显示窗口"""
        self.window.show()
        assert self.window.visible, "显示后visible应该为True"

    def test_hide_window(self):
        """测试隐藏窗口"""
        self.window.show()
        self.window.hide()
        assert not self.window.visible, "隐藏后visible应该为False"

    def test_toggle_window(self):
        """测试切换窗口显示状态"""
        # 初始隐藏
        assert not self.window.visible
        # 切换到显示
        self.window.toggle()
        assert self.window.visible
        # 切换到隐藏
        self.window.toggle()
        assert not self.window.visible

    def test_enter_with_text_copies_to_clipboard(self):
        """测试Enter键复制文本到剪贴板"""
        test_text = "测试内容"
        self.window.set_input_text(test_text)

        # 模拟Enter键事件
        self.window.event_generate("<Return>")
        self.window.update()

        # 检查剪贴板
        clipboard_content = pyperclip.paste()
        assert clipboard_content == test_text, f"剪贴板应包含'{test_text}'"
        assert not self.window.visible, "按Enter后窗口应关闭"

    def test_enter_with_empty_text(self):
        """测试空内容按Enter不复制"""
        self.window.clear_input()

        # 模拟Enter键事件
        self.window.event_generate("<Return>")
        self.window.update()

        # 窗口应关闭
        assert not self.window.visible, "按Enter后窗口应关闭"

    def test_escape_closes_window(self):
        """测试Esc键关闭窗口"""
        self.window.show()

        # 模拟Esc键事件
        self.window.event_generate("<Escape>")
        self.window.update()

        assert not self.window.visible, "按Esc后窗口应关闭"

    def test_get_input_text(self):
        """测试获取输入框文本"""
        test_text = "测试输入"
        self.window.set_input_text(test_text)
        result = self.window.get_input_text()
        assert result == test_text, "应返回输入的文本"

    def test_clear_input(self):
        """测试清空输入框"""
        self.window.set_input_text("有内容")
        self.window.clear_input()
        result = self.window.get_input_text()
        assert result == "", "清空后应为空"

    def test_history_button_callback(self):
        """测试历史按钮回调"""
        callback_called = [False]

        def mock_callback():
            callback_called[0] = True

        self.window.on_history_click = mock_callback
        self.window._on_history_click()

        assert callback_called[0], "历史按钮应触发回调"


def run_manual_tests():
    """
    手动测试函数

    运行此函数进行手动交互测试：
    python -m tests.test_main_window
    """
    print("=" * 50)
    print("AI Clip - 手动测试模式")
    print("=" * 50)

    window = MainWindow()
    window.show()

    print("\n测试步骤:")
    print("1. 输入一些文字")
    print("2. 按Enter键 - 应该复制到剪贴板并关闭窗口")
    print("3. 按Ctrl+Shift+Space重新打开")
    print("4. 按Esc键 - 应该关闭窗口")
    print("5. 点击📋按钮 - 应该打开历史窗口")
    print("6. 关闭窗口退出测试")

    window.mainloop()


if __name__ == "__main__":
    # 手动测试模式
    run_manual_tests()
