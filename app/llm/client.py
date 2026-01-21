from langchain_ollama import ChatOllama

def get_llm(streaming: bool = False):
    return ChatOllama(
        model="llama3",
        streaming=streaming,
    )
