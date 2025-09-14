#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全自动知识库构建器 - 最终修正版 V3

功能：一键完成从Markdown大纲到完整Obsidian知识库的构建
修正：
- 修正了因BOM字符导致第一个H2标题被忽略的Bug
- 增强了文件读取的稳定性和错误提示
- 优化了状态变量重置逻辑，确保模块解析正确
- 优化了部分链接和输出格式
"""

import os
import re
import sys

def build_complete_knowledge_base(markdown_file=None, base_path=None):
    """
    全自动构建完整知识库（最终修正版 V3）
    """
    
    # 如果没有提供文件，自动检测当前目录
    if markdown_file is None:
        current_dir = os.getcwd()
        md_files = [f for f in os.listdir(current_dir)
                   if f.endswith('.md')
                   and not f.startswith(('通用', '全自动', 'create', '总览'))]
        if not md_files:
            print("❌ 错误：当前目录下没有找到合适的.md文件")
            return
        markdown_file = os.path.join(current_dir, md_files[0])
        print(f"📂 自动检测文件: {os.path.basename(markdown_file)}")

    # 确保文件存在
    if not os.path.exists(markdown_file):
        print(f"❌ 错误：找不到文件 {markdown_file}")
        return

    # 设置基础路径
    if base_path is None:
        base_path = os.path.dirname(markdown_file)

    # 获取基础文件名
    base_filename = os.path.splitext(os.path.basename(markdown_file))[0]

    print(f"🚀 开始构建知识库: {base_filename}")
    print(f"📂 输出路径: {base_path}")

    # --- 核心修正：使用 'utf-8-sig' 编码来自动处理BOM ---
    try:
        with open(markdown_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 错误: 无法读取文件 {markdown_file}。详情: {e}")
        return

    # 清理函数
    def clean_filename(name):
        illegal_chars = r'[\\/*?"<>|]'
        cleaned = re.sub(illegal_chars, '', name).strip()
        return re.sub(r'\s+', ' ', cleaned)

    # 解析结构并收集钩子
    lines = content.strip().split('\n')
    structure = {}
    current_h2 = None
    current_h3 = None
    hooks_map = {}
    italic_content_map = {}

    stats = {
        'folders': 0, 'subfolders': 0, 'atomic_notes': 0,
        'hooks': 0, 'moc_notes': 0
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('## '):
            current_h2 = clean_filename(line[3:].strip())
            # 修正：当遇到新的H2时，必须重置H3的状态
            current_h3 = None 
            if current_h2 not in structure:
                structure[current_h2] = {}
                italic_content_map[current_h2] = []
                stats['folders'] += 1

        elif line.startswith('### ') and current_h2:
            current_h3 = clean_filename(line[4:].strip())
            if current_h3 not in structure[current_h2]:
                structure[current_h2][current_h3] = []
                stats['subfolders'] += 1

        # 修正：将斜体内容解析移到H3判断之后，并修正逻辑
        elif current_h2 and not current_h3 and line.startswith('*') and line.endswith('*'):
            italic_content = line[1:-1].strip()
            if italic_content:
                italic_content_map[current_h2].append(italic_content)

        elif line.startswith('- ') and current_h2 and current_h3:
            item = line[2:].strip()
            if item.startswith('钩子:'):
                hook_content = item[3:].strip()
                if structure[current_h2][current_h3]:
                    last_note = structure[current_h2][current_h3][-1]
                    if last_note not in hooks_map:
                        hooks_map[last_note] = []
                    hooks_map[last_note].append(hook_content)
                    stats['hooks'] += 1
            else:
                structure[current_h2][current_h3].append(item)
                stats['atomic_notes'] += 1
    
    moc_links = {}

    for h2_folder, subfolders in structure.items():
        h2_path = os.path.join(base_path, h2_folder)
        os.makedirs(h2_path, exist_ok=True)

        for h3_subfolder, notes in subfolders.items():
            h3_path = os.path.join(h2_path, h3_subfolder)
            os.makedirs(h3_path, exist_ok=True)

            moc_name = f"{h3_subfolder} MOC.md"
            moc_path = os.path.join(h3_path, moc_name)

            with open(moc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {h3_subfolder}\n\n")
                f.write(f"主题：[[{base_filename}学习总览]] > [[{h2_folder}]]\n\n")

                if h2_folder in italic_content_map and italic_content_map[h2_folder]:
                    f.write("## 核心概念\n\n")
                    for italic in italic_content_map[h2_folder]:
                        f.write(f"- {italic}\n")
                    f.write("\n")

                f.write("## 相关文章\n\n")
                for note in notes:
                    f.write(f"- [[{note}]]\n")

                f.write("\n## 链接\n\n")
                f.write(f"- [[{base_filename}学习总览]]\n")

            stats['moc_notes'] += 1

            if h2_folder not in moc_links:
                moc_links[h2_folder] = []
            moc_links[h2_folder].append(f"{h3_subfolder} MOC")

            for note in notes:
                note_name = clean_filename(note) + '.md'
                note_path = os.path.join(h3_path, note_name)

                with open(note_path, 'w', encoding='utf-8') as f:
                    if note in hooks_map and hooks_map[note]:
                        for hook in hooks_map[note]:
                            f.write(f"#### {hook}\n\n")
                            f.write("\n")

                    f.write("## 摘要\n\n\n")
                    f.write("## 要点\n\n- \n- \n- \n\n")
                    f.write("## 链接\n\n- [[{h3_subfolder} MOC]]\n")

    overview_path = os.path.join(base_path, f"{base_filename}学习总览.md")

    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(f"# {base_filename}学习总览\n\n")
        f.write(f"系统性学习 **{base_filename}** 的知识中心\n\n")

        f.write("## 统计\n\n")
        f.write(f"- **顶级模块**: {stats['folders']}个\n")
        f.write(f"- **子主题**: {stats['subfolders']}个\n")
        f.write(f"- **原子笔记**: {stats['atomic_notes']}篇\n")
        f.write(f"- **知识钩子**: {stats['hooks']}个\n\n")

        f.write("## 模块导航\n\n")

        for h2_folder, mocs in sorted(moc_links.items()):
            f.write(f"### [[{h2_folder}]]\n\n")
            for moc in sorted(mocs):
                f.write(f"- [[{moc}]]\n")
            f.write("\n")

        f.write("---\n\n> 💡 **链接结构说明**：原子笔记 → MOC笔记 → 学习总览\n")

    print("\n" + "="*50)
    print("✅ 知识库构建完成!")
    print(f"  - 顶级文件夹: {stats['folders']}个")
    print(f"  - 子文件夹: {stats['subfolders']}个")
    print(f"  - 原子笔记: {stats['atomic_notes']}篇")
    print(f"  - 知识钩子: {stats['hooks']}个")
    print(f"  - 输出目录: {base_path}")
    print("="*50)
    
    print(f"\n下一步操作：")
    print(f"1. 在Obsidian中打开: {base_path}")
    print(f"2. 打开总览笔记: **{base_filename}学习总览.md**")
    print(f"3. 开始你的学习之旅！🚀")

def print_usage():
    """打印使用说明"""
    print("""
