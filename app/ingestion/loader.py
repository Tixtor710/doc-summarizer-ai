from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
        pages = loader.load()
        return "\n".join(page.page_content for page in pages)

    elif suffix in [".txt", ".md"]:
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()
        return docs[0].page_content

    else:
        raise ValueError(f"Unsupported file type: {suffix}")
