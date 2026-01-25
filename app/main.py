from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import time

from app.retrieval.vectorstore import load_vectorstore
from app.retrieval.index_documents import index_all_documents
from app.services.summarizer import summarize
from app.services.streaming_summarizer import stream_summary
from app.llm.client import get_llm
from app.utils.logging import setup_logger
from app.middleware.request_logging import request_logging_middleware

from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# Session memory (D.7)
# --------------------------------------------------
SESSION_MEMORY: Dict[str, str] = {}

logger = setup_logger("api")

app = FastAPI(title="Document Summarizer AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Middleware
# --------------------------------------------------
app.middleware("http")(request_logging_middleware)

# --------------------------------------------------
# Frontend
# --------------------------------------------------
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

@app.get("/stream")
def stream_ui():
    return FileResponse(FRONTEND_DIR / "stream.html")

# --------------------------------------------------
# Vector store lifecycle
# --------------------------------------------------
vectorstore = None

@app.on_event("startup")
def startup():
    global vectorstore
    logger.info("Loading vector store")
    vectorstore = load_vectorstore()
    logger.info("Vector store loaded")

# --------------------------------------------------
# Health
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# --------------------------------------------------
# Summarization (non-stream)
# --------------------------------------------------
@app.post("/summarize")
def summarize_query(query: str):
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Vector store not loaded")

    docs = vectorstore.similarity_search(query, k=4)
    context_chunks = [d.page_content for d in docs]
    result = summarize(context_chunks)

    return result.model_dump()

# --------------------------------------------------
# Summarization (SSE streaming) — D.7
# --------------------------------------------------
@app.get("/summarize/sse")
def summarize_sse(query: str):
    if "latest_document" in SESSION_MEMORY:
        context_chunks = [SESSION_MEMORY["latest_document"]]
    else:
        if vectorstore is None:
            raise HTTPException(status_code=500, detail="Vector store not loaded")

        docs = vectorstore.similarity_search(query, k=4)
        context_chunks = [d.page_content for d in docs]

    def event_generator():
        for token in stream_summary(context_chunks):
            yield f"data: {token}\n\n"
            time.sleep(0.01)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# --------------------------------------------------
# Follow-up summarization (D.7)
# --------------------------------------------------
@app.post("/summarize/followup")
def summarize_followup(session_id: str, query: str):
    previous = SESSION_MEMORY.get(session_id)

    if not previous:
        raise HTTPException(status_code=400, detail="No previous session found")

    llm = get_llm()
    prompt = f"""
Given the previous summary:

{previous}

Answer this follow-up request:
{query}
"""

    response = llm.invoke(prompt)
    return {"response": response.content}

# --------------------------------------------------
# Upload + reindex
# --------------------------------------------------
DOCUMENTS_DIR = Path("data/documents")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    contents = await file.read()
    text = contents.decode("utf-8")

    # Save latest uploaded document in session memory
    SESSION_MEMORY["latest_document"] = text

    # Optional: still persist + reindex if you want
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DOCUMENTS_DIR / file.filename
    file_path.write_text(text, encoding="utf-8")

    index_all_documents()

    global vectorstore
    vectorstore = load_vectorstore()

    return {
        "status": "success",
        "filename": file.filename,
    }
