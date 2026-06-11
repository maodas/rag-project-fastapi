import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# REPLACE THIS: from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from supabase.client import create_client

load_dotenv()

print("Starting ingestion process...")

# 1. Load Data
loader = WebBaseLoader("https://fastapi.tiangolo.com/")
docs = loader.load()

# 2. Split Data
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# 3. Create Embeddings via API
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    task="feature-extraction",
    huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN")
)

# 4. Upload to Supabase
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))

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