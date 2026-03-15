#  Secure RAG Document Intelligence System

An **offline Retrieval-Augmented Generation (RAG) chatbot** that enables users to securely query and analyze PDF documents using a **locally hosted Large Language Model (LLM)**.

The system is designed for environments where **data privacy and security are critical**, such as corporate offices where sending documents to external AI APIs is not allowed.

---

# ⭐ Project Overview 

## 🟡 Situation

Organizations often handle **confidential internal documents** such as policies, reports, and technical manuals.
Most AI tools like ChatGPT require sending data to **external servers**, which creates **security and compliance concerns**.

Because of this, many organizations **cannot use public AI tools** to analyze internal documents.

---

## 🎯 Task

The objective was to build a **secure document intelligence system** that:

* Works **fully offline**
* Allows users to **query internal PDF documents**
* Uses **local AI models instead of external APIs**
* Provides **accurate answers with source citations**

---

## ⚙️ Action

To solve this problem, I implemented a **Retrieval-Augmented Generation (RAG) pipeline** consisting of several components:

### 1️⃣ Document Ingestion

PDF documents are uploaded and processed using a **PDF loader** to extract text content.

### 2️⃣ Text Chunking

Documents are split into **semantic chunks** using a recursive text splitter to improve retrieval accuracy.

### 3️⃣ Embedding Generation

Each chunk is converted into **vector embeddings** using a local embedding model running via **Ollama**.

### 4️⃣ Vector Storage

Embeddings are stored in **ChromaDB**, enabling efficient similarity search.

### 5️⃣ Retrieval

When a user asks a question, the system retrieves the **top relevant document chunks** from the vector database.

### 6️⃣ Response Generation

The retrieved context is passed to a **local LLM** which generates a response based only on the document content.

### 7️⃣ Source Attribution

The system includes **source file names and page numbers** so users can verify where the answer came from.

---

# 🚀 Key Features

* 🔐 **Fully Offline AI System**
* 📄 **PDF Document Question Answering**
* 🧠 **Local LLM via Ollama**
* 🔎 **Semantic Search with ChromaDB**
* 💬 **Interactive Chat UI with Streamlit**
* 📚 **Source Citation with Page Numbers**
* ⚡ **Efficient Chunking and Retrieval**

---

# 🧠 Tech Stack

| Component            | Technology  |
| -------------------- | ----------- |
| Programming Language | Python      |
| LLM Runtime          | Ollama      |
| AI Framework         | LangChain   |
| Vector Database      | ChromaDB    |
| UI Framework         | Streamlit   |
| Document Processing  | PyPDFLoader |

---

# 🏗️ System Architecture

```
PDF Documents
      │
      ▼
Document Loader
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation (Ollama)
      │
      ▼
Vector Database (ChromaDB)
      │
      ▼
Retriever
      │
      ▼
Local LLM (RAG Pipeline)
      │
      ▼
Generated Answer + Source Citation
```

---

# 🖥️ User Interface

The application provides a **web-based chat interface** built with Streamlit where users can:

1. Upload PDF documents
2. Index the documents into a vector database
3. Ask questions about the documents
4. Receive AI-generated answers with **source references**

---

# ▶️ How to Run the Project

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start the Streamlit interface

```bash
streamlit run ui.py
```

### 3️⃣ Open the application

```
http://localhost:8501
```

---

# 📊 Example Query

User Question:

```
What is the main topic discussed in this document?
```

Example AI Response:

```
The document discusses the architecture of transformer-based models used in natural language processing.

Source: attention_is_all_you_need.pdf, Page 2
```

---

# 📷 Demo

Screenshots and demo videos are available in the **output/** folder.

---

# 📌 Potential Use Cases

* Enterprise knowledge assistants
* Internal document search
* Policy and compliance analysis
* Research document exploration
* Secure AI assistants for organizations

---

# 🔮 Future Improvements

* Multi-document knowledge base
* PDF page highlighting for answers
* Document preview inside the UI
* Multi-user enterprise deployment
* Improved citation and reference visualization

---

# 👩‍💻 Author

**Diksha**

AI / Data Science Enthusiast focused on building **secure, practical AI systems using local models and RAG pipelines.**
