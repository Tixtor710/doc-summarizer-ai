from typing import Iterable
from app.llm.client import get_llm
from app.llm.prompts import STREAMING_PROMPT_TEMPLATE


def stream_summary(context_chunks) -> Iterable[str]:
    llm = get_llm(streaming=True)

    context = "\n\n".join(context_chunks)
    prompt = STREAMING_PROMPT_TEMPLATE.format(context=context)

    buffer = ""

    for chunk in llm.stream(prompt):
        if hasattr(chunk, "content") and chunk.content:
            buffer += chunk.content

            # Flush on sentence boundary
            if buffer.endswith((".", "!", "?")):
                yield buffer
                buffer = ""

    # Flush anything remaining
    if buffer.strip():
        yield buffer
