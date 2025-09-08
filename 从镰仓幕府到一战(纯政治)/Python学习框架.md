# Python学习框架：构建知识库工具

## 学习目标

通过复刻"全自动知识库构建器"，你将学习以下Python核心概念：
- 方法和属性的使用
- if嵌套逻辑
- 循环结构
- 函数定义和调用
- 字典和列表操作
- 文件操作
- 正则表达式
- 模块导入

## 学习步骤框架

### 第一步：项目初始化

**目标**：创建基本的Python脚本结构，学习模块导入和基本函数定义。

**任务提示**：
1. 创建一个新的Python文件，命名为`my_knowledge_builder.py`

2. 导入必要的模块：`os`, `re`, `sys`, `datetime`
import os
import re
import sys
from datetime import datetime
3. 定义一个主函数`build_knowledge_base()`，暂时只包含一个打印语句
def build_knowledge_base():
    print("知识库构建器启动中)

4. 添加`if __name__ == "__main__":`结构，调用主函数
if __name__ == "__main__":
    build_knowledge_base()

**知识点**：
- 模块导入方法：`import module_name` 和 `from module import name`
- 函数定义：`def function_name(parameters):`
- 主程序入口：`if __name__ == "__main__":`

**预期代码结构**：
```python
# 导入必要的模块
import os
import re
import sys
from datetime import datetime

# 定义主函数
def build_knowledge_base():
    print("知识库构建器启动中...")

# 主程序入口
if __name__ == "__main__":
    build_knowledge_base()
```

### 第二步：添加文件处理功能

**目标**：学习文件操作和异常处理，实现读取Markdown文件的功能。

**任务提示**：
1. 修改`build_knowledge_base()`函数，添加一个参数`markdown_file`
def build_knowledge_base(markdown_file=None):
    if not os.path.exists(markdown_file):
        print(f"错误，找不到文件{markdown}")
    return

2. 使用`with open()`语句读取文件内容
    with open(markdown_file, ‘r’, encoding='utf-8') as f: content = f.read()
3. 添加异常处理，处理文件不存在和编码问题
    try:
        with open(markdown_file, 'r', encoding= 'utf-8') as f:
            content = f.read()
        except with open (markdown_file, 'r', encodign= 'gbk') as f:
            context = f.read()

        
4. 将文件内容分割成行列表
    lines= context.split('\n')
    print("成功读取到文件，一共{lend(lends)}行")

**知识点**：
- 文件操作：`with open(file_path, 'r', encoding='utf-8') as f:`
- 异常处理：`try-except`结构
- 字符串方法：`content.split('\n')`分割行
- 条件判断：`if not os.path.exists(file_path):`

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None):
    # 检查文件是否存在
    if not os.path.exists(markdown_file):
        print(f"错误：找不到文件 {markdown_file}")
        return
    
    # 尝试读取文件
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 如果utf-8失败，尝试gbk编码
        with open(markdown_file, 'r', encoding='gbk') as f:
            content = f.read()
    
    # 将内容分割成行
    lines = content.split('\n')
    print(f"成功读取文件，共{len(lines)}行")
```

### 第三步：解析Markdown结构

**目标**：学习if嵌套和字符串方法，解析Markdown文件中的标题结构。

**任务提示**：
1. 创建变量跟踪当前标题层级：`current_h2`和`current_h3`
2. 创建嵌套字典存储结构：`structure = {}`
3. 遍历每一行，使用`startswith()`方法检查标题级别
4. 使用if嵌套处理不同级别的标题
5. 使用`strip()`方法清理标题文本

current_h2=None
current_h3=None
structure = {}
    for line in lines:
        line = line.strip()
        if not line
            continue

        if line.startswith('## ')
            current_h2 =line[3:].strip
            structure[current_h2] = {}
            current_h3 = None
        
        elif line.startswith('### ') and current_h2:
            current_h3 = line[4:].strip
            structure[current_h3][current_h2] = []

        elif line.startswith('- ') and current_h2 current_h3:
            item = line[2:].strip
            structure[current_h3][current_h2].append(item)

        print("解析成功，结构如下)
        print(structure)

            

**知识点**：
- 字符串方法：`line.startswith('## ')`检查前缀
- 字符串切片：`line[3:]`获取子字符串
- 字符串清理：`line.strip()`去除两端空白
- if嵌套：多层条件判断
- 字典操作：`structure[key] = value`添加键值对

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None):
    # [前面的代码保持不变]
    
    # 初始化变量
    structure = {}
    current_h2 = None
    current_h3 = None
    
    # 遍历每一行
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 处理二级标题
        if line.startswith('## '):
            current_h2 = line[3:].strip()
            structure[current_h2] = {}
            current_h3 = None  # 重置三级标题
            
        # 处理三级标题（需要先有二级标题）
        elif line.startswith('### ') and current_h2:
            current_h3 = line[4:].strip()
            structure[current_h2][current_h3] = []
            
        # 处理列表项（需要先有二级和三级标题）
        elif line.startswith('- ') and current_h2 and current_h3:
            item = line[2:].strip()
            structure[current_h2][current_h3].append(item)
    
    print("解析完成，结构如下：")
    print(structure)
```

