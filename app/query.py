import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from supabase.client import create_client

load_dotenv()

# 1. Initialize Supabase and Embeddings
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def query_rag(user_question):
    # 2. Convert question to vector
    question_vector = embeddings.embed_query(user_question)
    
    # 3. Search Supabase for the most similar chunk
    # 'match_documents' is the RPC function we will create next
    response = supabase.rpc("match_documents", {
        "query_embedding": question_vector,
        "match_threshold": 0.5,
        "match_count": 3
    }).execute()
    
    return response.data

# Test the query
question = "How do I create a FastAPI path operation?"
results = query_rag(question)

for res in results:
    print(f"Match Found: {res['content'][:200]}...")