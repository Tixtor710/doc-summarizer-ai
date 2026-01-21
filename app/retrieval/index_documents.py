from pathlib import Path
from app.ingestion.pipeline import ingest_document
from app.retrieval.vectorstore import build_and_save_vectorstore

DOCUMENTS_DIR = Path("data/documents")


def index_all_documents() -> None:
    all_chunks = []

    for doc_path in DOCUMENTS_DIR.glob("*.txt"):
        chunks = ingest_document(doc_path)
        for chunk in chunks:
            all_chunks.append(
                {
                    "text": chunk,
                    "source": doc_path.name
                }
            )

    build_and_save_vectorstore(all_chunks)
