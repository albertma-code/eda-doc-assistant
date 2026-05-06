from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./data/chroma_db"
    )
    
    print("向量数据库构建完成")
    return vectorstore

def get_retriever(vectorstore):
    # 从3个增加到5个，获取更多相关内容
    return vectorstore.as_retriever(search_kwargs={"k": 5})