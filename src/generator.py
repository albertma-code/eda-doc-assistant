import requests

def generate_answer(question: str, retriever):
    # 从ChromaDB找最相关的3个文本块
    relevant_chunks = retriever.invoke(question)
    
    # 拼接成上下文
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
    # 发给本地Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:14b",
            "prompt": f"""请根据以下文档内容回答问题。如果文档中没有相关信息，请直接说不知道。

文档内容：
{context}

问题：{question}""",
            "stream": False
        }
    )
    
    return response.json()["response"]