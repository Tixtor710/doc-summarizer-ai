from fastapi import FastAPI, HTTPException
from app.retrieval.vectorstore import load_vectorstore
from app.services.summarizer import summarize
from app.utils.logging import setup_logger
from app.middleware.request_logging import request_logging_middleware
from fastapi import UploadFile, File
from pathlib import Path
from app.retrieval.index_documents import index_all_documents
from fastapi.responses import StreamingResponse
from app.services.streaming_summarizer import stream_summary
from fastapi.middleware.cors import CORSMiddleware


logger = setup_logger("api")

app = FastAPI(title="Document Summarizer AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(request_logging_middleware)

vectorstore = None


@app.on_event("startup")
def startup():
    global vectorstore
    logger.info("Loading vector store")
    vectorstore = load_vectorstore()
    logger.info("Vector store loaded")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/summarize")
def summarize_query(query: str):
    

    if vectorstore is None:
        logger.error("Vector store not loaded")
        raise HTTPException(status_code=500, detail="Vector store not loaded")

    docs = vectorstore.similarity_search(query, k=4)
    logger.info(f"Retrieved {len(docs)} chunks")

    for d in docs:
        logger.debug(
            f"Source={d.metadata.get('source')} | Preview={d.page_content[:80]}"
        )

    context_chunks = [d.page_content for d in docs]

    result = summarize(context_chunks)
    logger.info("Summarization completed")

    return result.model_dump()

DOCUMENTS_DIR = Path("data/documents")

@app.post("/summarize/stream")
def summarize_stream(query: str):
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Vector store not loaded")

    docs = vectorstore.similarity_search(query, k=4)
    context_chunks = [d.page_content for d in docs]

    return StreamingResponse(
        stream_summary(context_chunks),
        media_type="text/plain"
    )

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported"
        )

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DOCUMENTS_DIR / file.filename

    contents = await file.read()
    file_path.write_bytes(contents)

    logger.info(f"Uploaded document: {file.filename}")

    # Reindex documents
    index_all_documents()

    # Reload vectorstore
    global vectorstore
    vectorstore = load_vectorstore()

    logger.info("Reindexing completed after upload")

    return {
        "status": "success",
        "filename": file.filename
    }
