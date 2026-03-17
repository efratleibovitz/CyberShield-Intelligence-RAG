import os
import json
import glob
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.groq import Groq
from schema import ProjectKnowledge
import os
from dotenv import load_dotenv

load_dotenv()
# הגדרת המודל
llm = Groq(
    model="llama-3.3-70b-versatile", 
    api_key=os.environ.get("GROQ_API_KEY")
)
prompt_template_str = """
Analyze the following documentation and extract ALL technical decisions, rules, and warnings.
Return the data in a structured format.

Documentation:
{context_str}
"""

def run_extraction():
    # 1. איסוף כל הטקסט מכל קבצי ה-md בתיקיות data
    all_content = ""
    files = glob.glob("data/**/*.md", recursive=True)
    
    print(f"📂 Found {len(files)} files to scan...")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_content += f"\n--- Source: {file_path} ---\n"
            all_content += f.read()

    # 2. הגדרת התוכנית לחילוץ מובנה
    program = LLMTextCompletionProgram.from_defaults(
        output_cls=ProjectKnowledge,
        prompt_template_str=prompt_template_str,
        llm=llm,
        verbose=True
    )

    # 3. הרצה וחילוץ
    print("🧠 Extracting structured data via Groq... please wait.")
    structured_data = program(context_str=all_content)

    # 4. שמירה לקובץ JSON
    output_path = "knowledge_base.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data.dict(), f, indent=4, ensure_ascii=False)
    
    print(f"✅ Success! Created {output_path}")

if __name__ == "__main__":
    run_extraction()