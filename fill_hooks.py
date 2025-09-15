import os
import sys
import openai

# ==============================================================================
# --- 1. AI 配置区域 (请在此处修改) ---
# ==============================================================================

# 安全地从环境变量中获取您的 DeepSeek API 密钥
# 这段代码会读取您在系统环境变量中设置的 "DEEPSEEK_API_KEY"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# 【请务必修改】在这里替换为你的 DeepSeek API 端点
# 通常是 "https://api.deepseek.com/v1" 或类似的地址
DEEPSEEK_API_BASE_URL = "https://api.deepseek.com/v1" 

# 检查密钥是否存在，如果不存在则给出清晰的错误提示并退出
if not DEEPSEEK_API_KEY:
    print("错误：无法找到 DEEPSEEK_API_KEY 环境变量。")
    print("请按照之前的教程，在Windows环境变量中设置您的 DeepSeek API 密钥。")
    sys.exit(1)

# ==============================================================================
# --- 2. 核心功能代码 (通常无需修改) ---
# ==============================================================================

def read_context_files(directory):
    """遍历所有子文件夹，读取所有 .md 文件的内容，合并成一个大的上下文。"""
    full_context = ""
    print(f"开始读取上下文文件夹: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            # 确保我们不会把主文件自己也读进去作为上下文
            if file.endswith(".md") and os.path.join(root, file) != main_file_path:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f"正在读取上下文: {file_path}")
                        # 为每个文件内容加上分隔符，方便 AI 理解
                        full_context += f"--- 来自文件: {file} ---\n{f.read()}\n\n"
                except Exception as e:
                    print(f"读取文件 {file_path} 失败: {e}")
    return full_context

def fill_hooks_with_ai(main_file_path, context):
    """读取主文件，使用 AI 填充知识钩子。"""
    if not context.strip():
        print("警告: 上下文内容为空，无法填充钩子，脚本将直接退出。")
        return

    print(f"开始使用 AI 填充主文件: {main_file_path}")
    
    # 初始化 AI 客户端，传入密钥和 API Base URL
    try:
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_API_BASE_URL
        )
    except Exception as e:
        print(f"初始化 AI 客户端失败: {e}")
        return
    
    with open(main_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped_line = line.strip()
        # 寻找需要填充的钩子
        if stripped_line.startswith('- 钩子:'):
            question = stripped_line.replace('- 钩子:', '').strip()
            
            new_lines.append(line) # 先保留原始问题行

            print(f"\n正在为钩子生成内容: {question}")
            
            try:
                # --- 这是调用 DeepSeek AI 的核心 ---
                prompt = f"""
                你是一位知识渊博的学者。请根据以下提供的学习材料，用简洁、启发性的语言，回答下面的问题。

                # 学习材料 (上下文):
                {context}

                # 需要回答的问题:
                {question}

                # 你的回答 (请直接针对问题进行回答，不要说“根据提供的材料...”或类似的话):
                """

                response = client.chat.completions.create(
                    model="deepseek-chat",  # 【请确认】这是您要使用的 DeepSeek 模型名称
                    messages=[
                        {"role": "system", "content": "你是一位知识渊博、善于总结的学者。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                )
                
                answer = response.choices[0].message.content.strip()

                # 将 AI 的回答格式化为 Markdown 引用块，并添加到问题下方
                # 我们将多行回答合并为一行，以保持格式整洁
                formatted_answer = f"> {answer.replace(os.linesep, ' ').replace('  ', ' ')}\n"
                new_lines.append(formatted_answer)
                print(f"  └── AI 回答: {answer}")

            except Exception as e:
                print(f"  └── 调用 AI 失败: {e}")
                # 即使失败，也添加一个提示，以防工作流中断
                new_lines.append("> (AI 内容生成失败，请检查 API 密钥、网络或账户余额)\n")
        else:
            # 如果不是钩子行，直接保留
            new_lines.append(line)

    # 将所有新内容（包括原始行和 AI 生成的回答）一次性写回原文件
    with open(main_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n知识钩子填充完毕！")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python fill_hooks.py <主Markdown文件路径> <内容文件夹路径>")
        sys.exit(1)
    
    main_file_path = sys.argv[1]
    content_dir = sys.argv[2]

    # 1. 读取所有子文件的内容作为上下文
    knowledge_context = read_context_files(content_dir)

    # 2. 使用 AI 填充主文件的钩子
    fill_hooks_with_ai(main_file_path, knowledge_context)