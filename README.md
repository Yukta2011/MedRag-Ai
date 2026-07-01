<<<<<<< HEAD
# MedRag-Ai
Medical Research Assistant instead of relying on a general-purpose chatbot, the system retrieves evidence directly from trusted medical sources such as PubMed and PMC Open Access articles and uses Retrieval-Augmented Generation (RAG) to generate grounded responses.
=======
⚕️ MedRAG AI — Hybrid Medical Research Assistant
A production-grade RAG system with intelligent local/cloud LLM routing, PHI-safe architecture, and a cinematic React frontend.
https://python.org
https://fastapi.tiangolo.com
https://react.dev
https://www.trychroma.com
LICENSE
<img src="https://raw.githubusercontent.com/Yukta2011/MedRag-Ai/main/assets/demo.gif" width="800" alt="MedRAG Demo">
</div>

What It Does?
MedRAG AI answers medical research questions by retrieving relevant papers from PubMed Central (PMC) and PubMed, then generating cited responses using a dual-LLM architecture:

| Query Type                                      | Route                | Model              | Why                                   |
| ----------------------------------------------- | -------------------- | ------------------ | ------------------------------------- |
| General research (e.g., "What is diabetes?")    | **Cloud**            | Google Gemini 3.5  | Best reasoning, comprehensive answers |
| PHI/sensitive (e.g., "Patient John Doe has...") | **Local**            | Mistral via Ollama | **Zero data leaves the machine**      |
| Cloud unavailable (503 error)                   | **Auto-Fallback**    | Local Mistral      | 100% uptime guarantee                 |

Architecture:

┌─────────────────────────────────────────────────────────────────┐
│                         REACT FRONTEND                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │ Glowing 3D  │  │  Search UI  │  │   HUD Overlays      │     │
│  │ Heart Video │  │  + Results  │  │  (bpm, O2, pH...)   │     │
│  │ Background  │  │             │  │                     │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP /ask?question=...
┌────────────────────────▼────────────────────────────────────────┐
│                      FASTAPI BACKEND  :8000                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │   /ask      │  │  /health    │  │      /stats         │     │
│  │  RAG Endpoint│  │  System Status│  │  Vector DB Stats  │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ ROUTER  │    │ RETRIEVER│    │  LOCAL   │
    │(PHI Det)│    │(ChromaDB)│    │  LLM     │
    │         │    │          │    │(Mistral) │
    │ Regex + │    │ Cosine   │    │ Ollama   │
    │ Keyword │    │ Similarity│   │ :11434   │
    └────┬────┘    └────┬─────┘    └────┬─────┘
         │              │               │
         └──────────────┼───────────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
    ┌──────────┐                 ┌──────────┐
    │  CLOUD   │◄────503?──────►│ FALLBACK │
    │ (Gemini) │   Auto-switch   │ (Local)  │
    └──────────┘                 └──────────┘

*Key Technical Decisions
1. Hybrid LLM Routing (Privacy by Design)

Python
# router.py — PHI detection with regex patterns
def route_question(question):
    phi_patterns = [
        r'\bpatient\b', r'\bname\b', r'\bssn\b',
        r'\bdate of birth\b', r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
    ]
    for pattern in phi_patterns:
        if re.search(pattern, question.lower()):
            return "local"   # Never leaves machine
    return "cloud"           #  Use Gemini


2. Graceful Cloud Degradation

Python
# rag_pipeline.py — Auto-fallback on any cloud failure
answer = ask_cloud_model(prompt)
if "Error" in answer or "UNAVAILABLE" in answer or "503" in answer:
    print("  Cloud failed...  Falling back to local Mistral...")
    answer = ask_local_model(prompt)
    model_used = "local (Mistral) [cloud fallback]"

3. Production-Ready Metadata Extraction
Parsed journal name, year, and authors from PMC XML (not just raw text):

