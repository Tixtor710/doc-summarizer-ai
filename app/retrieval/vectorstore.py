from pathlib import Path
from langchain_community.vectorstores import FAISS
from app.retrieval.embeddings import get_embedding_model

VECTORSTORE_PATH = Path("data/vectorstore")


def build_and_save_vectorstore(chunks: list[str]) -> FAISS:
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)
    return vectorstore


def load_vectorstore() -> FAISS:
    embeddings = get_embedding_model()
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