### 第四步：创建文件夹结构

**目标**：学习os模块方法和路径操作，根据解析结果创建文件夹结构。

**任务提示**：
1. 添加一个参数`base_path`指定输出目录
2. 使用`os.path.join()`方法构建路径
3. 使用`os.makedirs()`创建目录，设置`exist_ok=True`
4. 遍历解析结果，为每个二级和三级标题创建文件夹

**知识点**：
- 路径操作：`os.path.join(path1, path2)`连接路径
- 目录创建：`os.makedirs(path, exist_ok=True)`
- 嵌套循环：遍历嵌套字典结构
- 字典方法：`dict.items()`获取键值对

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None, base_path=None):
    # [前面的代码保持不变]
    
    # 如果没有指定输出目录，使用当前目录
    if not base_path:
        base_path = os.path.dirname(os.path.abspath(markdown_file))
    
    # 创建文件夹结构
    for h2_folder, subfolders in structure.items():
        # 创建二级标题文件夹
        h2_path = os.path.join(base_path, h2_folder)
        os.makedirs(h2_path, exist_ok=True)
        
        # 创建三级标题子文件夹
        for h3_subfolder, notes in subfolders.items():
            h3_path = os.path.join(h2_path, h3_subfolder)
            os.makedirs(h3_path, exist_ok=True)
    
    print("文件夹结构创建完成")
```

### 第五步：创建原子笔记

**目标**：学习文件写入和字符串格式化，为每个笔记创建Markdown文件。

**任务提示**：
1. 为每个笔记创建文件名（清理特殊字符）
2. 使用`with open()`写入文件
3. 使用f-string格式化字符串
4. 添加基本的笔记结构

**知识点**：
- 文件写入：`with open(path, 'w', encoding='utf-8') as f:`
- 字符串格式化：f"字符串{变量}"
- 文件名清理：创建一个函数清理文件名中的特殊字符
- 循环嵌套：遍历所有笔记

**预期代码结构**：
```python
def clean_filename(filename):
    """清理文件名中的特殊字符"""
    # 移除不允许在文件名中使用的字符
    invalid_chars = '<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()

def build_knowledge_base(markdown_file=None, base_path=None):
    # [前面的代码保持不变]
    
    # 创建原子笔记
    for h2_folder, subfolders in structure.items():
        for h3_subfolder, notes in subfolders.items():
            h3_path = os.path.join(base_path, h2_folder, h3_subfolder)
            
            # 为每个笔记创建文件
            for note in notes:
                # 清理文件名
                note_name = clean_filename(note) + '.md'
                note_path = os.path.join(h3_path, note_name)
                
                # 写入笔记内容
                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {note}\n\n")
                    f.write(f"主题：{h2_folder} > {h3_subfolder}\n\n")
                    f.write("## 内容\n\n")
                    f.write("在这里添加笔记内容...\n\n")
                    f.write("## 钩子\n\n")
                    f.write("- 思考点1\n")
                    f.write("- 思考点2\n")
    
    print("原子笔记创建完成")
