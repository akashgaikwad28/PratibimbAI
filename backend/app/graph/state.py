# backend/app/graph/state.py
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class GraphState(BaseModel):
    # user input
    topic: str
    urls: List[str]
    tone: str = "Professional"
    style: str = "Concise"
    platform: str = "LinkedIn"
    num_posts: int = 1
    profession: Optional[str] = None

    # pipeline data
    raw_contents: List[str] = []
    clean_contents: List[str] = []
    ranked_contents: Optional[List[str]] = None
    final_posts: List[str] = []

    # execution metadata
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = Field(default_factory=datetime.utcnow)
    errors: List[str] = []
    
    # configuration
    llm_provider: str = "openai"
    llm_api_key: Optional[str] = None
    

    failed_urls: List[str] = []
    fallback_used: bool = False
    
    # Pro Features: Critic & Scoring
    scores: Dict[str, float] = {} # e.g., {"virality": 8.5, "clarity": 9.0}
    critic_feedback: Optional[str] = None
    retry_count: int = 0
    
    # Pro Features: Memory
    user_id: Optional[str] = None
    context_memories: List[str] = [] # Retrieved past posts for style matching