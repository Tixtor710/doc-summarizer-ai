import time
from typing import Iterable
from app.llm.client import get_llm
from app.llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


def stream_summary(context_chunks: list[str]) -> Iterable[str]:
    llm = get_llm(streaming=True)

    context = "\n\n".join(context_chunks)
    prompt = USER_PROMPT_TEMPLATE.format(context=context)

    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", prompt),
    ]

    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content
            time.sleep(0.1)  # 👈 ADD THIS LINE (temporary)
