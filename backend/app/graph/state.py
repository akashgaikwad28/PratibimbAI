# backend/app/graph/state.py
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class GraphState(BaseModel):
    # user input
    topic: str
    urls: List[str]

    # pipeline data
    raw_contents: List[str] = []
    clean_contents: List[str] = []
    ranked_contents: Optional[List[Dict]] = None
    final_post: Optional[str] = None

    # execution metadata
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = Field(default_factory=datetime.utcnow)
    errors: List[str] = []
    

    failed_urls: List[str] = []
    fallback_used: bool = False