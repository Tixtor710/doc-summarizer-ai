from app.llm.client import get_llm
from app.llm.prompts import STREAMING_PROMPT_TEMPLATE

def stream_summary(context_chunks):
    llm = get_llm(streaming=True)

    context = "\n\n".join(context_chunks)
    prompt = STREAMING_PROMPT_TEMPLATE.format(context=context)

    for chunk in llm.stream(prompt):
        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content
