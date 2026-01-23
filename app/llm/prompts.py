SYSTEM_PROMPT = """
You are an internal document summarization assistant.
Use only the provided context.
If information is missing, say so.
Do not invent facts.
"""

USER_PROMPT_TEMPLATE = """

Context:
{context}

Task:
Summarize the document for an engineer.

Constraints:
- Max 150 words
- Bullet key points
- No assumptions
- No external knowledge

IMPORTANT:
- Respond with ONLY valid JSON
- Do not include explanations or prose
- Do not include markdown

JSON format:
{{
  "summary": "...",
  "key_points": ["...", "..."]
}}
"""
STREAMING_PROMPT_TEMPLATE = """
You are a helpful assistant.

Using the context below, explain the document clearly and naturally.
Write in full sentences, like you are explaining to a human.

Rules:
- Do NOT return JSON
- Do NOT use bullet points
- Do NOT mention the word "context"
- Write conversationally

Context:
{context}
"""
