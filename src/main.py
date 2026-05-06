import sys
from loader import load_and_split
from retriever import build_vectorstore, get_retriever
from generator import generate_answer

def main():
    # 第一步：读取PDF，切块
    pdf_path = input("请输入PDF文件路径：")
    print("正在读取文档...")
    chunks = load_and_split(pdf_path)
    
    # 第二步：构建向量数据库
    print("正在构建向量数据库，首次运行需要几分钟...")
    vectorstore = build_vectorstore(chunks)
    retriever = get_retriever(vectorstore)
    
    # 第三步：开始问答
    print("\n✅ 准备完成！开始提问吧（输入 exit 退出）\n")
    while True:
        question = input("你的问题：")
        if question.lower() == "exit":
            break
        
        print("正在查找答案...")
        answer = generate_answer(question, retriever)
        print(f"\nClaude的回答：\n{answer}\n")

if __name__ == "__main__":
    main()