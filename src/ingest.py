import sys
import os
from loader import load_and_split
from retriever import build_vectorstore

def ingest(pdf_paths: list):
    all_chunks = []
    for pdf_path in pdf_paths:
        print(f"正在读取文档：{pdf_path}")
        chunks = load_and_split(pdf_path)
        all_chunks.extend(chunks)
        print(f"✅ {pdf_path} 读取完成，共{len(chunks)}个块")
    
    print(f"\n共{len(all_chunks)}个块，正在构建向量数据库...")
    build_vectorstore(all_chunks)
    print("✅ 所有文档导入完成！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python ingest.py <pdf1> <pdf2> ...")
        sys.exit(1)
    ingest(sys.argv[1:])