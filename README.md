# FastAPI AI Documentation Assistant

A robust, serverless Retrieval-Augmented Generation (RAG) chatbot that provides technical answers by querying official FastAPI documentation. 

## 🚀 Live Demo
[https://rag-project-fastapi.vercel.app/](https://rag-project-fastapi.vercel.app/)

## 🏗️ Technical Architecture
This project implements a complete RAG pipeline to ensure accuracy and reduce LLM hallucinations.
- **Frontend:** Responsive HTML/JavaScript interface with modern CSS.
- **Backend:** FastAPI (Python), deployed serverless on Vercel.
- **Orchestration:** LangChain for document splitting, embedding, and prompt management.
- **Database:** Supabase (PostgreSQL with `pgvector`) for storing and querying document embeddings.
- **AI/LLM:** Llama-3 (via Groq API) for high-speed, cost-efficient inference.
- **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers) for semantic vector representation.

## ⚙️ How it Works
1. **Ingestion:** The system crawls FastAPI documentation, splits text into meaningful chunks, and embeds them into a vector space.
2. **Retrieval:** When a user asks a question, the system converts the query to a vector and finds the most semantically similar text chunks in Supabase using cosine similarity.
3. **Generation:** Retrieved context is injected into a prompt, and Llama-3 generates a precise answer based on that context.

## 🛠️ Tech Stack & Skills Demonstrated
- **Data Engineering:** Recursive character text splitting and vector embedding workflows.
- **Infrastructure:** Version-controlled database schema and serverless API deployment.
- **Security:** Implementation of Row-Level Security (RLS) and environment variable management (secrets).
- **Frontend/Backend Integration:** Handling asynchronous API communication and UI/UX state management.