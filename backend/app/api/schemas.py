from pydantic import BaseModel
from typing import List, Optional

class GenerateRequest(BaseModel):
    topic: str
    urls: List[str]
    tone: Optional[str] = "Professional"
    style: Optional[str] = "Concise"
    platform: Optional[str] = "LinkedIn"
    num_posts: Optional[int] = 1

class GenerateResponse(BaseModel):
    topic: str
    clean_contents: List[str]
    final_posts: List[str] = []
