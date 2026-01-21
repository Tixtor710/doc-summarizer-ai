from pydantic import BaseModel
from typing import List


class DocumentSummary(BaseModel):
    summary: str
    key_points: List[str]
