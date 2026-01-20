from pathlib import Path
from app.ingestion.pipeline import ingest_document

chunks = ingest_document(Path(".\data\documents\To me,20 Years Ago…..pdf"))

print(len(chunks))
print(chunks[0][:500])
