# Document Summarizer AI

A modular document summarization system built in Python, designed to ingest real-world documents and prepare them for grounded, retrieval-based summarization.

This project focuses on **robust preprocessing, clean architecture, and reproducibility**, rather than prompt-only demos.

---

## Overview

The system ingests documents (PDF, TXT, Markdown), normalizes and chunks their content, and prepares them for downstream retrieval-augmented generation (RAG).

The project is structured to reflect production-ready GenAI workflows:
- Deterministic document ingestion
- Semantic chunking with overlap
- Clear separation of concerns
- Explicit dependency management
- Extensible architecture for embeddings and retrieval

---

## Features

- PDF, TXT, and Markdown document ingestion
- Text normalization for consistent downstream processing
- Semantic chunking using recursive character splitting
- Modular project structure (ingestion, retrieval, LLM, services)
- Ready for vector embeddings and FAISS-based retrieval
- FastAPI application scaffold for future API exposure

---

## Project Structure
```
doc-summarizer-ai/
├── app/
│ ├── ingestion/ # Document loading, normalization, chunking
│ ├── retrieval/ # Embeddings and vector store (WIP)
│ ├── llm/ # Model client and prompt templates (WIP)
│ ├── services/ # Application services
│ ├── schemas/ # Pydantic schemas
│ ├── utils/ # Logging and utilities
│ ├── config.py
│ └── main.py
├── data/
│ └── documents/ # Input documents (ignored by git)
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup

### Prerequisites
- Python 3.10+
- Virtual environment support
------
### Installation

```bash
git clone https://github.com/Tixtor710/doc-summarizer-ai.git
cd doc-summarizer-ai
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
-----
### Environment Variables

```bash
Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```
-----
### Testing Document Ingestion
Place a document in:
```
data/documents/
```
Run the ingestion test module from the project root:
```
python -m app.ingestion.test
```
This will:
1. Load the document
2. Normalize the text
3. Chunk it into semantic segments
4. Print chunk count and sample output
-----
### Design Philosophy
- **Garbage in, garbage out applies:** preprocessing quality matters more than model size
- **Determinism over vibes:** predictable pipelines beat clever prompts
- **Separation of concerns:** ingestion, retrieval, and generation are independent layers
- **Fail loudly:** errors are preferred over silent hallucinations
------
### Roadmap
- Document ingestion and chunking
- Embeddings generation
- FAISS vector store integration
- Retrieval-augmented generation (RAG)
- Output validation and evaluation
- Human-in-the-loop review