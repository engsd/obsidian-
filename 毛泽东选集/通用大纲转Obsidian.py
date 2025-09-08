#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用Markdown大纲转Obsidian知识库工具

功能：将符合特定格式的Markdown大纲文件转换为Obsidian知识库结构
格式要求：
- ## 二级标题 → 顶级文件夹
- ### 三级标题 → 子文件夹  
- - 列表项 → 原子笔记文件
- - 钩子: → 会被忽略（用于钩子提取）

使用方法：
python 通用大纲转Obsidian.py [大纲文件.md] [输出目录]
"""

import os
import re
import sys

def create_obsidian_structure(markdown_file=None, base_path=None):
    """
    根据Markdown大纲文件创建Obsidian知识库结构
    
    参数:
        markdown_file: Markdown大纲文件路径
        base_path: 目标目录路径（默认为Markdown文件所在目录）
    """
    
    # 如果没有提供文件，使用当前目录下的第一个.md文件
    if markdown_file is None:
        current_dir = os.getcwd()
        md_files = [f for f in os.listdir(current_dir) if f.endswith('.md') and not f.startswith('通用大纲转Obsidian')]
        if not md_files:
            print("❌ 错误：当前目录下没有找到.md文件")
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
    
    # 读取Markdown大纲文件
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(markdown_file, 'r', encoding='gbk') as f:
            content = f.read()
    
    # 清理函数：移除文件名中的非法字符
    def clean_filename(name):
        # 移除Windows文件名中的非法字符和多余空格
        illegal_chars = r'[\\/:*?"<>|]'
        cleaned = re.sub(illegal_chars, '', name).strip()
        # 移除连续空格和首尾空格
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned
    
    # 解析大纲结构
    lines = content.strip().split('\n')
    current_top_folder = None
    current_sub_folder = None
    
    # 统计创建的项目
    created_folders = []
    created_files = []
    
    # 获取文件名用于通用模板
    base_filename = os.path.splitext(os.path.basename(markdown_file))[0]
    
    print(f"🚀 开始处理: {base_filename}")
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # 跳过空行和钩子
        if not line or line.startswith('- 钩子:'):
            continue
            
        if line.startswith('## '):
            # 创建顶级文件夹
            folder_name = clean_filename(line[3:].strip())
            folder_path = os.path.join(base_path, folder_name)
            
            try:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    created_folders.append(folder_name)
                    print(f"📁 创建文件夹: {folder_name}")
                
                current_top_folder = folder_path
                current_sub_folder = None  # 重置子文件夹
            except Exception as e:
                print(f"❌ 创建文件夹失败: {folder_name} - {e}")
            
        elif line.startswith('### ') and current_top_folder:
            # 创建子文件夹
            subfolder_name = clean_filename(line[4:].strip())
            subfolder_path = os.path.join(current_top_folder, subfolder_name)
            
            try:
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                    created_folders.append(f"{os.path.basename(current_top_folder)}\\{subfolder_name}")
                    print(f"📂 创建子文件夹: {subfolder_name}")
                
                current_sub_folder = subfolder_path
                
                # 创建子文件夹的MOC笔记
                moc_name = f"{subfolder_name} MOC.md"
                moc_path = os.path.join(subfolder_path, moc_name)
                
                if not os.path.exists(moc_path):
                    with open(moc_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {subfolder_name}\n\n")
                        f.write(f'这是"{base_filename}"中"{subfolder_name}"主题的MOC（Map of Content）笔记。\n\n')
                        f.write("## 相关原子笔记\n\n")
                        f.write("> 该目录下的原子笔记将自动添加到此列表\n\n")
                    created_files.append(moc_path)
                    print(f"📄 创建MOC: {moc_name}")
                    
            except Exception as e:
                print(f"❌ 创建子文件夹失败: {subfolder_name} - {e}")
            
        elif line.startswith('- ') and current_sub_folder:
            # 创建原子笔记
            note_title = line[2:].strip()
            if note_title.startswith('钩子:'):
                continue
                
            note_name = clean_filename(note_title) + '.md'
            note_path = os.path.join(current_sub_folder, note_name)
            
            try:
                if not os.path.exists(note_path):
                    with open(note_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {note_title}\n\n")
                        f.write(f"📚 来源：{base_filename}\n")
                        f.write(f"🏷️ 主题：{os.path.basename(current_sub_folder)}\n\n")
                        f.write("---\n\n")
                        f.write("## 📝 内容摘要\n\n")
                        f.write("<!-- 在此处添加内容摘要 -->\n\n")
                        f.write("## 🔍 关键要点\n\n")
                        f.write("- [ ] 要点1\n")
                        f.write("- [ ] 要点2\n")
                        f.write("- [ ] 要点3\n\n")
                        f.write("## 💭 思考与联系\n\n")
                        f.write("<!-- 在此处添加个人思考和与其他知识的联系 -->\n\n")
                        f.write("## 🔗 相关链接\n\n")
                        f.write("<!-- 在此处添加相关链接和参考文献 -->\n\n")
                    created_files.append(note_path)
                    print(f"📄 创建笔记: {note_name}")
                    
                    # 更新MOC笔记，添加原子笔记链接
                    moc_name = f"{os.path.basename(current_sub_folder)} MOC.md"
                    moc_path = os.path.join(current_sub_folder, moc_name)
                    
                    if os.path.exists(moc_path):
                        with open(moc_path, 'a', encoding='utf-8') as f:
                            f.write(f"- [[{note_title}]]\n")
                        
            except Exception as e:
                print(f"❌ 创建笔记失败: {note_name} - {e}")
    
    # 打印最终统计
    print(f"\n" + "="*50)
    print(f"📊 创建统计：")
    print(f"📁 文件夹: {len(created_folders)} 个")
    print(f"📄 文件: {len(created_files)} 个")
    print(f"📍 输出路径: {base_path}")
    print("="*50)
    print("✅ 知识库结构创建完成！")
    
    # 提供后续建议
    print(f"\n💡 后续建议：")
    print(f"1. 使用钩子提取脚本为笔记添加思考钩子")
    print(f"2. 在Obsidian中打开此目录开始使用")
    print(f"3. 根据需要自定义笔记模板")

def print_usage():
    """打印使用说明"""
    print("""
