import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.chat import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/api/ask")
async def ask_bot(query: Query):
    try:
        answer = generate_answer(query.question)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

@app.get("/api/debug")
async def debug_env():
    return {
        "supabase_url": os.environ.get("SUPABASE_URL") is not None,
        "groq_key": os.environ.get("GROQ_API_KEY") is not None,
        "hf_token": os.environ.get("HUGGINGFACEHUB_API_TOKEN") is not None
    }