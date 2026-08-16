# MedRAG-AI

## Privacy-Aware Medical Research Assistant using Hybrid Retrieval-Augmented Generation

MedRAG-AI is an AI-powered medical research assistant designed to provide evidence-based medical information by combining:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Semantic Search
- Biomedical Research Databases
- Privacy-aware AI routing

The system retrieves relevant medical literature from **PubMed** and **PMC Open Access research articles**, processes the information through a vector search pipeline, and generates grounded responses using a hybrid LLM architecture.

The platform combines:

- Retrieval-Augmented Generation for evidence-based responses
- ChromaDB vector search for semantic retrieval
- Sentence Transformer embeddings for medical document understanding
- Ollama-based local LLM inference for privacy-sensitive queries
- Google Gemini for general medical reasoning
- React-based interactive frontend
- FastAPI backend API architecture
<img width="1893" height="844" alt="image" src="https://github.com/user-attachments/assets/ec793934-dd46-428d-81c6-1d1694e93d79" />


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

                                        |
                                        v

                              ChromaDB Vector Store

                                        |
                                        v

                              Medical Research Context

        |                               |
        ---------------------------------

                          |
                          v

                  Response Generator

                          |
                          v

                  React User Interface
```


# Technology Stack


## Frontend Technologies

| Technology | Purpose |
|------------|---------|
| React.js | Component-based user interface development |
| Vite | Fast frontend development and build tooling |
| JavaScript | Frontend logic implementation |
| CSS3 | UI design and responsive styling |
| Fetch API | Backend API communication |


## Backend Technologies

| Technology | Purpose |
|------------|---------|
| Python | Core backend development |
| FastAPI | High-performance REST API framework |
| Uvicorn | ASGI server |
| SQLAlchemy | Database ORM layer |
| Pydantic | API data validation |


## Artificial Intelligence Stack

| Technology | Purpose |
|------------|---------|
| Retrieval-Augmented Generation (RAG) | Grounding LLM responses using research documents |
| Sentence Transformers | Generating semantic embeddings |
| ChromaDB | Vector database for similarity search |
| Ollama | Local LLM inference |
| Mistral | Local language model |
| Google Gemini API | Cloud-based reasoning model |
| LangChain Concepts | Retrieval and prompting workflow design |


# Medical Data Sources

| Source | Purpose |
|--------|---------|
| PubMed | Biomedical research articles |
| PMC Open Access | Full-text scientific publications |
| NCBI APIs | Research paper retrieval |


# Environment Requirements


## Python Version

MedRAG-AI is developed and tested using:

```
Python 3.11.9
```

Python 3.11 is recommended because AI and scientific computing libraries provide better compatibility with this version.

Used libraries include:

- ChromaDB
- Sentence Transformers
- NumPy
- Pandas
- PyTorch-based dependencies


## Required Software

| Software | Version |
|----------|---------|
| Python | 3.11.9 |
| Node.js | 18+ |
| npm | 9+ |
| Ollama | Latest |
| Git | Latest |


# Frontend Architecture

The frontend is developed using React.js and provides an interactive interface for communicating with the medical AI assistant.


## Frontend Responsibilities

The frontend handles:

- User query input
- API communication
- Loading states
- AI response rendering
- Research paper citation display
- Model information display
- UI animations and styling


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


# Frontend Request Flow


Example query:

```
What are the symptoms of diabetes?
```


Flow:

```
User Input

     |

React Component

     |

API Request

     |

FastAPI Backend

     |

Response Received

     |

UI Updates

     |

Answer + Research Sources Displayed
```


# Backend Architecture


The backend manages:

- API handling
- Query processing
- Medical research retrieval
- LLM routing
- Prompt generation
- Response generation


## Backend Structure

```
backend

|
├── app.py
│     FastAPI application entry point
│
├── rag_pipeline.py
│     Complete RAG workflow
│
├── retriever.py
│     Medical document retrieval
│
├── vector_store.py
│     ChromaDB interaction layer
│
├── embedder.py
│     Creates document embeddings
│
├── chunker.py
│     Splits research documents
│
├── pmc_loader.py
│     Loads PMC research papers
│
├── pubmed_loader.py
│     Loads PubMed articles
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
│     Creates vector database
│
├── build_rag_prompt.py
│     Evidence-based prompt generation
│
└── build_general_prompt.py
      General prompt generation
```


# Backend Request Processing Flow


When a user submits a medical question:


## Step 1: API Request

Frontend sends:


```json
{
 "question":"What is hypertension?"
}
```


Endpoint:

```
POST /ask
```


---

## Step 2: Privacy Routing


The router checks:

- Patient information
- Medical records
- Personal identifiers
- Sensitive health information


Decision:


```
                Question

                    |

             Privacy Router

              /            \

      Sensitive              General

          |                    |

          v                    v

      Ollama               Gemini

```


# RAG Pipeline Workflow


## Step 1: Query Processing

The user question is converted into a semantic embedding.


Example:

```
"What causes kidney disease?"
```

becomes a searchable vector representation.


---

## Step 2: Vector Retrieval


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


Retrieved information:

- Research content
- Paper metadata
- Authors
- Journal
- Year
- PMC ID


---

## Step 3: Context Creation


Retrieved documents are combined:


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

## Step 5: Response Generation


Output contains:

- Medical explanation
- Supporting research papers
- Citations
- Model information


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


# Local and Cloud LLM Architecture


## Local Model

Technology:

```
Ollama + Mistral
```


Used for:

- Privacy-sensitive queries
- Offline processing
- Local inference


Advantages:

- Medical data remains locally processed
- No external API transmission


---

## Cloud Model

Technology:

```
Google Gemini API
```


Used for:

- General medical questions
- Complex reasoning
- Research explanations


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


# Running the Project


# Backend Setup


Create Python 3.11 environment:


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
pip install -r requirements.txt
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


# Frontend Setup


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


# Building Research Index


Generate vector database:


```bash
cd backend

python build_index.py
```


This performs:


- Research paper loading
- Text extraction
- Document cleaning
- Chunk generation
- Embedding creation
- ChromaDB storage


# Key Features


✅ Medical research question answering

✅ Evidence-grounded responses

✅ PubMed and PMC integration

✅ Hybrid LLM architecture

✅ Privacy-aware routing

✅ Local AI inference

✅ Semantic document retrieval

✅ Research paper citations

✅ React-based interface

✅ FastAPI backend

✅ ChromaDB vector search


# Future Improvements


- Multi-language medical assistance
- Voice-based medical queries
- Medical report upload and analysis
- Timeline-based patient health insights
- Doctor-friendly research summaries
- Advanced biomedical models


# Disclaimer

MedRAG-AI is an AI research assistant and does not replace professional medical advice, diagnosis, or treatment.

Always consult qualified healthcare professionals for medical decisions.
