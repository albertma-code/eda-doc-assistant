import requests

def generate_answer(question: str, retriever):
    try:
        # 第一步：判断是否需要查文档
        check_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:14b",
                "prompt": f"""判断以下问题是否需要查询专业技术文档才能回答。

以下情况回答"不需要"：
- 问候语，比如"你好"、"早上好"
- 询问AI身份，比如"你是谁"、"你叫什么"
- 闲聊，比如"今天天气怎么样"
- 通用常识问题

以下情况回答"需要"：
- 涉及具体技术命令或工具的问题
- 涉及EDA、LSF、芯片设计的专业问题
- 需要查阅手册才能准确回答的问题

只回答"需要"或"不需要"，不要其他内容。

问题：{question}""",
                "stream": False
            }
        )
        
        response_text = check_response.json()["response"].strip()
        need_search = response_text == "需要" or (("需要" in response_text) and ("不需要" not in response_text))

        # 第二步：如果需要查文档，检索相关内容
        context = ""
        sources = []

        if need_search:
            chunks = retriever.invoke(question)
            context_parts = []
            for chunk in chunks:
                source = chunk.metadata.get("source", "未知文档")
                page = chunk.metadata.get("page", 0)
                sources.append(f"{source} 第{page+1}页")
                context_parts.append(chunk.page_content)
            context = "\n\n".join(context_parts)

        # 第三步：生成回答
        if context:
            prompt = f"""请根据以下文档内容回答问题。如果文档中没有相关信息，请直接说不知道。

文档内容：
{context}

问题：{question}"""
        else:
            prompt = question

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:14b",
                "prompt": prompt,
                "stream": False
            }
        )

        answer = response.json()["response"]
        sources = list(set(sources))
        return answer, sources

    except Exception as e:
        if "Connection refused" in str(e) or "10061" in str(e):
            return "❌ Ollama未启动，请先运行 `ollama serve`", []
        return f"❌ 发生错误：{str(e)}", []
    