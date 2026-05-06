import sys
from loader import load_and_split
from retriever import build_vectorstore

def ingest(pdf_path: str):
    print(f"正在读取文档：{pdf_path}")
    chunks = load_and_split(pdf_path)
    print("正在构建向量数据库...")
    build_vectorstore(chunks)
    print("✅ 文档导入完成！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python ingest.py <pdf路径>")
        sys.exit(1)
    ingest(sys.argv[1])