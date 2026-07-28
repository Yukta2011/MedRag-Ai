# MedRAG-AI

## Privacy-Aware Medical Research Assistant using Hybrid Retrieval-Augmented Generation

MedRAG-AI is an AI-powered medical research assistant designed to provide evidence-based medical information by combining Retrieval-Augmented Generation (RAG), Large Language Models, semantic search, and biomedical research databases.

The system retrieves relevant medical literature from PubMed and PMC Open Access research articles, processes the information using a vector search pipeline, and generates grounded responses using a hybrid LLM architecture.

The platform combines:

* Retrieval-Augmented Generation for evidence-based responses
* ChromaDB vector search for semantic retrieval
* Sentence Transformer embeddings for medical document understanding
* Ollama-based local LLM inference for privacy-sensitive queries
* Google Gemini for general medical research reasoning
* React-based interactive frontend
* FastAPI backend API architecture

---

# System Architecture Overview

```
                         User
                          |
                          |
                          v

                 React Frontend
                          |
                          |
                    REST API Request
                          |
                          v

                 FastAPI Backend

                          |
        ---------------------------------
        |                               |
        v                               v

  Privacy Router                 RAG Pipeline

        |                               |
        |                               |
        v                               v

 Local Ollama LLM              Document Retriever

        |                               |
        |                               v

        |                         ChromaDB Vector Store

        |                               |
        |                               v

        |                      Medical Research Context

        |                               |
        ---------------------------------

                          |
                          v

                  Response Generator

                          |
                          v

                  React User Interface
```

---

# Technology Stack

## Frontend Technologies

| Technology | Purpose                                     |
| ---------- | ------------------------------------------- |
| React.js   | Component-based user interface development  |
| Vite       | Fast frontend development and build tooling |
| JavaScript | Frontend logic implementation               |
| CSS3       | UI design and responsive styling            |
| Fetch API  | Communication with backend APIs             |

---

## Backend Technologies

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Core backend development            |
| FastAPI    | High-performance REST API framework |
| Uvicorn    | ASGI server for running FastAPI     |
| SQLAlchemy | Database ORM layer                  |
| Pydantic   | Data validation and API schemas     |

---

## Artificial Intelligence Stack

| Technology                           | Purpose                                          |
| ------------------------------------ | ------------------------------------------------ |
| Retrieval-Augmented Generation (RAG) | Grounding LLM responses using research documents |
| Sentence Transformers                | Generating semantic embeddings                   |
| ChromaDB                             | Vector database for similarity search            |
| Ollama                               | Local LLM inference                              |
| Mistral                              | Local language model                             |
| Google Gemini API                    | Cloud-based reasoning model                      |
| LangChain concepts                   | Prompting and retrieval workflow design          |

---

## Medical Data Sources

| Source          | Purpose                           |
| --------------- | --------------------------------- |
| PubMed          | Biomedical research articles      |
| PMC Open Access | Full-text scientific publications |
| NCBI APIs       | Research paper retrieval          |

---

# Frontend Architecture

The frontend is developed using React.js and provides an interactive interface for users to communicate with the medical AI assistant.

## Frontend Responsibilities

The frontend handles:

* User query input
* API communication
* Loading states
* AI response rendering
* Research paper citation display
* Model information display
* UI animations and styling

## Frontend Structure

```
frontend

|
├── src
│
├── App.jsx
│      Main React application component
│
├── App.css
│      Application styling
│
├── public
│      Static assets
│
├── package.json
│      Frontend dependencies
│
└── vite.config.js
       Vite configuration
```

---

# Frontend Request Flow

Example:

User asks:

```
What are the symptoms of diabetes?
```

Flow:

```
User Input

     |
     v

React Component
(App.jsx)

     |
     v

API Request

     |
     v

FastAPI Backend

     |
     v

Response Received

     |
     v

UI Updates

     |
     v

Answer + Research Sources Displayed
```

---

# Backend Architecture

The backend manages:

* API handling
* Query processing
* Research retrieval
* LLM routing
* Prompt generation
* Response generation

Backend structure:

