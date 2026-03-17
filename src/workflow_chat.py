# import os
# import asyncio
# import httpx
# from dotenv import load_dotenv
# from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step, Context
# from llama_index.core import StorageContext, load_index_from_storage, Settings
# from llama_index.core.embeddings import MockEmbedding

# load_dotenv()

# # הגדרות אינדקס
# Settings.embed_model = MockEmbedding(embed_dim=384)
# storage_context = StorageContext.from_defaults(persist_dir="./storage")
# index = load_index_from_storage(storage_context)

# class StatusEvent(Event):
#     msg: str

# class RetrievalEvent(Event):
#     context_str: str
#     query: str

# class ValidationEvent(Event):
#     context_str: str
#     query: str
#     is_valid: bool

# class CyberShieldWorkflow(Workflow):
    
#     @step
#     async def ingest_and_retrieve(self, ctx: Context, ev: StartEvent) -> RetrievalEvent:
#         query = ev.get("query")
#         ctx.write_event_to_stream(StatusEvent(msg="🔍 שליפת מידע מהמסמכים..."))
        
#         retriever = index.as_retriever(similarity_top_k=3)
#         nodes = retriever.retrieve(query)
#         context_str = "\n".join([n.node.get_content() for n in nodes])
#         return RetrievalEvent(context_str=context_str, query=query)

#     @step
#     async def validate_context(self, ctx: Context, ev: RetrievalEvent) -> ValidationEvent:
#         ctx.write_event_to_stream(StatusEvent(msg="🛡️ בודק את רלוונטיות המידע..."))
#         await asyncio.sleep(0.5) # רק כדי שהמשתמש יספיק לראות
#         is_valid = len(ev.context_str.strip()) > 50
#         return ValidationEvent(context_str=ev.context_str, query=ev.query, is_valid=is_valid)

#     @step
#     async def generate_answer(self, ctx: Context, ev: ValidationEvent) -> StopEvent:
#         if not ev.is_valid:
#             return StopEvent(result="מצטער, לא נמצא מידע רלוונטי.")
        
#         ctx.write_event_to_stream(StatusEvent(msg="🧠 מנסח תשובה חכמה..."))
#         prompt = f"Context: {ev.context_str}\n\nQuestion: {ev.query}\nAnswer:"
        
#         async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
#             headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}
#             data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
#             response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
#             answer = response.json()['choices'][0]['message']['content']
        
#         return StopEvent(result=answer)

import os
import asyncio
import httpx
from dotenv import load_dotenv
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step, Context
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.core.embeddings import MockEmbedding

load_dotenv()

# הגדרות ליבה - שימוש ב-MockEmbedding למניעת בעיות SSL/נטפרי
Settings.embed_model = MockEmbedding(embed_dim=384)

# טעינת האינדקס מהאחסון המקומי
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

# --- הגדרת אירועים (Events) ---
class StatusEvent(Event):
    msg: str

class RetrievalEvent(Event):
    context_str: str
    query: str
    search_iteration: int

class ValidationEvent(Event):
    context_str: str
    query: str
    is_valid: bool

