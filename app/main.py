from fastapi import FastAPI, HTTPException
from app.retrieval.vectorstore import load_vectorstore
from app.services.summarizer import summarize
from app.utils.logging import setup_logger
from app.middleware.request_logging import request_logging_middleware


logger = setup_logger("api")

app = FastAPI(title="Document Summarizer AI")
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

