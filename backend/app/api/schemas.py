from pydantic import BaseModel
from typing import List, Optional

class GenerateRequest(BaseModel):
    topic: str
    urls: List[str]

class GenerateResponse(BaseModel):
    topic: str
    clean_contents: List[str]
    final_post: Optional[str] = None
