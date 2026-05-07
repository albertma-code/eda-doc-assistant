import requests

def generate_answer(question: str, retriever):
    relevant_chunks = retriever.invoke(question)
    
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
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
    
    answer = response.json()["response"]
    
    # 提取来源信息
    sources = []
    for chunk in relevant_chunks:
        source = chunk.metadata.get("source", "未知文档")
        page = chunk.metadata.get("page", "未知页码")
        source_info = f"{source} 第{page+1}页"
        if source_info not in sources:
            sources.append(source_info)
    
    return answer, sources