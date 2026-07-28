from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from rag_pipeline import ask_rag
from vector_store import collection


# =====================================================
# FastAPI
# =====================================================

app = FastAPI(
    title="MedRAG AI",
    version="3.0.0",
    description="Privacy-First Medical Research Assistant"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Request Model
# =====================================================

class AskRequest(BaseModel):
    question: str


# =====================================================
# Root
# =====================================================

@app.get("/")
def root():

    return {
        "message": "MedRAG AI Running",
        "version": "3.0.0",
        "docs": "/docs"
    }


# =====================================================
# Health
# =====================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "documents": collection.count(),

        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",

        "vector_database": "ChromaDB"

    }


# =====================================================
# Statistics
# =====================================================

@app.get("/stats")
def stats():

    return {

        "documents": collection.count(),

        "database": "ChromaDB",

        "embedding_model": "all-MiniLM-L6-v2"

    }


# =====================================================
# GET ASK
# =====================================================

@app.get("/ask")
def ask(question: str):

    result = ask_rag(question)

    return result


# =====================================================
# POST ASK
# =====================================================

@app.post("/ask")
def ask_post(request: AskRequest):

    result = ask_rag(request.question)

    return result


# =====================================================
# Debug Routes
# =====================================================

print("\n================ ROUTES ================\n")

for route in app.routes:
    methods = ",".join(route.methods)
    print(f"{methods:20} {route.path}")

print("\n========================================\n")


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )