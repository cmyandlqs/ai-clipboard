# AI Clip

> 在 AI 思考的时候，你的思考也不被中断。

一款专注于提升与 AI（Claude、ChatGPT 等）对话效率的轻量级剪贴板增强工具。

## 功能特点

- ⚡ **快速输入** - `Ctrl+Shift+Space` 毫秒级唤起输入框
- 📋 **剪贴板监控** - 自动记录复制历史（最多100条）
- 🔍 **即时搜索** - 快速过滤历史记录
- 💾 **数据持久化** - 重启后历史记录不丢失
- 🎨 **现代深色主题** - 简洁美观的界面设计
- 📍 **位置记忆** - 记住窗口位置

## 快速开始

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd AI_Clipboard

# 安装依赖
pip install -r requirements.txt
```

### 运行

```bash
python main.py
```

### 使用方法

1. **快速输入**
   - 按 `Ctrl+Shift+Space` 唤起输入框
   - 输入内容后按 `Enter` 复制到剪贴板
   - 按 `Esc` 关闭窗口

2. **查看历史**
   - 在主窗口点击 📋 按钮打开历史记录
   - 点击任意记录复制到剪贴板
   - 使用搜索框快速过滤

3. **退出程序**
   - 按 `Ctrl+C` 退出

## 项目结构

```
AI_Clipboard/
├── main.py                 # 程序入口
├── config.py               # 配置文件
├── core/
│   ├── clipboard.py        # 剪贴板监控
│   ├── hotkey.py           # 全局快捷键
│   ├── storage.py          # 历史记录存储
│   └── config_manager.py   # 配置管理器
├── ui/
│   ├── main_window.py      # 主输入窗口
│   └── history_window.py   # 历史记录弹窗
├── utils/
│   └── helpers.py          # 工具函数
└── requirements.txt        # 依赖列表
```

## 技术栈

- **Python 3.11+**
- **Tkinter** - GUI框架
- **pyperclip** - 剪贴板操作
- **keyboard** - 全局快捷键

## 配置文件

配置文件存储在 `%APPDATA%\AI Clip\`：

- `history.json` - 历史记录
- `config.json` - 窗口位置等配置

## 开发计划

- [x] Phase 1: 基础窗口 + 快捷键
- [x] Phase 2: 剪贴板监控
- [x] Phase 3: 历史记录弹窗
- [x] Phase 4: 搜索功能
- [x] Phase 5: 数据持久化
- [x] Phase 6: 窗口位置记忆
- [ ] 系统托盘支持
- [ ] 自定义快捷键
- [ ] 导出/导入历史

## 许可证

MIT License

---

**AI Clip** v0.1.0 - 让 AI 对话更高效
