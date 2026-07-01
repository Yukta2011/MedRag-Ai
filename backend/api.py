from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import ask_rag
from vector_store import collection
import uvicorn


app = FastAPI(title="MedRAG API", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "MedRAG API v2.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "vector_db": "chroma",
        "local_llm": "ollama",
        "cloud_llm": "gemini",
        "router": "phi-detector",
        "documents": collection.count()
    }


@app.get("/ask")
def ask(question: str):
    result = ask_rag(question)
    return result


@app.get("/stats")
def stats():
    return {
        "total_documents": collection.count(),
        "vector_db": "chroma",
        "embedding_model": "all-MiniLM-L6-v2"
    }





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)