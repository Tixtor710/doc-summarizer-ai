from pathlib import Path
from app.ingestion.pipeline import ingest_document
from app.retrieval.vectorstore import build_vectorstore
from app.services.summarizer import summarize

path = Path("data/documents/superman.txt")

chunks = ingest_document(path)
vectorstore = build_vectorstore(chunks)

docs = vectorstore.similarity_search(
    query="What is the main message of this document?",
    k=4
)

context_chunks = [d.page_content for d in docs]

result = summarize(context_chunks)

print(result.model_dump_json(indent=2))
