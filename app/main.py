from fastapi import FastAPI, HTTPException
from app.retrieval.vectorstore import load_vectorstore
from app.services.summarizer import summarize

app = FastAPI(title="Document Summarizer AI")

vectorstore = None


@app.on_event("startup")
def startup():
    global vectorstore
    vectorstore = load_vectorstore()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/summarize")
def summarize_query(query: str):
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Vector store not loaded")

    docs = vectorstore.similarity_search(query, k=4)
    context_chunks = [d.page_content for d in docs]

    result = summarize(context_chunks)
    return result.model_dump()
