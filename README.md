# EDA Doc Assistant

基于 RAG（检索增强生成）技术的文档智能问答工具。

## 功能
上传任意 PDF 文档，用自然语言提问，AI 自动从文档中找到相关内容并生成回答。

## 技术栈
- **LangChain**：RAG 框架
- **ChromaDB**：本地向量数据库
- **HuggingFace**：文本向量化模型
- **Ollama + Qwen2.5**：本地大语言模型，完全免费无需 API Key

## 快速开始

### 安装依赖
pip install langchain langchain-community langchain-huggingface langchain-text-splitters pypdf chromadb sentence-transformers requests

### 安装 Ollama 并下载模型
ollama pull qwen2.5:14b

### 运行
python src/main.py

## 特点
- 完全本地运行，无需联网，无需付费
- 支持中文文档和中文提问
- 可替换任意 PDF 文档使用