```

### 第六步：提取钩子内容

**目标**：学习条件判断和列表操作，提取并处理钩子内容。

**任务提示**：
1. 修改解析逻辑，识别以"钩子:"开头的列表项
2. 创建`hooks_map`字典存储钩子内容
3. 将钩子内容添加到对应的笔记中

**知识点**：
- 条件判断：`if item.startswith('钩子:'):`
- 列表操作：`list.append()`添加元素
- 字典操作：检查键是否存在，添加键值对
- 字符串切片：提取钩子内容

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None, base_path=None):
    # [前面的代码保持不变，但需要修改解析部分]
    
    # 初始化变量
    structure = {}
    hooks_map = {}  # 添加钩子映射
    current_h2 = None
    current_h3 = None
    
    # 遍历每一行
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 处理二级标题
        if line.startswith('## '):
            current_h2 = line[3:].strip()
            structure[current_h2] = {}
            current_h3 = None  # 重置三级标题
            
        # 处理三级标题（需要先有二级标题）
        elif line.startswith('### ') and current_h2:
            current_h3 = line[4:].strip()
            structure[current_h2][current_h3] = []
            
        # 处理列表项（需要先有二级和三级标题）
        elif line.startswith('- ') and current_h2 and current_h3:
            item = line[2:].strip()
            
            # 检查是否是钩子
            if item.startswith('钩子:'):
                # 提取钩子内容
                hook_content = item[3:].strip()
                
                # 获取最后一个笔记
                if structure[current_h2][current_h3]:
                    last_note = structure[current_h2][current_h3][-1]
                    
                    # 初始化钩子列表（如果不存在）
                    if last_note not in hooks_map:
                        hooks_map[last_note] = []
                    
                    # 添加钩子
                    hooks_map[last_note].append(hook_content)
            else:
                # 添加普通笔记
                structure[current_h2][current_h3].append(item)
    
    # [后面的代码保持不变，但需要修改创建笔记的部分]
    
    # 创建原子笔记（修改版）
    for h2_folder, subfolders in structure.items():
        for h3_subfolder, notes in subfolders.items():
            h3_path = os.path.join(base_path, h2_folder, h3_subfolder)
            
            # 为每个笔记创建文件
            for note in notes:
                # 清理文件名
                note_name = clean_filename(note) + '.md'
                note_path = os.path.join(h3_path, note_name)
                
                # 写入笔记内容
                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {note}\n\n")
                    f.write(f"主题：{h2_folder} > {h3_subfolder}\n\n")
                    f.write("## 内容\n\n")
                    f.write("在这里添加笔记内容...\n\n")
                    f.write("## 钩子\n\n")
                    
                    # 添加钩子内容（如果有）
                    if note in hooks_map:
                        for hook in hooks_map[note]:
                            f.write(f"- {hook}\n")
                    else:
                        f.write("- 暂无钩子\n")
    
    print("原子笔记和钩子创建完成")
```

### 第七步：创建MOC笔记

**目标**：学习文件操作和列表推导式，为每个子主题创建MOC（Map of Content）笔记。

**任务提示**：
1. 为每个三级标题创建MOC笔记
2. 使用列表推导式获取笔记列表
3. 在MOC笔记中添加到所有原子笔记的链接
4. 添加统计信息

