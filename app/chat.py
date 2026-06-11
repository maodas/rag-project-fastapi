import os
from groq import Groq
from app.query import query_rag # Import your retrieval logic

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_answer(user_question):
    # 1. Retrieve relevant docs
    docs = query_rag(user_question)
    context = "\n".join([d['content'] for d in docs])
    
    # 2. Build Prompt
    prompt = f"Use the following context to answer the question: {context}\n\nQuestion: {user_question}"
    
    # 3. Call LLM
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content