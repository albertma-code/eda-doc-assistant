import streamlit as st
import subprocess
import time
from retriever import get_retriever
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from generator import generate_answer

st.title("📄 EDA文档智能问答")
st.caption("基于内部知识库的智能问答系统")

# 直接加载已有的向量数据库
@st.cache_resource
def load_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings
    )
    return get_retriever(vectorstore)

# 检查Ollama是否在运行
def check_ollama():
    try:
        import requests
        requests.get("http://localhost:11434")
        return True
    except:
        return False

if not check_ollama():
    st.warning("⚠️ Ollama未启动")
    if st.button("🚀 启动Ollama"):
        subprocess.Popen(["ollama", "serve"])
        time.sleep(2)
        if check_ollama():
            st.success("✅ Ollama已启动！")
            st.rerun()
        else:
            st.error("启动失败，请手动运行 `ollama serve`")
    st.stop()
    
with st.spinner("正在加载知识库，请稍候..."):
    retriever = load_retriever()

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 输入框
if question := st.chat_input("输入你的问题..."):
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            answer, sources = generate_answer(question, retriever)
        st.write(answer)
        if sources:
            st.caption("📄 来源：" + " | ".join(sources))
    st.session_state.messages.append({"role": "assistant", "content": answer})
