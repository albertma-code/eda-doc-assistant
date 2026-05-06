from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split(pdf_path: str):
    # 读取PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # 切块，每块500字，块之间重叠50字
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    
    print(f"共读取 {len(documents)} 页，切成 {len(chunks)} 个块")
    return chunks