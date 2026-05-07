# EDA Doc Assistant

基于 RAG 技术的 EDA 文档智能问答系统，支持多文档导入，提供聊天式 Web 界面，完全本地运行。

## 功能
- 支持多个 PDF 文档同时导入
- 中文提问，自动从英文文档中检索并回答
- 回答时显示来源文档和页码
- 聊天式 Web 界面，支持历史对话
- 完全本地运行，无需 API Key，无需联网

## 技术栈
- **LangChain**：RAG 框架
- **ChromaDB**：本地向量数据库
- **HuggingFace MiniLM**：多语言文本向量化
- **Ollama + Qwen2.5:14b**：本地大语言模型
- **Streamlit**：Web 界面

## 快速开始

### 1. 安装依赖
pip install langchain langchain-community langchain-huggingface langchain-text-splitters langchain-ollama pypdf chromadb sentence-transformers requests streamlit

### 2. 安装 Ollama 并下载模型
ollama pull qwen2.5:14b

### 3. 导入文档（CAD工程师操作）
python src/ingest.py data/your_doc.pdf data/another_doc.pdf

### 4. 启动问答界面
streamlit run src/app.py --server.fileWatcherType none

## 项目结构
├── src/
│   ├── ingest.py      # 文档导入脚本
│   ├── loader.py      # PDF读取与切块
│   ├── retriever.py   # 向量化与检索
│   ├── generator.py   # 调用本地模型生成回答
│   └── app.py         # Streamlit网页界面
└── data/              # 存放PDF文档