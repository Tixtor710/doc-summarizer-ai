from pathlib import Path
from app.ingestion.pipeline import ingest_document
from app.retrieval.vectorstore import build_and_save_vectorstore

path = Path("data/documents/superman.txt")  # or whichever file is canonical

chunks = ingest_document(path)
build_and_save_vectorstore(chunks)

print("Vector store built and saved.")
