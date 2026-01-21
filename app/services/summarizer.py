import json
import re
from app.llm.client import get_llm
from app.llm.prompts import USER_PROMPT_TEMPLATE

from app.schemas.summary import DocumentSummary


def _extract_json(text: str) -> dict:
    """
    Extract the first JSON object found in the text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")

    return json.loads(match.group())


def summarize(context_chunks: list[str]) -> DocumentSummary:
    llm = get_llm()
    context = "\n\n".join(context_chunks)

    response = llm.invoke([
    {
        "role": "user",
        "content": USER_PROMPT_TEMPLATE.format(context=context)
    }
])


    data = _extract_json(response.content)
    return DocumentSummary.model_validate(data)