Python
# pmc_loader.py — Full XML metadata parsing
{
    "pmc_id": "13289534",
    "title": "Are surgical nurses ready for AI?",
    "authors": ["Ömer Taşçı", "İlknaz Kara", "Barış Özdere"],
    "journal": "BMC Nursing",
    "year": "2026",
    "text": "..."
}


4. Citation-First RAG
Every answer includes formatted sources:

[1] Diabetic gastroparesis: pathophysiology... | Galeano, Tumminia, Oteri | Endocrine (2026) | PMC:13290835
Tech Stack
| Layer           | Technology                         | Purpose                           |
| --------------- | ---------------------------------- | --------------------------------- |
| **Backend**     | FastAPI + Uvicorn                  | High-performance async API        |
| **Vector DB**   | ChromaDB + `all-MiniLM-L6-v2`      | Semantic search over 27K+ chunks  |
| **Embeddings**  | SentenceTransformers               | 384-dim dense vectors             |
| **Chunking**    | Custom overlap + sentence boundary | 500-char chunks, 100-char overlap |
| **Local LLM**   | Ollama + Mistral 7B                | On-premise inference              |
| **Cloud LLM**   | Google Gemini 3.5 Flash            | Advanced reasoning                |
| **Data Source** | NCBI E-utilities (PMC + PubMed)    | 500 real medical papers           |
| **Frontend**    | React 18 + Vite + Pure CSS         | No bloat, full control            |
| **Effects**     | Canvas 2D + CSS animations         | HUD grid, scan lines, particles   |
| **Video BG**    | MP4 heart animation                | Medical cinematic feel            |

 Performance
| Metric              | Value                                   |
| ------------------- | --------------------------------------- |
| Total Documents     | 500 PMC articles                        |
| Total Chunks        | ~27,000                                 |
| Embedding Model     | `all-MiniLM-L6-v2` (384-dim)            |
| Retrieval Time      | <100ms                                  |
| Local LLM Timeout   | 300s (slow hardware tolerant)           |
| Cloud Fallback      | <1s switchover                          |
| API Response Format | JSON with citations, route, model\_used |

 * Quick Start
Prerequisites
Python 3.11+
Node.js 18+
Ollama installed (ollama.ai)
Google Gemini API key


1. Clone & Setup Backend
bash
git clone https://github.com/Yukta2011/MedRag-Ai.git
cd MedRag-Ai/backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirement.txt


2. Configure Environment
bash
# Edit .env
GEMINI_API_KEY=your_key_here
NCBI_EMAIL=your_email@example.com


3. Build Vector Database
bash
ollama pull mistral
ollama serve                    # Terminal 1
python process_pmc.py           # Terminal 2 (builds ChromaDB)


4. Start API
bash
python api.py                   # localhost:8000


5. Start Frontend
bash
cd ../frontend
npm install
npm run dev                     # localhost:5173


API Endpoints
| Endpoint                | Method | Description                                                  |
| ----------------------- | ------ | ------------------------------------------------------------ |
| `GET /ask?question=...` | Query  | Main RAG endpoint. Returns answer + citations + routing info |
| `GET /health`           | —      | System status: vector DB, LLMs, router health                |
| `GET /stats`            | —      | Document count, embedding model info                         |


Sample Response
JSON
{
  "answer": "Diabetes mellitus is a metabolic disorder characterized by hyperglycemia...",
  "sources": [
    "[1] Diabetic gastroparesis... | Galeano, Tumminia, Oteri | Endocrine (2026) | PMC:13290835",
    "[2] Diabetic impact on the neuroaxis... | Okdahl, Brock | Frontiers in Endocrinology (2026) | PMC:13290679"
  ],
  "route": "cloud",
  "model_used": "cloud (Gemini)",
  "chunks_retrieved": 5
}

 *Frontend Features