```
backend

|
├── app.py
│     FastAPI application entry point
│
├── rag_pipeline.py
│     Complete RAG execution workflow
│
├── retriever.py
│     Searches relevant medical documents
│
├── vector_store.py
│     ChromaDB interaction layer
│
├── embedder.py
│     Creates document embeddings
│
├── chunker.py
│     Splits documents into smaller sections
│
├── pmc_loader.py
│     Loads PMC research papers
│
├── pubmed_loader.py
│     Loads PubMed research papers
│
├── router.py
│     Determines local/cloud model usage
│
├── local_llm.py
│     Ollama integration
│
├── cloud_llm.py
│     Gemini integration
│
├── build_index.py
│     Creates vector database index
│
├── build_rag_prompt.py
│     Creates evidence-based prompts
│
└── build_general_prompt.py
      Creates general medical prompts
```

---

# Backend Request Processing Flow

When a user submits a question:

## Step 1: API Request

Frontend sends:

```
POST /ask
```

with:

```json
{
 "question":"What is hypertension?"
}
```

---

## Step 2: Query Routing

The router analyzes the question.

It checks for:

* Patient information
* Medical records
* Personal identifiers
* Sensitive health information

Decision:

```
                 Question

                    |

              Privacy Router

              /            \

        Sensitive          General

            |                 |

            v                 v

        Ollama             Gemini
```

---

# RAG Pipeline Workflow

## Step 1: Query Processing

The user's question is converted into a searchable representation.

Example:

```
"What causes kidney disease?"
```

becomes a semantic embedding.

---

## Step 2: Vector Retrieval

The retriever searches ChromaDB.

Process:

```
Question

   |

Embedding Generation

   |

Similarity Search

   |

Top Relevant Research Chunks
```

The system retrieves:

* Research content
* Paper metadata
* Authors
* Journal
* Year
* PMC ID

---

## Step 3: Context Creation

Retrieved documents are combined into a context.

Example:

```
Medical Research Context:

Paper 1:
Kidney disease risk factors...

Paper 2:
Clinical outcomes...
```

---

## Step 4: Prompt Generation

The system creates an evidence-based prompt:

```
Answer using only the provided medical research.

Do not create unsupported findings.

Provide a clear medical explanation.
```

---

## Step 5: LLM Response Generation

The selected model generates the final answer.

Output contains:

* Medical explanation
* Supporting research papers
* Citations
* Model information

---

# Research Document Processing Pipeline

Before answering queries, medical literature is indexed.

```
PubMed / PMC Papers

        |

        v

Document Loader

        |

        v

Text Cleaning

        |

        v

Chunk Generation

        |

        v

Embedding Creation

        |

        v

ChromaDB Storage
```

---

# Database and Vector Storage

ChromaDB stores:

```
Vector Database

|
├── Document Embeddings
|
├── Research Text Chunks
|
└── Metadata

      |
      ├── Title
      ├── Authors
      ├── Journal
      ├── Year
      └── PMC ID
```

---

# Local and Cloud LLM Architecture

## Local Model

Technology:

```
Ollama + Mistral
```

Used for:

* Privacy-sensitive queries
* Offline processing
* Local inference

Advantages:

* Data remains locally processed
* No external API transmission

---

## Cloud Model

Technology:

```
Google Gemini API
```

Used for:

* General medical questions
* Complex reasoning
* Research explanations

---

# Automatic Fallback Mechanism

If Gemini fails:

```
Gemini Request

      |

 API Failure?

      |

      v

Ollama Local Model

      |

      v

Generated Response
```

---

# Running the Project

## Backend Setup

Create environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run backend:

```bash
cd backend

uvicorn app:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

Install dependencies:

```bash
cd frontend

npm install
```

Run:

```bash
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# Building Research Index

To generate the vector database:

```bash
cd backend

python build_index.py
```

This performs:

1. Research paper loading
2. Text extraction
3. Chunk generation
4. Embedding creation
5. Vector database storage

---

# Key Features

* Medical research question answering
* Evidence-grounded responses
* PubMed and PMC integration
* Hybrid LLM architecture
* Privacy-aware routing
* Local AI inference
* Semantic document retrieval
* Research paper citations
* React-based interface
* FastAPI backend
* ChromaDB vector search

---

