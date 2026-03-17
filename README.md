# 🛡️ CyberShield – Advanced RAG & Intelligent Workflow System

CyberShield is an advanced **Retrieval-Augmented Generation (RAG)** system designed to analyze, organize, and query large cybersecurity documentation collections.

The system combines **semantic search**, **structured knowledge extraction**, and **LLM-based routing** to provide accurate and explainable answers from complex technical documents.

---

# 🚀 Key Capabilities

### 🧠 Hybrid LLM Router

An intelligent routing layer determines whether a user query should be answered using:

* **Structured knowledge (JSON Knowledge Base)**
* **Semantic search over vector embeddings**

### 📚 Structured Knowledge Extraction

A custom extraction pipeline automatically identifies and extracts:

* Architectural decisions
* Security rules
* Technical warnings
* System constraints

from large documentation collections.

### 🔎 Semantic Retrieval (RAG)

Documents are indexed into a **vector database** allowing the system to retrieve relevant context and generate grounded responses.

### 🔁 Intelligent Workflow Engine

Built using **LlamaIndex Workflows**, enabling:

* Multi-step reasoning
* Retry logic when results are insufficient
* Context validation before answering

### 🔐 Secure Network Compatibility

CyberShield supports **Direct Inference mode**, allowing stable communication with LLM providers even under strict SSL inspection environments.

---

# 🧠 System Architecture

```
User Question
      │
      ▼
  LLM Router
 (Query Classification)
  /            \
 ▼              ▼
Structured     Semantic
Query Path     Search Path
(JSON KB)      (Vector DB)
      \        /
       ▼      ▼
     Validation
       │
       ▼
  Final Response
```

---

# 🧰 Tech Stack

| Component       | Technology           |
| --------------- | -------------------- |
| LLM             | Groq – Llama-3.3-70B |
| Framework       | LlamaIndex           |
| Workflow Engine | LlamaIndex Workflows |
| Vector Storage  | Local Vector Store   |
| Structured Data | JSON Knowledge Base  |
| Validation      | Pydantic             |
| UI              | Gradio               |
| Networking      | HTTPX                |

---

# 📂 Project Structure

```
CyberShield/
│
├── data/
│   ├── claude_docs/
│   └── cursor_docs/
│
├── src/
│   ├── main.py
│   ├── extract_data.py
│   ├── workflow_chat.py
│   ├── query_chat.py
│   ├── schema.py
│   └── utils.py
│
├── storage/
│   ├── index_store.json
│   ├── docstore.json
│   ├── graph_store.json
│   └── image_vector_store.json
│
├── requirements.txt
└── README.md
```

---

# ⚡ Quick Start

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USER_NAME/CyberShield-RAG-Inference.git
cd CyberShield-RAG-Inference
pip install -r requirements.txt
```

---

# ⚙️ Environment Setup

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

# 📋 Running the System

### 1️⃣ Build the Vector Index

```
python src/main.py
```

This step indexes the documentation and builds the vector database used for semantic retrieval.

---

### 2️⃣ Extract Structured Knowledge

```
python src/extract_data.py
```

This script analyzes the documents and builds a structured **Knowledge Base**.

---

### 3️⃣ Start the Chat Interface

```
python src/query_chat.py
```

A **Gradio web interface** will open, allowing you to interact with the system.

---

# 💬 Example Queries

### Structured Queries

These queries are answered using the structured knowledge base.

* "Show me all architectural decisions"
* "List the security rules"
* "What technical warnings exist?"

### Semantic Queries

These queries use vector retrieval and contextual reasoning.

* "How is the firewall configured?"
* "Explain the authentication workflow"
* "How does the system handle network security?"

### Validation Queries

These queries test the system’s ability to detect irrelevant requests.

* "How do I make a pizza?"

---

# 🔍 How It Works

CyberShield processes each user query using a **multi-stage workflow**:

1. **Query Classification** – The router determines the best retrieval strategy.
2. **Context Retrieval** – Either structured JSON lookup or vector search.
3. **Validation Step** – Ensures retrieved context is relevant.
4. **Retry Logic** – If context is insufficient, the system performs an additional search.
5. **Answer Generation** – The LLM generates a grounded response with references.

---

# 📌 Notes

This project demonstrates advanced **RAG architecture patterns**, including:

* Hybrid retrieval strategies
* Structured knowledge extraction
* Workflow-driven reasoning pipelines
* LLM routing strategies

---

# 👩‍💻 Author

Developed by **Efrat**

---
