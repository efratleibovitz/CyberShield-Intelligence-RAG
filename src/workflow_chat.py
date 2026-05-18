import os
import json
import asyncio
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Context, Event
from llama_index.llms.groq import Groq
from dotenv import load_dotenv

load_dotenv()

# הגדרת אירועים
class RouteEvent(Event):
    route: str  # "structured" or "semantic"
    query: str

class RetrievalEvent(Event):
    context_str: str
    query: str
    search_iteration: int = 1

class ValidationEvent(Event):
    context_str: str
    query: str
    is_valid: bool

class StatusEvent(Event):
    msg: str

# --- ה-Workflow המשודרג ---
class CyberShieldWorkflow(Workflow):
    llm = Groq(model="llama-3.3-70b-versatile")

    def __init__(self, index=None, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.llm = Groq(model="llama-3.3-70b-versatile")

    @step
    async def router(self, ctx: Context, ev: StartEvent) -> RouteEvent | StopEvent:
        query = ev.get("query")
        if not query:
            return StopEvent(result="אנא ספק שאלה תקינה.")

        ctx.write_event_to_stream(StatusEvent(msg="🤖 מנתח את סוג השאלה (Routing)..."))

        # שימוש ב-LLM כדי להחליט על הניתוב בצורה חכמה
        router_prompt = f"""
        Analyze the user query: "{query}"
        Is this a request for a list, multiple rules, all decisions, or structured summaries? 
        If yes, answer 'structured'. 
        If it's a general question or needs explanation, answer 'semantic'.
        Answer ONLY with one word.
        """
        response = await self.llm.acomplete(router_prompt)
        route = response.text.strip().lower()

        # גיבוי למקרה שה-LLM לא ענה בדיוק
        if "structured" not in route and "semantic" not in route:
            route = "semantic"

        return RouteEvent(route=route, query=query)

    @step
    async def handle_structured(self, ctx: Context, ev: RouteEvent) -> StopEvent | RetrievalEvent:
        if ev.route != "structured":
            # אם זה לא מובנה, שלחי לאירוע השליפה הרגיל (שלב ב')
            return RetrievalEvent(context_str="", query=ev.query)
            
        ctx.write_event_to_stream(StatusEvent(msg="📊 שולף נתונים מובנים מ-Knowledge Base..."))
        
        try:
            with open("knowledge_base.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return StopEvent(result="שגיאה: קובץ הנתונים המובנים לא נמצא. אנא הריצי את ה-Extractor.")

        # יצירת תשובה מבוססת JSON
        prompt = f"""
        You are a Cyber Security Expert. Based on this structured JSON data, 
        provide a detailed and organized answer to the question.
        Use bullet points for lists.
        
        Data: {json.dumps(data, indent=2, ensure_ascii=False)}
        Question: {ev.query}
        """
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=response.text)

    
    @step
    async def ingest_and_retrieve(self, ctx: Context, ev: RetrievalEvent) -> RetrievalEvent | StopEvent:
        if ev.context_str:
            return ev
        
        ctx.write_event_to_stream(StatusEvent(msg="🔍 מחפש במאגר המידע הסמנטי..."))
        
        # שימוש באינדקס שקיבלנו ב-init
        retriever = self.index.as_retriever(similarity_top_k=3 if ev.search_iteration == 1 else 6)
        nodes = retriever.retrieve(ev.query)
        context_str = "\n".join([n.node.get_content() for n in nodes])
        
        return RetrievalEvent(context_str=context_str, query=ev.query, search_iteration=ev.search_iteration)
   
    @step
    async def validate_context(self, ctx: Context, ev: RetrievalEvent) -> ValidationEvent | RetrievalEvent:
        # (הקוד של הולידציה שבנינו קודם...)
        context_len = len(ev.context_str.strip())
        if context_len < 150 and ev.search_iteration == 1:
            return RetrievalEvent(context_str="", query=ev.query, search_iteration=2) # ניסיון חוזר עם top_k גדול יותר
            
        is_valid = context_len > 50
        return ValidationEvent(context_str=ev.context_str, query=ev.query, is_valid=is_valid)

    @step
    async def generate_answer(self, ctx: Context, ev: ValidationEvent) -> StopEvent:
        if not ev.is_valid:
            return StopEvent(result="מצטער, לא מצאתי מספיק מידע רלוונטי בתיעוד.")
            
        ctx.write_event_to_stream(StatusEvent(msg="✍️ מנסח תשובה סופית..."))
        prompt = f"Context: {ev.context_str}\n\nQuestion: {ev.query}\nAnswer:"
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=response.text)