# ⚕️ MedRAG AI
### Hybrid Retrieval-Augmented Medical Research Assistant

MedRAG AI is a production-ready Retrieval-Augmented Generation (RAG) system that answers medical research questions using trusted biomedical literature from PubMed Central (PMC).

Unlike a general-purpose chatbot, MedRAG AI retrieves relevant research papers first and then generates grounded responses using either Google Gemini or a local Mistral model running through Ollama.

---

## Features

- Retrieval-Augmented Generation (RAG)
- Semantic search using ChromaDB
- Evidence-based answers with citations
- Google Gemini integration
- Local Mistral (Ollama) support
- Automatic cloud → local fallback
- PHI-aware routing
- Research paper metadata
  - Title
  - Authors
  - Journal
  - Publication Year
  - PMC Link
- Modern React frontend
- Animated medical dashboard
- Glassmorphism UI
- Interactive research paper cards

---

# System Architecture

```
                        User
                          │
                          ▼
                  React Frontend
                          │
                          ▼
                    FastAPI Backend
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     Router          Retriever          API Layer
        │                 │
        │          Chroma Vector DB
        │                 │
        │                 ▼
        │        Top-k Research Papers
        │
        ▼
   Local / Cloud Decision
        │
 ┌──────┴─────────┐
 ▼                ▼
Gemini        Ollama Mistral
        │
        ▼
 Final Answer + Citations
```

---

# Tech Stack

## Frontend

- React
- Vite
- CSS
- Glassmorphism UI

## Backend

- FastAPI
- Python
- Uvicorn

## AI Models

- Google Gemini
- Ollama
- Mistral

## Vector Database

- ChromaDB

## Embeddings

- sentence-transformers
- all-MiniLM-L6-v2

## Data Sources

- PubMed Central
- PubMed

---

# Folder Structure

```
MedicalResearchAssistant-rag-v2
│
├── backend
│   ├── api.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── router.py
│   ├── local_llm.py
│   ├── cloud_llm.py
│   ├── vector_store.py
│   ├── embedder.py
│   ├── process_pmc.py
│   ├── pmc_loader.py
│   ├── pubmed_loader.py
│   ├── evaluate_rag.py
│   ├── test_dataset.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
├── vectorstore
│
└── README.md
```

---

# Retrieval Pipeline

```
User Question
      │
      ▼
Generate Embedding
      │
      ▼
ChromaDB Similarity Search
      │
      ▼
Retrieve Top-k Chunks
      │
      ▼
Similarity Filtering
      │
      ▼
Prompt Construction
      │
      ▼
Route Decision
      │
 ┌────┴────┐
 ▼         ▼
Gemini   Ollama
      │
      ▼
Evidence-based Response
```

---

# Intelligent Routing

The system automatically selects the appropriate model.

### Cloud

General medical research questions

Example

```
What is diabetes?
```

↓

Google Gemini

---

### Local

Sensitive or PHI-related prompts

Example

```
Patient John Doe has diabetes...
```

↓

Ollama Mistral

---

### Automatic Fallback

If Gemini is unavailable

↓

Automatically switches to

↓

Local Mistral

without interrupting the user.

---

# Retrieval Improvements

The retriever performs:

- semantic similarity search
- keyword matching
- metadata filtering
- similarity threshold filtering
- duplicate paper removal
- paper ranking

This prevents unrelated papers from appearing in responses.

---

# Research Metadata

Every retrieved paper contains

- Title
- Authors
- Journal
- Publication Year
- PMC ID
- Direct PMC URL
- Similarity Score

---

# Evaluation Pipeline

The project includes an evaluation framework.

Metrics include

- Retrieval Accuracy
- Precision@K
- Recall@K
- Response Time
- Model Used
- Retrieval Success
- Citation Quality

Output files

```
evaluation_report.csv

evaluation_results.json
```

Run

```bash
python evaluate_rag.py
```

---

# Frontend

Modern medical dashboard featuring

- video background
- animated particles
- HUD overlays
- search interface
- research paper cards
- responsive design
- route badges
- retrieval indicators

---

# Installation

## Clone

```bash
git clone https://github.com/Yukta2011/MedRag-Ai.git

cd MedRag-Ai
```

---

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## Environment Variables

Create

```
.env
```

```
GEMINI_API_KEY=YOUR_API_KEY
NCBI_EMAIL=your_email@example.com
```

---

## Install Ollama

```
ollama pull mistral
```

Start

```
ollama serve
```

---

## Build Vector Database

```bash
python process_pmc.py
```

---

## Run Backend

```bash
uvicorn api:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Example API

```
GET

/ask?question=What is diabetes?
```

Example Response

```json
{
  "answer": "...",
  "route": "cloud",
  "model_used": "Gemini",
  "retrieval": true,
  "chunks_retrieved": 5,
  "fallback": false,
  "sources": [
    {
      "title": "...",
      "authors": "...",
      "journal": "...",
      "year": "2026",
      "pmc_id": "...",
      "url": "..."
    }
  ]
}
```

---

# Performance

| Metric | Value |
|---------|-------|
| Research Papers | 500+ |
| Text Chunks | 27,000+ |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Retrieval | Top-5 |
| Local LLM | Mistral |
| Cloud LLM | Gemini |
| Automatic Fallback | Yes |

---

# Future Improvements

- PDF upload
- Clinical report analysis
- Voice input
- Medical image support
- Multi-language interface
- Doctor dashboard
- Authentication
- User history
- Personalized recommendations
- Docker deployment

---

# License

MIT License

---

# Author

**Yukta Walanju**

B.Tech Computer Science (AI)

Medical AI • Machine Learning • Retrieval-Augmented Generation • Healthcare AI

