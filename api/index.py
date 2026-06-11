import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.chat import generate_answer
from fastapi.middleware.cors import CORSMiddleware

# Initialize the app once
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ask") # Match this with your frontend fetch
async def ask_bot(query: Query):
    answer = generate_answer(query.question)
    return {"answer": answer}