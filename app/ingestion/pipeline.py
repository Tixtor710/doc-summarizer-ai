from pathlib import Path
from .loader import load_document
from .normalizer import normalize_text
from .chunker import chunk_text


def ingest_document(path: Path) -> list[str]:
    raw_text = load_document(path)
    clean_text = normalize_text(raw_text)
    chunks = chunk_text(clean_text)
    return chunks
