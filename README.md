# 🛡️ CyberShield RAG Inference System

An advanced **Retrieval-Augmented Generation (RAG)** system designed to provide intelligent insights into cybersecurity specifications and development protocols.

## 🚀 Overview
CyberShield AI leverages **LlamaIndex** and **Groq's Llama-3.3** model to allow users to chat with technical documentation. It breaks down complex PDF/Markdown files into searchable segments and provides context-aware answers.

## ✨ Key Features
- **Direct API Inference:** Custom HTTP implementation to bypass SSL inspection and network restrictions.
- **Smart Retrieval:** Uses localized vector storage for fast context fetching.
- **Interactive UI:** Built with Gradio for a seamless, modern chat experience.
- **Source Attribution:** Every answer includes the specific documents used as sources.

## 🛠️ Tech Stack
- **Orchestration:** LlamaIndex
- **LLM:** Groq (Llama-3.3-70b-versatile)
- **Frontend:** Gradio
- **Networking:** HTTPX (Custom Secure Client)

## 📋 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USER_NAME/CyberShield-RAG-Inference.git](https://github.com/YOUR_USER_NAME/CyberShield-RAG-Inference.git)
   cd CyberShield-RAG-Inference


2. Install Dependencies:

   ```bash
    pip install -r requirements.txt

3. Environment Configuration:
Create a .env file in the root directory and add your Groq API Key:

   ```bash
    GROQ_API_KEY=your_actual_key_here

4. Initialize the Index:
   ```bash

    python src/main.py


⚠️ Network Note
This project was optimized for high-security network environments. It uses a specialized Direct-Inference mode to ensure stable communication with AI cloud providers even under strict SSL policies.