from langchain_community.vectorstores import FAISS
from typing import List
from app.retrieval.embeddings import get_embedding_model


def build_vectorstore(chunks: List[str]) -> FAISS:
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore
