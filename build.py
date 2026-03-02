"""
AI Clip - PyInstaller 打包脚本
"""

import PyInstaller.__main__
import os
import sys

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 打包参数
PyInstaller.__main__.run([
    os.path.join(ROOT_DIR, "main.py"),
    
    # 输出目录
    f"--distpath={os.path.join(ROOT_DIR, 'dist')}",
    f"--workpath={os.path.join(ROOT_DIR, 'build')}",
    f"--specpath={ROOT_DIR}",
    
    # 单文件模式
    "--onefile",
    
    # 窗口模式（无控制台）
    "--windowed",
    
    # 应用名称
    "--name=AI Clip",
    
    # 图标（如果有的话）
    # f"--icon={os.path.join(ROOT_DIR, 'assets', 'icon.ico')}",
    
    # 隐藏导入
    "--hidden-import=PIL",
    "--hidden-import=PIL.Image",
    "--hidden-import=PIL.ImageDraw",
    "--hidden-import=pystray",
    "--hidden-import=pystray._win32",
    "--hidden-import=keyboard",
    "--hidden-import=pyperclip",
    
    # 数据文件（如果有）
    # f"--add-data={os.path.join(ROOT_DIR, 'assets')};assets",
    
    # 排除不需要的模块
    "--exclude-module=matplotlib",
    "--exclude-module=numpy",
    "--exclude-module=scipy",
    "--exclude-module=pandas",
    
    # 清理临时文件
    "--clean",
    
    # 不显示日志
    "--noconfirm",
])

print("\n" + "=" * 50)
print("打包完成！")
print(f"输出文件: {os.path.join(ROOT_DIR, 'dist', 'AI Clip.exe')}")
print("=" * 50)