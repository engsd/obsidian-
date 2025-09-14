#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全自动知识库构建器 - 修正版

功能：一键完成从Markdown大纲到完整Obsidian知识库的构建
包括：
1. 解析Markdown大纲结构
2. 创建文件夹和原子笔记
3. 提取钩子内容并写入对应笔记
4. 建立链接网络：
   - 原子笔记 → MOC笔记
   - MOC笔记 → 学习总览
   - 原子笔记 → 学习总览（无链接）

使用方法：
python 全自动知识库构建器_修正版.py [大纲文件.md] [输出目录]
"""

import os
import re
import sys
from datetime import datetime

def build_complete_knowledge_base(markdown_file=None, base_path=None):
    """
    全自动构建完整知识库（修正版）
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
    
    print(f"开始构建知识库: {base_filename}")
    print(f"输出路径: {base_path}")
    
    # 读取Markdown文件
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(markdown_file, 'r', encoding='gbk') as f:
            content = f.read()
    
    # 清理函数
    def clean_filename(name):
        illegal_chars = r'[\/*?"<>|]'
        cleaned = re.sub(illegal_chars, '', name).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned
    
    # 解析结构并收集钩子
    lines = content.strip().split('\n')
    structure = {}
    current_h2 = None
    current_h3 = None
    hooks_map = {}  # 存储每个笔记的钩子
    italic_content_map = {}  # 存储每个二级标题下的斜体内容
    
    # 统计信息
    stats = {
        'folders': 0,
        'subfolders': 0,
        'atomic_notes': 0,
        'hooks': 0,
        'moc_notes': 0
    }
    
    # 解析大纲结构
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('## '):
            # H2 - 顶级文件夹
            current_h2 = clean_filename(line[3:].strip())
            structure[current_h2] = {}
            italic_content_map[current_h2] = []  # 初始化斜体内容列表
            stats['folders'] += 1
            
        elif line.startswith('### ') and current_h2:
            # H3 - 子文件夹
            current_h3 = clean_filename(line[4:].strip())
            structure[current_h2][current_h3] = []
            stats['subfolders'] += 1
            
        elif line.startswith('- ') and current_h2 and current_h3:
            # 原子笔记或钩子
            item = line[2:].strip()
            
            if item.startswith('钩子:'):
                # 这是钩子内容
                hook_content = item[3:].strip()
                
                # 找到最近的原子笔记标题
                if structure[current_h2][current_h3]:
                    last_note = structure[current_h2][current_h3][-1]
                    if last_note not in hooks_map:
                        hooks_map[last_note] = []
                    hooks_map[last_note].append(hook_content)
                    stats['hooks'] += 1
            else:
                # 这是原子笔记标题
                structure[current_h2][current_h3].append(item)
                stats['atomic_notes'] += 1
        elif current_h2 and not current_h3 and ('*' in line):
            # 提取二级标题下的斜体内容
            italic_pattern = r'\*([^*]+)\*'
            italic_matches = re.findall(italic_pattern, line)
            for match in italic_matches:
                italic_content_map[current_h2].append(match.strip())
    
    # 创建文件夹和文件 - 使用base_path作为根目录
    moc_links = {}  # 存储MOC笔记路径用于总览
    
    for h2_folder, subfolders in structure.items():
        h2_path = os.path.join(base_path, h2_folder)
        os.makedirs(h2_path, exist_ok=True)
        
        for h3_subfolder, notes in subfolders.items():
            h3_path = os.path.join(h2_path, h3_subfolder)
            os.makedirs(h3_path, exist_ok=True)
            
            # 创建MOC笔记
            moc_name = f"{h3_subfolder} MOC.md"
            moc_path = os.path.join(h3_path, moc_name)
            
            with open(moc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {h3_subfolder}\n\n")
                f.write(f"主题：{h2_folder} > {h3_subfolder}\n\n")
                
                # 添加二级标题下的斜体内容
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
            
            # 创建原子笔记
            for note in notes:
                note_name = clean_filename(note) + '.md'
                note_path = os.path.join(h3_path, note_name)
                
                with open(note_path, 'w', encoding='utf-8') as f:
                    #f.write(f"# {note}\n\n")
                    
                    # 写入钩子内容
                    if note in hooks_map and hooks_map[note]:
                        for hook in hooks_map[note]:
                            f.write(f"#### {hook}\n\n")
                            f.write("\n")
                        
                    f.write("## 摘要\n\n")
                    f.write("\n")
                    f.write("## 要点\n\n")
                    f.write("- \n")
                    f.write("- \n")
                    f.write("- \n")
                    f.write("\n## 链接\n\n")
                    f.write(f"- [[{h3_subfolder} MOC]]\n")
                    # 原子笔记中不包含到学习总览的链接
    
    # 创建总览笔记
    overview_path = os.path.join(base_path, f"{base_filename}学习总览.md")
    
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(f"# {base_filename}学习总览\n\n")
        f.write(f"系统性学习{base_filename}的知识中心\n\n")
        
        f.write("## 统计\n\n")
        f.write(f"- 顶级模块: {stats['folders']}个\n")
        f.write(f"- 子主题: {stats['subfolders']}个\n")
        f.write(f"- 原子笔记: {stats['atomic_notes']}篇\n")
        f.write(f"- 钩子: {stats['hooks']}个\n\n")
        
        f.write("## 模块导航\n\n")
        
        for h2_folder, mocs in sorted(moc_links.items()):
            f.write(f"### {h2_folder}\n\n")
            for moc in sorted(mocs):
                f.write(f"- [[{moc}]]\n")
            f.write("\n")
        
        # 更新说明
        f.write("---\n\n")
        f.write("> 💡 **链接结构说明**：\n")
        f.write("> - 原子笔记 → MOC笔记（单向链接）\n")
        f.write("> - MOC笔记 → 学习总览（单向链接）\n")
        f.write("> - 原子笔记 → 学习总览（无链接）\n")
    
    # 打印最终统计
    print(f"\n" + "="*50)
    print(f"知识库构建完成")
    print(f"顶级文件夹: {stats['folders']}个")
    print(f"子文件夹: {stats['subfolders']}个")
    print(f"原子笔记: {stats['atomic_notes']}篇")
    print(f"知识钩子: {stats['hooks']}个")
    print(f"输出目录: {base_path}")
    print("="*50)
    
    print(f"\n下一步操作：")
    print(f"1. 在Obsidian中打开: {base_path}")
    print(f"2. 打开总览笔记: {base_filename}学习总览.md")
    print(f"3. 开始你的学习之旅！")

def print_usage():
    """打印使用说明"""
    print("""
🔧 全自动知识库构建器 - 原子笔记不链接总览版

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
- 单向链接网络：
  - 原子笔记 → MOC笔记
  - MOC笔记 → 学习总览
  - 原子笔记 → 学习总览（无链接）
- 立即可用！

🔗 链接结构：
- 原子笔记 → MOC笔记（单向）
- MOC笔记 → 学习总览（单向）
- 原子笔记 → 学习总览（无链接）
""")

if __name__ == "__main__":
    import sys
    
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