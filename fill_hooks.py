import os
import sys
import openai # 我们将使用 OpenAI 的 API，因为它非常强大。您也可以换成其他任何模型的 API

# --- 配置您的 AI ---
# 强烈建议将 API 密钥设置为环境变量，而不是写在代码里
# os.environ["OPENAI_API_KEY"] = "sk-..."
# 如果您的模型服务商使用类似 OpenAI 的接口（很多国产大模型都支持），可以在这里配置
# openai.api_base = "https://your-api-endpoint/v1"

def read_context_files(directory):
    """遍历所有子文件夹，读取所有 .md 文件的内容，合并成一个大的上下文。"""
    full_context = ""
    print(f"开始读取上下文文件夹: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f"正在读取: {file_path}")
                        full_context += f.read() + "\n\n---\n\n"
                except Exception as e:
                    print(f"读取文件 {file_path} 失败: {e}")
    return full_context

def fill_hooks_with_ai(main_file_path, context):
    """读取主文件，使用 AI 填充知识钩子。"""
    if not context.strip():
        print("警告: 上下文内容为空，无法填充钩子。")
        return

    print(f"开始处理主文件: {main_file_path}")
    
    client = openai.OpenAI()
    
    with open(main_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped_line = line.strip()
        # 寻找需要填充的钩子，可以根据您的具体格式微调
        if stripped_line.startswith('- 钩子:'):
            question = stripped_line.replace('- 钩子:', '').strip()
            
            # 将原始问题行先添加进去
            new_lines.append(line)

            print(f"\n正在为钩子生成内容: {question}")
            
            try:
                # --- 这是调用 AI 的核心 ---
                prompt = f"""
                你是一位知识渊博的学者。请根据以下提供的学习材料（上下文），用简洁、启发性的语言，回答下面的问题。

                # 学习材料 (上下文):
                {context}

                # 需要回答的问题:
                {question}

                # 你的回答 (直接回答，不要说“根据材料...”):
                """

                response = client.chat.completions.create(
                    model="gpt-4-turbo",  # 您可以换成任何强大的模型，比如 deepseek-coder 等
                    messages=[
                        {"role": "system", "content": "你是一位知识渊博的学者。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                )
                
                answer = response.choices[0].message.content.strip()

                # 将答案格式化后添加
                # 使用 > 引用块的格式，让答案在 Markdown 中更美观
                formatted_answer = f"> {answer.replace(os.linesep, ' ')}\n"
                new_lines.append(formatted_answer)
                print(f"AI 回答: {answer}")

            except Exception as e:
                print(f"调用 AI 失败: {e}")
                # 如果 AI 调用失败，也添加一个提示，避免流程中断
                new_lines.append("> (AI 内容生成失败)\n")
        else:
            # 如果不是钩子行，直接添加
            new_lines.append(line)

    # 将填充后的内容写回原文件
    with open(main_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n知识钩子填充完毕！")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python fill_hooks.py <主Markdown文件路径> <内容文件夹路径>")
        sys.exit(1)
    
    main_file = sys.argv[1]
    content_dir = sys.argv[2]

    # 1. 读取所有子文件的内容作为上下文
    knowledge_context = read_context_files(content_dir)

    # 2. 使用 AI 填充主文件的钩子
    fill_hooks_with_ai(main_file, knowledge_context)