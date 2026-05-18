
import os
import warnings
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.embeddings import MockEmbedding # מובנה בתוך הספרייה, לא דורש הורדה!

warnings.filterwarnings('ignore')

def run_pipeline():
    print("🚀 מתחיל הרצה במצב עקיפת חסימות...")
    
    # שלב 1: טעינה
    if not os.path.exists("./data"):
        print("שגיאה: תיקיית data לא קיימת!")
        return
        
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    documents = reader.load_data()

    # שלב 2: פירוק לצ'אנקים
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)
    print(f"✅ נוצרו {len(nodes)} צ'אנקים.")

    # שלב 3: מודל דמה (עוקף את כל בעיות ה-SSL והאינטרנט)
    # זה יוצר וקטורים "מזויפים" רק כדי שהמערכת תעבוד מקומית
    embed_model = MockEmbedding(embed_dim=384)

    print("🔨 בונה אינדקס מקומי...")
    index = VectorStoreIndex(nodes, embed_model=embed_model)
    
    # שלב 4: שמירה למחשב
    index.storage_context.persist(persist_dir="./storage")
    print("\n✅✅✅ הצלחנו!!! ✅✅✅")
    print("האינדקס נשמר בתיקיית storage.")
    print("עכשיו אפשר להפעיל את הצ'אט.")
def get_index():
    # פונקציה שטוענת את האינדקס הקיים מהזיכרון
    if os.path.exists("./storage"):
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        # שימי לב: אם השתמשת ב-MockEmbedding ביצירה, חייבים להשתמש בו גם בטעינה
        return load_index_from_storage(storage_context, embed_model=MockEmbedding(embed_dim=384))
    else:
        # אם אין אינדקס, מריצים את ה-pipeline ליצירה חדשה
        return run_pipeline()

# משתנה גלובלי שיהיה זמין לייבוא
index = get_index()
if __name__ == "__main__":
    run_pipeline()

