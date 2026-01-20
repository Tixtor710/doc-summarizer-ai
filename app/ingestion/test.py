from pathlib import Path
from app.ingestion.pipeline import ingest_document

chunks = ingest_document(Path(".\data\documents\superman.txt"))

print(len(chunks))
print(chunks[0][:500])
