from pathlib import Path
from langchain_community.vectorstores import FAISS
from app.retrieval.embeddings import get_embedding_model

VECTORSTORE_PATH = Path("data/vectorstore")


from pathlib import Path
from langchain_community.vectorstores import FAISS
from app.retrieval.embeddings import get_embedding_model

VECTORSTORE_PATH = Path("data/vectorstore")


def build_and_save_vectorstore(chunks_with_meta: list[dict]) -> FAISS:
    embeddings = get_embedding_model()

    texts = [c["text"] for c in chunks_with_meta]
    metadatas = [{"source": c["source"]} for c in chunks_with_meta]

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    vectorstore.save_local(VECTORSTORE_PATH)
    return vectorstore



def load_vectorstore() -> FAISS:
    embeddings = get_embedding_model()
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
