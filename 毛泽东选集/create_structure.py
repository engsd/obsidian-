import os
import re
import shutil

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
        md_files = [f for f in os.listdir(current_dir) if f.endswith('.md')]
        if not md_files:
            print("错误：当前目录下没有找到.md文件")
            return
        markdown_file = os.path.join(current_dir, md_files[0])
        print(f"使用文件: {os.path.basename(markdown_file)}")
    
    # 确保文件存在
    if not os.path.exists(markdown_file):
        print(f"错误：找不到文件 {markdown_file}")
        return
    
    # 设置基础路径
    if base_path is None:
        base_path = os.path.dirname(markdown_file)
    
    # 读取Markdown大纲文件
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(outline_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 清理函数：移除文件名中的非法字符
    def clean_filename(name):
        # 移除Windows文件名中的非法字符
        illegal_chars = r'[\\/:*?"<>|]'
        return re.sub(illegal_chars, '', name).strip()
    
    # 解析大纲并创建结构
    lines = content.strip().split('\n')
    current_top_folder = None
    current_sub_folder = None
    
    # 统计创建的项目
    created_folders = []
    created_files = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('## '):
            # 创建顶级文件夹
            folder_name = clean_filename(line[3:].strip())
            folder_path = os.path.join(base_path, folder_name)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                created_folders.append(folder_name)
            
            current_top_folder = folder_path
            
        elif line.startswith('### ') and current_top_folder:
            # 创建子文件夹
            subfolder_name = clean_filename(line[4:].strip())
            subfolder_path = os.path.join(current_top_folder, subfolder_name)
            
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
                created_folders.append(f"{os.path.basename(current_top_folder)}\{subfolder_name}")
            
            current_sub_folder = subfolder_path
            
            # 创建子文件夹的MOC笔记
            moc_name = f"{subfolder_name} MOC.md"
            moc_path = os.path.join(subfolder_path, moc_name)
            
            if not os.path.exists(moc_path):
                with open(moc_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {subfolder_name}\n\n")
                    f.write(f"这是《毛泽东选集》中"{subfolder_name}"主题的MOC（Map of Content）笔记。\n\n")
                    f.write("## 相关原子笔记\n\n")
                created_files.append(moc_path)
            
        elif line.startswith('- ') and not line.startswith('- 钩子:') and current_sub_folder:
            # 创建原子笔记
            note_name = clean_filename(line[2:].strip()) + '.md'
            note_path = os.path.join(current_sub_folder, note_name)
            
            if not os.path.exists(note_path):
                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {line[2:].strip()}\n\n")
                    f.write(f"来源：《毛泽东选集》\n")
                    f.write(f"主题：{os.path.basename(current_sub_folder)}\n\n")
                    f.write("## 内容\n\n")
                created_files.append(note_path)
                
                # 更新MOC笔记，添加原子笔记链接
                moc_name = f"{os.path.basename(current_sub_folder)} MOC.md"
                moc_path = os.path.join(current_sub_folder, moc_name)
                
                if os.path.exists(moc_path):
                    with open(moc_path, 'a', encoding='utf-8') as f:
                        f.write(f"[[{note_name[:-3]}]]\n")
    
    # 打印创建统计
    print(f"已创建 {len(created_folders)} 个文件夹：")
    for folder in created_folders:
        print(f"  - {folder}")
    
    print(f"\n已创建 {len(created_files)} 个文件：")
    for file in created_files:
        print(f"  - {os.path.basename(file)}")
    
    print("\n所有文件夹和笔记创建完成！")

if __name__ == "__main__":
    create_obsidian_structure()