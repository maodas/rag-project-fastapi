import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from supabase.client import create_client

# Load the .env file FIRST
load_dotenv() 

print("Starting ingestion process...")

# 1. Load Data
print("Loading FastAPI documentation...")
loader = WebBaseLoader("https://fastapi.tiangolo.com/")
docs = loader.load()
print(f"Loaded {len(docs)} document(s).")

# 2. Split Data
print("Splitting data into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)
print(f"Created {len(chunks)} chunks.")

# 3. Create Embeddings
print("Initializing embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Upload to Supabase
print("Connecting to Supabase...")
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))

print("Starting upload to Supabase...")
for i, chunk in enumerate(chunks):
    vector = embeddings.embed_query(chunk.page_content)
    data = {
        "content": chunk.page_content,
        "embedding": vector,
        "metadata": chunk.metadata
    }
    supabase.table("document_chunks").insert(data).execute()
    if i % 10 == 0:
        print(f"Uploaded {i}/{len(chunks)} chunks...")

print(f"Successfully ingested {len(chunks)} chunks into Supabase!")