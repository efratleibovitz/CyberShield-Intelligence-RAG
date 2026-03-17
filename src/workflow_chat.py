# import os
# import asyncio
# import httpx
# from dotenv import load_dotenv
# from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step, Context
# from llama_index.core import StorageContext, load_index_from_storage, Settings
# from llama_index.core.embeddings import MockEmbedding

# load_dotenv()

# Settings.embed_model = MockEmbedding(embed_dim=384)
# storage_context = StorageContext.from_defaults(persist_dir="./storage")
# index = load_index_from_storage(storage_context)

# # הגדרת אירועים שמעבירים את השאלה לאורך כל הדרך
# class RetrievalEvent(Event):
#     context_str: str
#     original_query: str

# class ValidationEvent(Event):
#     context_str: str
#     original_query: str
#     is_valid: bool

# class CyberShieldWorkflow(Workflow):
    
#     @step
#     async def ingest_and_retrieve(self, ev: StartEvent) -> RetrievalEvent:
#         query = ev.get("query")
#         retriever = index.as_retriever(similarity_top_k=3)
#         nodes = retriever.retrieve(query)
#         context_str = "\n".join([n.node.get_content() for n in nodes])
#         return RetrievalEvent(context_str=context_str, original_query=query)

#     @step
#     async def validate_context(self, ev: RetrievalEvent) -> ValidationEvent:
#         # בדיקה אם המידע שחזר מספיק ארוך (ולידציה)
#         is_valid = len(ev.context_str.strip()) > 50
#         return ValidationEvent(
#             context_str=ev.context_str, 
#             original_query=ev.original_query, 
#             is_valid=is_valid
#         )

#     @step
#     async def generate_answer(self, ev: ValidationEvent) -> StopEvent:
#         if not ev.is_valid:
#             return StopEvent(result="מצטער, לא מצאתי מספיק מידע רלוונטי במסמכים.")
            
#         prompt = f"Context: {ev.context_str}\n\nQuestion: {ev.original_query}\nAnswer based only on context:"
#         answer = await self.ask_groq_async(prompt)
#         return StopEvent(result=answer)

#     async def ask_groq_async(self, prompt):
#         async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
#             url = "https://api.groq.com/openai/v1/chat/completions"
#             headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}
#             data = {
#                 "model": "llama-3.3-70b-versatile",
#                 "messages": [{"role": "user", "content": prompt}]
#             }
#             response = await client.post(url, headers=headers, json=data)
#             return response.json()['choices'][0]['message']['content']

# async def main():
#     wf = CyberShieldWorkflow(timeout=60, verbose=True)
#     result = await wf.run(query="What is the firewall config?")
#     print(f"\n✅ Final Result:\n{result}")

# if __name__ == "__main__":
#     asyncio.run(main())


import os
import asyncio
import httpx
from dotenv import load_dotenv
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step, Context
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.core.embeddings import MockEmbedding

load_dotenv()

# הגדרות אינדקס
Settings.embed_model = MockEmbedding(embed_dim=384)
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

class StatusEvent(Event):
    msg: str

class RetrievalEvent(Event):
    context_str: str
    query: str

class ValidationEvent(Event):
    context_str: str
    query: str
    is_valid: bool

class CyberShieldWorkflow(Workflow):
    
    @step
    async def ingest_and_retrieve(self, ctx: Context, ev: StartEvent) -> RetrievalEvent:
        query = ev.get("query")
        ctx.write_event_to_stream(StatusEvent(msg="🔍 שליפת מידע מהמסמכים..."))
        
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)
        context_str = "\n".join([n.node.get_content() for n in nodes])
        return RetrievalEvent(context_str=context_str, query=query)

    @step
    async def validate_context(self, ctx: Context, ev: RetrievalEvent) -> ValidationEvent:
        ctx.write_event_to_stream(StatusEvent(msg="🛡️ בודק את רלוונטיות המידע..."))
        await asyncio.sleep(0.5) # רק כדי שהמשתמש יספיק לראות
        is_valid = len(ev.context_str.strip()) > 50
        return ValidationEvent(context_str=ev.context_str, query=ev.query, is_valid=is_valid)

    @step
    async def generate_answer(self, ctx: Context, ev: ValidationEvent) -> StopEvent:
        if not ev.is_valid:
            return StopEvent(result="מצטער, לא נמצא מידע רלוונטי.")
        
        ctx.write_event_to_stream(StatusEvent(msg="🧠 מנסח תשובה חכמה..."))
        prompt = f"Context: {ev.context_str}\n\nQuestion: {ev.query}\nAnswer:"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}
            data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
            response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            answer = response.json()['choices'][0]['message']['content']
        
        return StopEvent(result=answer)