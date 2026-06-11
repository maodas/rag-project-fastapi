
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse # Import this
from pydantic import BaseModel
from app.chat import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADD THIS: Serve the index.html file when visiting the root URL
@app.get("/")
async def read_index():
    return FileResponse("index.html")

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_bot(query: Query):
    answer = generate_answer(query.question)
    return {"answer": answer}

@app.get("/debug")
async def debug_env():
    return {
        "supabase_url_configured": os.environ.get("SUPABASE_URL") is not None,
        "groq_key_configured": os.environ.get("GROQ_API_KEY") is not None
    }