from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import time
import sys

from app.retrieval.vectorstore import load_vectorstore
from app.retrieval.index_documents import index_all_documents
from app.services.summarizer import summarize
from app.services.streaming_summarizer import stream_summary
from app.utils.logging import setup_logger
from app.middleware.request_logging import request_logging_middleware


logger = setup_logger("api")

app = FastAPI(title="Document Summarizer AI")
from fastapi.middleware.cors import CORSMiddleware

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
# Frontend (D.2)
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
    logger.info(f"Retrieved {len(docs)} chunks")

    context_chunks = [d.page_content for d in docs]
    result = summarize(context_chunks)

    logger.info("Summarization completed")
    return result.model_dump()

# --------------------------------------------------
# Summarization (SSE streaming) — D.3
# --------------------------------------------------
@app.get("/summarize/sse")
def summarize_sse(query: str):
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Vector store not loaded")

    docs = vectorstore.similarity_search(query, k=4)
    context_chunks = [d.page_content for d in docs]

    def event_generator():
        for token in stream_summary(context_chunks):
            yield f"data: {token}\n\n"
            time.sleep(0.01)  # helps flush on Windows

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
# Upload + reindex
# --------------------------------------------------
DOCUMENTS_DIR = Path("data/documents")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DOCUMENTS_DIR / file.filename

    contents = await file.read()
    file_path.write_bytes(contents)

    logger.info(f"Uploaded document: {file.filename}")

    index_all_documents()

    global vectorstore
    vectorstore = load_vectorstore()

    logger.info("Reindexing completed after upload")

    return {
        "status": "success",
        "filename": file.filename,
    }
