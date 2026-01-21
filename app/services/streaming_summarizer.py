import json
from typing import Iterable
from app.llm.client import get_llm
from app.llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


def stream_summary(context_chunks):
    llm = get_llm(streaming=True)

    context = "\n\n".join(context_chunks)
    prompt = USER_PROMPT_TEMPLATE.format(context=context)

    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", prompt),
    ]

    for chunk in llm.stream(messages):
        # LangChain streaming chunks
        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content

