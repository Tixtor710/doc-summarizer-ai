from pathlib import Path
from app.retrieval.pipeline import ingest_and_index

doc_path = Path("data/documents/superman.txt")

vectorstore = ingest_and_index(doc_path)

results = vectorstore.similarity_search(
    query="What advice does the author give to his younger self?",
    k=2
)

print(results[0].page_content[:500])


