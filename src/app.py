import streamlit as st
from loader import load_and_split
from retriever import build_vectorstore, get_retriever
from generator import generate_answer

st.title("📄 EDA文档智能问答")
st.caption("上传PDF文档，用中文提问，AI自动从文档中找答案")

# 上传PDF
uploaded_file = st.file_uploader("上传PDF文档", type="pdf")

if uploaded_file:
    pdf_path = f"../data/{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if "retriever" not in st.session_state:
        with st.spinner("正在读取文档，请稍候..."):
            chunks = load_and_split(pdf_path)
            vectorstore = build_vectorstore(chunks)
            st.session_state.retriever = get_retriever(vectorstore)
        st.success("文档加载完成，开始提问吧！")

    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 输入框（回车自动发送）
    if question := st.chat_input("输入你的问题..."):
        # 显示用户问题
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # 生成回答
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                answer = generate_answer(question, st.session_state.retriever)
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})