# --- ה-Workflow המשודרג ---
class CyberShieldWorkflow(Workflow):
    
    @step
    async def ingest_and_retrieve(self, ctx: Context, ev: StartEvent) -> RetrievalEvent | StopEvent:
        query = ev.get("query")
        
        # ולידציה 1: קלט ריק או "שטויות"
        if not query or len(query.strip()) < 3:
            return StopEvent(result="⚠️ השאלה שסיפקת קצרה מדי או ריקה. אנא נסה לשאול שאלה מפורטת יותר.")
        
        ctx.write_event_to_stream(StatusEvent(msg="🔍 מחפש מקורות רלוונטיים במאגר..."))
        
        # שליפה ראשונית (top_k=3)
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)
        context_str = "\n".join([n.node.get_content() for n in nodes])
        
        return RetrievalEvent(context_str=context_str, query=query, search_iteration=1)

    @step
    async def validate_context(self, ctx: Context, ev: RetrievalEvent) -> ValidationEvent | RetrievalEvent:
        ctx.write_event_to_stream(StatusEvent(msg="🛡️ מנתח את רלוונטיות המידע סמנטית..."))
        await asyncio.sleep(0.5)

        # 1. שליפת ה-Scores של הצ'אנקים שנמצאו
        # אנחנו בודקים מה הציון הגבוה ביותר שקיבלנו מהחיפוש הסמנטי
        # הערה: כדי שזה יעבוד, אנחנו צריכים להעביר את ה-nodes מהשלב הקודם או לשלוף שוב
        
        context_len = len(ev.context_str.strip())
        
        # 2. ולידציה על בסיס נפח המידע והקשר
        # אם החיפוש הסמנטי החזיר מעט מאוד חומר
        if context_len < 200 and ev.search_iteration == 1:
            ctx.write_event_to_stream(StatusEvent(msg="🔍 המידע לא מספיק ממוקד, מנסה חיפוש סמנטי רחב..."))
            
            # ניתוב לחיפוש רחב יותר כדי לתת הזדמנות למצוא הקשר רחוק יותר
            retriever = index.as_retriever(similarity_top_k=5)
            nodes = retriever.retrieve(ev.query)
            
            # בדיקת ה-Score המקסימלי שנמצא
            max_score = nodes[0].score if nodes else 0
            
            # אם אפילו בחיפוש רחב הציון נמוך מאוד (למשל פחות מ-0.6)
            if max_score < 0.6:
                 ctx.write_event_to_stream(StatusEvent(msg="⚠️ רמת ביטחון נמוכה מאוד בתוצאות..."))
            
            expanded_context = "\n".join([n.node.get_content() for n in nodes])
            return RetrievalEvent(context_str=expanded_context, query=ev.query, search_iteration=2)

        # אם הגענו לפה, אנחנו סומכים על המידע או שזה הניסיון השני
        is_valid = context_len > 100
        return ValidationEvent(context_str=ev.context_str, query=ev.query, is_valid=is_valid)
    
    @step
    async def generate_answer(self, ctx: Context, ev: ValidationEvent) -> StopEvent:
        # טיפול במקרה של חוסר תוצאות (Confidence נמוך מדי)
        if not ev.is_valid:
            ctx.write_event_to_stream(StatusEvent(msg="❌ ולידציה נכשלה: אין מידע מספק."))
            return StopEvent(result="מצטער, לא מצאתי מספיק מידע רלוונטי במסמכים כדי לספק תשובה מהימנה.")
        
        ctx.write_event_to_stream(StatusEvent(msg="🧠 מנסח תשובה סופית על בסיס המקורות..."))
        
        # בניית הפרומפט ל-LLM (Groq)
        prompt = f"""
        You are a Cyber Security Expert. Use only the provided context to answer the question.
        If the answer is not in the context, say you don't know.
        
        Context:
        {ev.context_str}
        
        Question: {ev.query}
        
        Answer:"""
        
        # קריאה אסינכרונית ל-Groq
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}]
            }
            response = await client.post(url, headers=headers, json=data)
            
            if response.status_code != 200:
                return StopEvent(result=f"שגיאה בתקשורת עם Groq: {response.text}")
                
            answer = response.json()['choices'][0]['message']['content']
        
        return StopEvent(result=answer)

# הרצה ידנית לבדיקה (טרמינל)
if __name__ == "__main__":
    async def main():
        wf = CyberShieldWorkflow(timeout=60, verbose=True)
        # נסי שאלה קצרה מדי כדי לבדוק ולידציה: "hi"
        # נסי שאלה רגילה: "What is the firewall config?"
        result = await wf.run(query="What is the firewall config?")
        print(f"\n--- Final Output ---\n{result}")

    asyncio.run(main())