**知识点**：
- 列表推导式：`[表达式 for 变量 in 可迭代对象 if 条件]`
- 文件操作：写入MOC笔记文件
- 字符串格式化：创建链接格式
- 统计信息：计算文件夹、子文件夹和笔记数量

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None, base_path=None):
    # [前面的代码保持不变]
    
    # 创建MOC笔记
    for h2_folder, subfolders in structure.items():
        for h3_subfolder, notes in subfolders.items():
            # 创建MOC文件路径
            moc_name = f"{h3_subfolder} MOC.md"
            moc_path = os.path.join(base_path, h2_folder, h3_subfolder, moc_name)
            
            # 写入MOC内容
            with open(moc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {h3_subfolder}\n\n")
                f.write(f"主题：{h2_folder} > {h3_subfolder}\n\n")
                f.write("## 笔记列表\n\n")
                
                # 添加笔记链接
                for note in notes:
                    note_link = clean_filename(note) + '.md'
                    f.write(f"- [[{note_link}]]\n")
                
                f.write("\n## 钩子汇总\n\n")
                
                # 添加钩子汇总
                for note in notes:
                    if note in hooks_map:
                        f.write(f"### {note}\n\n")
                        for hook in hooks_map[note]:
                            f.write(f"- {hook}\n")
                        f.write("\n")
    
    print("MOC笔记创建完成")
```

### 第八步：提取斜体内容

**目标**：学习正则表达式，提取二级标题下的斜体内容。

**任务提示**：
1. 创建`italic_content_map`字典存储斜体内容
2. 使用正则表达式`r'\*([^*]+)\*'`匹配斜体内容
3. 将斜体内容添加到MOC笔记中

**知识点**：
- 正则表达式：`re.findall(pattern, string)`查找所有匹配
- 正则表达式模式：`r'\*([^*]+)\*'`匹配两个星号之间的内容
- 字典操作：存储和访问斜体内容
- 条件判断：检查是否有斜体内容

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None, base_path=None):
    # [前面的代码保持不变，但需要修改解析部分]
    
    # 初始化变量
    structure = {}
    hooks_map = {}
    italic_content_map = {}  # 添加斜体内容映射
    current_h2 = None
    current_h3 = None
    
    # 遍历每一行
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 处理二级标题
        if line.startswith('## '):
            current_h2 = line[3:].strip()
            structure[current_h2] = {}
            italic_content_map[current_h2] = []  # 初始化斜体内容列表
            current_h3 = None  # 重置三级标题
            
        # 处理三级标题（需要先有二级标题）
        elif line.startswith('### ') and current_h2:
            current_h3 = line[4:].strip()
            structure[current_h2][current_h3] = []
            
        # 处理列表项（需要先有二级和三级标题）
        elif line.startswith('- ') and current_h2 and current_h3:
            item = line[2:].strip()
            
            # 检查是否是钩子
            if item.startswith('钩子:'):
                # [钩子处理代码保持不变]
            else:
                # 添加普通笔记
                structure[current_h2][current_h3].append(item)
        
        # 提取二级标题下的斜体内容
        elif current_h2 and not current_h3 and ('*' in line):
            # 使用正则表达式提取斜体内容
            italic_pattern = r'\*([^*]+)\*'
            italic_matches = re.findall(italic_pattern, line)
            for match in italic_matches:
                italic_content_map[current_h2].append(match.strip())
    
    # [中间代码保持不变]
    
    # 创建MOC笔记（修改版）
    for h2_folder, subfolders in structure.items():
        for h3_subfolder, notes in subfolders.items():
            # 创建MOC文件路径
            moc_name = f"{h3_subfolder} MOC.md"
            moc_path = os.path.join(base_path, h2_folder, h3_subfolder, moc_name)
            
            # 写入MOC内容
            with open(moc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {h3_subfolder}\n\n")
                f.write(f"主题：{h2_folder} > {h3_subfolder}\n\n")
                
                # 添加核心概念（斜体内容）
                if italic_content_map[h2_folder]:
                    f.write("## 核心概念\n\n")
                    for italic in italic_content_map[h2_folder]:
                        f.write(f"- {italic}\n")
                    f.write("\n")
                
                f.write("## 笔记列表\n\n")
                
                # [后面的代码保持不变]
    
    print("MOC笔记和核心概念创建完成")
```

### 第九步：创建总览笔记

**目标**：学习文件操作和统计信息收集，创建整个知识库的总览笔记。

**任务提示**：
1. 收集统计信息：文件夹数、子文件夹数、笔记数、钩子数
2. 创建总览笔记文件
3. 添加统计信息和导航链接
4. 添加生成时间

**知识点**：
- 统计信息收集：使用计数器变量
- 时间处理：`datetime.now()`获取当前时间
- 字符串格式化：创建复杂的输出格式
- 文件操作：写入总览笔记

**预期代码结构**：
```python
def build_knowledge_base(markdown_file=None, base_path=None):
    # [前面的代码保持不变，但需要添加统计信息收集]
    
    # 初始化统计信息
    stats = {
        'folders': 0,
        'subfolders': 0,
        'atomic_notes': 0,
        'hooks': 0
    }
    
    # 修改解析部分，更新统计信息
    for line in lines:
        # [前面的代码保持不变]
        
        # 处理二级标题
        if line.startswith('## '):
            # [前面的代码保持不变]
            stats['folders'] += 1  # 增加文件夹计数
            
        # 处理三级标题
        elif line.startswith('### ') and current_h2:
            # [前面的代码保持不变]
            stats['subfolders'] += 1  # 增加子文件夹计数
            
        # 处理列表项
        elif line.startswith('- ') and current_h2 and current_h3:
            item = line[2:].strip()
            
            # 检查是否是钩子
            if item.startswith('钩子:'):
                # [前面的代码保持不变]
                stats['hooks'] += 1  # 增加钩子计数
            else:
                # [前面的代码保持不变]
                stats['atomic_notes'] += 1  # 增加笔记计数
    
    # [中间代码保持不变]
    
    # 创建总览笔记
    base_filename = os.path.splitext(os.path.basename(markdown_file))[0]
    overview_path = os.path.join(base_path, f"{base_filename}学习总览.md")
    
    with open(overview_path, 'w', encoding='utf-8') as f:
        # 写入标题和时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"# {base_filename}学习总览\n\n")
        f.write(f"生成时间：{current_time}\n\n")
        
        # 写入统计信息
        f.write("## 统计信息\n\n")
        f.write(f"- 顶级文件夹: {stats['folders']}个\n")
        f.write(f"- 子文件夹: {stats['subfolders']}个\n")
        f.write(f"- 原子笔记: {stats['atomic_notes']}个\n")
        f.write(f"- 钩子数量: {stats['hooks']}个\n\n")
        
        # 写入导航
        f.write("## 知识库导航\n\n")
        for h2_folder in structure.keys():
            f.write(f"### {h2_folder}\n\n")
            for h3_subfolder in structure[h2_folder].keys():
                moc_link = os.path.join(h2_folder, h3_subfolder, f"{h3_subfolder} MOC.md")
                f.write(f"- [[{moc_link}]]\n")
            f.write("\n")
    
    print("总览笔记创建完成")
    print("知识库构建完成！")
```

### 第十步：完善命令行参数处理

**目标**：学习命令行参数处理，使脚本更加灵活易用。

**任务提示**：
1. 修改主程序入口，处理不同的命令行参数组合
2. 添加帮助信息显示功能
3. 实现自动检测Markdown文件的功能
4. 添加错误处理和用户友好的提示

**知识点**：
- 命令行参数：`sys.argv`获取命令行参数
- 条件判断：处理不同的参数组合
- 函数调用：根据参数调用不同的函数
- 列表操作：检查参数数量和内容

**预期代码结构**：
```python
def print_usage():
    """打印使用说明"""
    print("使用方法：")
    print("  python my_knowledge_builder.py")
    print("  python my_knowledge_builder.py <markdown_file>")
    print("  python my_knowledge_builder.py <markdown_file> <output_dir>")
    print("  python my_knowledge_builder.py -h/--help/help")
    print("\n参数说明：")
    print("  <markdown_file>  Markdown大纲文件路径")
    print("  <output_dir>    输出目录路径（可选，默认为Markdown文件所在目录）")
    print("  -h/--help/help  显示帮助信息")

def find_markdown_file():
    """在当前目录中查找Markdown文件"""
    for file in os.listdir('.'):
        if file.endswith('.md') and not file.startswith(('总览', 'MOC')):
            return file
    return None

# 主程序入口
if __name__ == "__main__":
    # 处理命令行参数
    if len(sys.argv) == 1:
        # 无参数：自动查找Markdown文件
        markdown_file = find_markdown_file()
        if markdown_file:
            print(f"找到文件：{markdown_file}")
            build_knowledge_base(markdown_file)
        else:
            print("错误：当前目录下未找到Markdown文件")
            print_usage()
    elif len(sys.argv) == 2:
        # 一个参数：可能是文件路径或帮助请求
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
        else:
            build_knowledge_base(sys.argv[1])
    elif len(sys.argv) == 3:
        # 两个参数：文件路径和输出目录
        build_knowledge_base(sys.argv[1], sys.argv[2])
    else:
        # 参数过多
        print("错误：参数过多")
        print_usage()
```

## 学习总结

通过完成以上十个步骤，你已经成功复刻了一个完整的知识库构建工具，并学习了以下Python核心概念：

1. **模块导入**：`import`和`from...import`语句
2. **函数定义和调用**：`def`语句、参数传递、返回值
3. **条件判断**：`if-elif-else`结构、if嵌套
4. **循环结构**：`for`循环、嵌套循环
5. **数据结构**：字典、列表、嵌套数据结构
6. **字符串操作**：`startswith()`、`strip()`、切片、格式化
7. **文件操作**：`with open()`、读写文件、异常处理
8. **路径操作**：`os.path.join()`、`os.makedirs()`、`os.path.exists()`
9. **正则表达式**：`re.findall()`、正则模式
10. **命令行参数处理**：`sys.argv`、条件判断
11. **时间处理**：`datetime.now()`、时间格式化
12. **列表推导式**：简洁的列表创建方式

## 进阶挑战

如果你已经完成了以上所有步骤，可以尝试以下进阶挑战：

1. **添加更多Markdown语法支持**：支持粗体、链接、代码块等
2. **创建GUI界面**：使用tkinter或PyQt创建图形用户界面
3. **添加配置文件支持**：使用JSON或YAML文件存储配置
4. **实现增量更新**：只更新变化的部分，而不是重建整个知识库
5. **添加日志功能**：记录操作过程和错误信息
6. **支持更多输出格式**：如HTML、PDF等
7. **添加单元测试**：使用unittest或pytest测试代码
8. **优化性能**：处理大型文件时的性能优化

祝你学习愉快！