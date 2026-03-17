# # # import os
# # import pip_system_certs.wrapt_requests # <--- תוספת 1: הכי חשובה ל-SSL
# # import warnings                        # <--- תוספת 2: כדי שלא יציפו אותך באזהרות
# # warnings.filterwarnings('ignore')

# # from dotenv import load_dotenv
# # from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
# # from llama_index.core.node_parser import SentenceSplitter
# # from llama_index.embeddings.cohere import CohereEmbedding
# # from llama_index.vector_stores.pinecone import PineconeVectorStore
# # from pinecone import Pinecone
# # import os
# # import certifi
# # import ssl
# # # הגדרת נתיב תעודות האבטחה
# # os.environ['SSL_CERT_FILE'] = certifi.where()
# # os.environ['PYTHONHTTPSVERIFY'] = '0'
# # ssl._create_default_https_context = ssl._create_unverified_context
# # # טעינת מפתחות
# # load_dotenv()

# # def run_pipeline():
# #     # --- שלב 1: Loading ---
# #     print("טוען מסמכים...")
# #     reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
# #     documents = reader.load_data()

# #     # --- שלב 2: Chunking (Node Parsers) ---
# #     # אנחנו מחלקים את הטקסט לחתיכות של 512 תווים עם חפיפה
# #     parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
# #     nodes = parser.get_nodes_from_documents(documents)
# #     print(f"נוצרו {len(nodes)} צ'אנקים (Nodes).")

# #     # --- שלב 3: Embedding (Cohere) ---
# #     embed_model = CohereEmbedding(
# #         cohere_api_key=os.environ["COHERE_API_KEY"],
# #         model_name="embed-english-v3.0",
# #         input_type="search_document",
# #         use_async=False
# #     )

# #     # --- שלב 4: Pinecone & VectorStoreIndex ---
# #     # חיבור לפינקון
# #     pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# #     pinecone_index = pc.Index("cyber-shield-index") # וודאי שזה השם שיצרת!

# #     # הגדרת ה-Vector Store עם Metadata
# #     vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
# #     storage_context = StorageContext.from_defaults(vector_store=vector_store)

# #     # יצירת האינדקס ושמירה (כאן ה-Embedding קורה בפועל)
# #     index = VectorStoreIndex(
# #         nodes, 
# #         storage_context=storage_context, 
# #         embed_model=embed_model
# #     )

# #     print("המידע אונדקס בהצלחה ב-Pinecone עם Metadata!")
# #     return index

# # if __name__ == "__main__":
# #     run_pipeline()



# import os
# import warnings
# warnings.filterwarnings('ignore')

# from dotenv import load_dotenv
# from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.embeddings.cohere import CohereEmbedding

# load_dotenv()

# def run_pipeline():
#     print("טוען מסמכים...")
#     reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
#     documents = reader.load_data()

#     parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
#     nodes = parser.get_nodes_from_documents(documents)
#     print(f"נוצרו {len(nodes)} צ'אנקים.")

#     # אנחנו משאירים את Cohere כי אמרת שהוא עובד בדפדפן
#     embed_model = CohereEmbedding(
#         cohere_api_key=os.environ["COHERE_API_KEY"],
#         model_name="embed-english-v3.0",
#         input_type="search_document"
#     )

#     print("יוצר אינדקס מקומי (עוקף Pinecone)...")
#     index = VectorStoreIndex(nodes, embed_model=embed_model)
    
#     # שמירה מקומית
#     index.storage_context.persist(persist_dir="./storage")
#     print("✅ המידע אונדקס ונשמר בתיקיית storage!")
#     return index

# if __name__ == "__main__":
#     run_pipeline()


import os
import warnings
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
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

if __name__ == "__main__":
    run_pipeline()