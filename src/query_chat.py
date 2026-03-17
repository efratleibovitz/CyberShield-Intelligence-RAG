# import os
# import warnings
# import pip_system_certs.wrapt_requests
# warnings.filterwarnings('ignore')

# from dotenv import load_dotenv
# from pinecone import Pinecone
# from llama_index.core import VectorStoreIndex, StorageContext, get_response_synthesizer
# from llama_index.vector_stores.pinecone import PineconeVectorStore
# from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.llms.cohere import Cohere
# import gradio as gr

# load_dotenv()

# # --- הגדרות בסיסיות ---
# embed_model = CohereEmbedding(
#     cohere_api_key=os.environ["COHERE_API_KEY"],
#     model_name="embed-english-v3.0",
#     input_type="search_query"
# )

# llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-plus")

# # חיבור ל-Pinecone
# pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# pinecone_index = pc.Index("cyber-shield-index")
# vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# # יצירת האינדקס מתוך ה-Vector Store הקיים
# index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

# # --- הגדרת רכיבי ה-RAG (לפי הדרישות) ---

# # 1. Retriever - מוצא את ה-Nodes הכי רלוונטיים
# retriever = index.as_retriever(similarity_top_k=3)

# # 2. Response Synthesizer - מנסח את התשובה הסופית
# response_synthesizer = get_response_synthesizer(llm=llm, response_mode="compact")

# # 3. Query Engine - מחבר את הכל ביחד
# query_engine = index.as_query_engine(
#     retriever=retriever,
#     response_synthesizer=response_synthesizer
# )

# def chat_function(message, history):
#     try:
#         # ביצוע השאילתה
#         response = query_engine.query(message)
#         return str(response)
#     except Exception as e:
#         return f"שגיאה: {str(e)}"

# # --- ממשק Gradio ---
# view = gr.ChatInterface(
#     fn=chat_function,
#     title="Cyber Shield Chat - RAG System",
#     description="שאל שאלות על בסיס הידע של הכלים שהעלנו (Claude/Cursor)",
#     examples=["What are the main features of Cursor?", "How to use Claude for code?"]
# )

# if __name__ == "__main__":
#     print("מפעיל את ממשק הצ'אט...")
#     view.launch(share=False)




import os
import httpx    

import gradio as gr
from main import index  # מייבא את האינדקס המוכן
from workflow_chat import CyberShieldWorkflow, StatusEvent
async def chat_interface(message, history):
    # מעבירים את האינדקס ל-Workflow בזמן היצירה
    wf = CyberShieldWorkflow(index=index, timeout=60, verbose=True)
    handler = wf.run(query=message)
    
    status_display = ""
    async for event in handler.stream_events():
        if isinstance(event, StatusEvent):
            status_display = f"*{event.msg}*\n\n"
            yield status_display 
            
    final_result = await handler
    yield str(final_result)

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown("# 🛡️ Cyber Shield - Live Workflow")
    gr.ChatInterface(fn=chat_interface)

if __name__ == "__main__":
    demo.launch()