Full-screen glowing anatomical heart video background
CRT-style HUD: grid lines, scanning line animation, floating particles
Real-time medical vitals display (bpm, mmHg, O2 Sat, pH, Temp)
Glassmorphism UI: translucent panels with backdrop blur
Route indicator badges: Local AI (Privacy) /  Cloud AI (Gemini)
Animated citations with PMC links
Sign Up / Login modals with gradient styling
Fully responsive (mobile hides HUD, stacks layout)


*Security & Privacy
| Feature            | Implementation                       |
| ------------------ | ------------------------------------ |
| PHI Detection      | Regex + keyword matching on query    |
| Local Processing   | Ollama runs entirely offline         |
| No Data Logging    | Cloud only sees non-PHI prompts      |
| API Key Protection | Stored in `.env`, never committed    |
| CORS               | Configured for localhost development |

* Project Structure
plain
MedicalResearchAssistant-rag-v2/
├── backend/
│   ├── api.py              # FastAPI app with CORS
│   ├── rag_pipeline.py     # Orchestrator: retrieve → route → generate → fallback
│   ├── router.py           # PHI detection engine
│   ├── retriever.py        # ChromaDB semantic search
│   ├── vector_store.py     # Collection management + add_chunks
│   ├── embedder.py         # SentenceTransformer wrapper
│   ├── chunker.py          # Overlapping text segmentation
│   ├── pmc_loader.py       # NCBI E-utilities XML parser (metadata + text)
│   ├── pubmed_loader.py    # PubMed abstract fetcher
│   ├── process_pmc.py      # ETL: load → chunk → embed → store
│   ├── local_llm.py        # Ollama/Mistral client (300s timeout)
│   ├── cloud_llm.py        # Gemini 3.5 with multi-model fallback
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React app: video BG, search, HUD, modals
│   │   ├── App.css         # Pure CSS: animations, glassmorphism, responsive
│   │   └── main.jsx        # React 18 entry point
│   ├── public/
│   │   └── heart-bg.mp4    # Glowing anatomical heart video
│   ├── index.html
│   ├── package.json
│   └── vite.config.js      # Proxy to localhost:8000
├── .env                    # API keys (gitignored in production)
└── vectorstore/            # ChromaDB persistent data

 *Testing
bash
# Backend
python rag_pipeline.py          # CLI interactive mode
python -c "from pmc_loader import get_article_text; print(get_article_text('13289534'))"
curl "http://localhost:8000/ask?question=What%20is%20diabetes?"

# Frontend
# Open http://localhost:5173
# Try: "What is artificial intelligence in healthcare?" → Cloud
# Try: "Patient John Doe has diabetes symptoms" → Local

 Challenges Solved

| Challenge                         | Solution                                                             |
| --------------------------------- | ------------------------------------------------------------- |
| Gemini 503 errors                 | Auto-fallback to local Mistral with user notification                |
| Slow local LLM (120s timeout)     | Increased to 300s; added phi3/tinyllama recommendation               |
| Missing journal/year in citations | Rewrote PMC XML parser to extract `<journal-title>` and `<pub-date>` |
| PowerShell file encoding issues   | Used Notepad for manual file creation to avoid UTF-8 corruption      |
| Nested frontend folder            | Clean recreation with proper Vite structure                          |
| Video background performance      | `object-fit: cover` + hardware-accelerated CSS animations            |

Future Roadmap:
[ ] Docker Compose for one-command deployment
[ ] WebSocket streaming for real-time LLM responses
[ ] Multi-language support (PubMed abstracts in 10+ languages)
[ ] PDF upload for private document RAG
[ ] Fine-tuned BioMistral for medical domain accuracy
[ ] Three.js 3D heart model (procedural geometry + heartbeat animation)

Yukta Walanju — Built as a capstone project demonstrating full-stack ML engineering, from data pipelines to production APIs to cinematic UIs.
<div align="center">
⭐ Star this repo if you found it useful!
</div>
>>>>>>> ebdf43d989e00cf1a9ee7ed7d4fd5d8eb4b1b942
https://medrag-ai-1.onrender.com/
