import os
from dotenv import load_dotenv
# REPLACE THIS: from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from supabase.client import create_client

load_dotenv()

# 1. Initialize Supabase and API-based Embeddings
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))

# Use the Inference API instead of local model
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    task="feature-extraction",
    huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN")
)

def query_rag(user_question):
    # 2. Convert question to vector via API
    question_vector = embeddings.embed_query(user_question)
    
    # 3. Search Supabase
    response = supabase.rpc("match_documents", {
        "query_embedding": question_vector,
        "match_threshold": 0.5,
        "match_count": 3
    }).execute()
    
    return response.data