🔧 通用Markdown大纲转Obsidian工具

📋 使用方法：
1. 基本用法（自动检测当前目录的.md文件）：
   python 通用大纲转Obsidian.py

2. 指定Markdown文件：
   python 通用大纲转Obsidian.py 我的大纲.md

3. 指定文件和输出目录：
   python 通用大纲转Obsidian.py 我的大纲.md ./输出目录

4. 使用绝对路径：
   python 通用大纲转Obsidian.py "C:/文档/大纲.md" "D:/Obsidian/知识库"

📋 文件格式要求：
## 主题一           → 创建"主题一"文件夹
### 子主题1        → 创建"主题一/子主题1"子文件夹
- 文章标题1        → 创建"主题一/子主题1/文章标题1.md"
- 文章标题2        → 创建"主题一/子主题1/文章标题2.md"
### 子主题2        → 创建"主题一/子主题2"子文件夹
- 文章标题3        → 创建"主题一/子主题2/文章标题3.md"

## 主题二           → 创建"主题二"文件夹
### 子主题3        → 创建"主题二/子主题3"子文件夹
- 文章标题4        → 创建"主题二/子主题3/文章标题4.md"

特殊处理：
- 跳过空行
- 跳过以"- 钩子:"开头的行
- 自动处理文件名中的非法字符
- 为每个子文件夹创建MOC索引
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # 无参数，使用当前目录
        create_obsidian_structure()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
        else:
            # 指定Markdown文件
            create_obsidian_structure(sys.argv[1])
    elif len(sys.argv) == 3:
        # 指定文件和输出目录
        create_obsidian_structure(sys.argv[1], sys.argv[2])
    else:
        print_usage()