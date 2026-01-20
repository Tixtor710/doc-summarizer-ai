from pathlib import Path
from langchain_community.vectorstores import FAISS
from app.ingestion.pipeline import ingest_document
from app.retrieval.vectorstore import build_vectorstore


def ingest_and_index(path: Path) -> FAISS:
    chunks = ingest_document(path)
    vectorstore = build_vectorstore(chunks)
    return vectorstore