🔧 全自动知识库构建器 - V3

📋 一键完成所有操作：
1️⃣ 解析Markdown大纲
2️⃣ 创建文件夹结构
3️⃣ 提取钩子内容
4️⃣ 建立单向链接（原子→MOC→总览）
5️⃣ 生成总览导航

📋 使用方法：
1. 基本用法（自动检测）：
   python 全自动知识库构建器_修正版.py

2. 指定大纲文件：
   python 全自动知识库构建器_修正版.py 我的大纲.md

3. 指定文件和输出目录：
   python 全自动知识库构建器_修正版.py 我的大纲.md ./输出目录

📋 大纲格式要求：
## 主题一           → 创建顶级文件夹
*核心概念1*        → 斜体内容将写入MOC笔记的核心概念部分
*核心概念2*        → 可以添加多个核心概念
### 子主题1        → 创建子文件夹
- 文章标题1        → 创建原子笔记
- 钩子: 问题1      → 添加思考钩子到文章1
- 钩子: 问题2      → 添加更多钩子
- 文章标题2        → 创建另一个原子笔记
- 钩子: 问题3      → 添加钩子到文章2

🎯 输出结果：
- 完整的Obsidian知识库结构
- 所有钩子已写入对应笔记
- 二级标题下的斜体内容已写入对应MOC笔记的核心概念部分
- 单向链接网络
- 立即可用！
""")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        build_complete_knowledge_base()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
        else:
            build_complete_knowledge_base(sys.argv[1])
    elif len(sys.argv) == 3:
        build_complete_knowledge_base(sys.argv[1], sys.argv[2])
    else:
        print_usage()