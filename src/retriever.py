from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def build_vectorstore(chunks):
    # 用HuggingFace的免费模型把文本转成向量
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # 把所有块存入ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./data/chroma_db"
    )
    
    print("向量数据库构建完成")
    return vectorstore

def get_retriever(vectorstore):
    # 每次搜索返回最相关的3个块
    return vectorstore.as_retriever(search_kwargs={"k": 3})