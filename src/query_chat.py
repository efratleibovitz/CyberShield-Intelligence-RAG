# # import os
# # import warnings
# # import pip_system_certs.wrapt_requests
# # warnings.filterwarnings('ignore')

# # from dotenv import load_dotenv
# # from pinecone import Pinecone
# # from llama_index.core import VectorStoreIndex, StorageContext, get_response_synthesizer
# # from llama_index.vector_stores.pinecone import PineconeVectorStore
# # from llama_index.embeddings.cohere import CohereEmbedding
# # from llama_index.llms.cohere import Cohere
# # import gradio as gr

# # load_dotenv()

# # # --- הגדרות בסיסיות ---
# # embed_model = CohereEmbedding(
# #     cohere_api_key=os.environ["COHERE_API_KEY"],
# #     model_name="embed-english-v3.0",
# #     input_type="search_query"
# # )

# # llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-plus")

# # # חיבור ל-Pinecone
# # pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# # pinecone_index = pc.Index("cyber-shield-index")
# # vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# # # יצירת האינדקס מתוך ה-Vector Store הקיים
# # index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

# # # --- הגדרת רכיבי ה-RAG (לפי הדרישות) ---

# # # 1. Retriever - מוצא את ה-Nodes הכי רלוונטיים
# # retriever = index.as_retriever(similarity_top_k=3)

# # # 2. Response Synthesizer - מנסח את התשובה הסופית
# # response_synthesizer = get_response_synthesizer(llm=llm, response_mode="compact")

# # # 3. Query Engine - מחבר את הכל ביחד
# # query_engine = index.as_query_engine(
# #     retriever=retriever,
# #     response_synthesizer=response_synthesizer
# # )

# # def chat_function(message, history):
# #     try:
# #         # ביצוע השאילתה
# #         response = query_engine.query(message)
# #         return str(response)
# #     except Exception as e:
# #         return f"שגיאה: {str(e)}"

# # # --- ממשק Gradio ---
# # view = gr.ChatInterface(
# #     fn=chat_function,
# #     title="Cyber Shield Chat - RAG System",
# #     description="שאל שאלות על בסיס הידע של הכלים שהעלנו (Claude/Cursor)",
# #     examples=["What are the main features of Cursor?", "How to use Claude for code?"]
# # )

# # if __name__ == "__main__":
# #     print("מפעיל את ממשק הצ'אט...")
# #     view.launch(share=False)



# import os
# import warnings
# import httpx
# import gradio as gr
# from dotenv import load_dotenv
# from llama_index.core import StorageContext, load_index_from_storage, Settings
# from llama_index.core.embeddings import MockEmbedding

# load_dotenv()
# warnings.filterwarnings('ignore')

# # 1. הגדרת חיפוש מקומי (Mock) כדי שלא יקרוס בגלל SSL
# Settings.embed_model = MockEmbedding(embed_dim=384)

# # 2. פונקציה שפונה ל-Groq ישירות (בלי הספרייה שחסומה)
# def ask_groq(prompt):
#     url = "https://api.groq.com/openai/v1/chat/completions"
#     key = os.environ.get('GROQ_API_KEY')
    
#     if not key:
#         return "שגיאה: חסר מפתח API של Groq בקובץ .env"

#     headers = {
#         "Authorization": f"Bearer {key}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "llama-3.3-70b-versatile",
#         "messages": [{"role": "user", "content": prompt}]
#     }
    
#     with httpx.Client(verify=False) as client:
#         response = client.post(url, headers=headers, json=data)
        
#         # אם יש שגיאה מהשרת, נציג אותה
#         if response.status_code != 200:
#             return f"שגיאה מהשרת של Groq: {response.text}"
            
#         return response.json()['choices'][0]['message']['content']
# # 3. טעינת האינדקס מהמחשב
# storage_context = StorageContext.from_defaults(persist_dir="./storage")
# index = load_index_from_storage(storage_context)

# def chat_function(message, history):
#     try:
#         # א. שלב ה-Retrieval (שליפה)
#         retriever = index.as_retriever()
#         nodes = retriever.retrieve(message)
        
#         # הדפסה לטרמינל כדי שתוכלי לעקוב:
#         print(f"\n--- [מחשבת המערכת: שליפת מידע] ---")
#         print(f"השאלה שנשאלה: {message}")
#         context = ""
#         for i, n in enumerate(nodes):
#             content = n.node.get_content()
#             print(f"\nצ'אנק מספר {i+1} שנשלף:")
#             print(f"{content[:200]}...") # מדפיס רק את ההתחלה של כל צ'אנק
#             context += content + "\n"
#         print(f"--- [סוף שליפה] ---\n")
        
#         # ב. שלב ה-Generation (שליחה ל-Groq)
#         full_prompt = f"Context: {context}\n\nQuestion: {message}\nAnswer based only on context:"
#         answer = ask_groq(full_prompt)
#         return answer
#     except Exception as e:
#         return f"שגיאה: {str(e)}"

# # 4. ממשק Gradio
# view = gr.ChatInterface(fn=chat_function, title="Cyber Shield - Groq Direct Mode")

# if __name__ == "__main__":
#     print("🚀 מפעיל צ'אט במצב ישיר... נטפרי לא יכולים לעצור את זה!")
#     view.launch(share=False)


import os
import warnings
import httpx
import gradio as gr
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.core.embeddings import MockEmbedding

load_dotenv()
warnings.filterwarnings('ignore')

Settings.embed_model = MockEmbedding(embed_dim=384)

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    with httpx.Client(verify=False, timeout=30.0) as client:
        response = client.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']

# טעינת האינדקס
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

def chat_function(message, history):
    try:
        retriever = index.as_retriever(similarity_top_k=4)
        nodes = retriever.retrieve(message)
        
        # בניית ההקשר ורשימת המקורות
        context = ""
        sources = []
        for i, n in enumerate(nodes):
            text = n.node.get_content()
            source_name = n.node.metadata.get('file_name', f'Document {i+1}')
            context += f"\n[Source: {source_name}]\n{text}\n"
            sources.append(f"📄 {source_name}")
        
        full_prompt = f"Context: {context}\n\nQuestion: {message}\nAnswer based only on context:"
        answer = ask_groq(full_prompt)
        
        # החזרת התשובה יחד עם המקורות בצורה יפה
        formatted_sources = "\n\n**Sources used:** " + ", ".join(list(set(sources)))
        return answer + formatted_sources
        
    except Exception as e:
        return f"שגיאה: {str(e)}"

# עיצוב הממשק (Theme)
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate")) as demo:
    gr.Markdown("# 🛡️ Cyber Shield AI")
    gr.Markdown("Interactive RAG system for system specifications and security protocols.")
    gr.ChatInterface(fn=chat_function)

if __name__ == "__main__":
    demo.launch(share=False)