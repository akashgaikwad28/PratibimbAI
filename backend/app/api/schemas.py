from pydantic import BaseModel
from typing import List, Optional, Dict

class GenerateRequest(BaseModel):
    topic: str
    urls: List[str]
    tone: Optional[str] = "Professional"
    style: Optional[str] = "Concise"
    platform: Optional[str] = "LinkedIn"
    num_posts: Optional[int] = 1
    llm_provider: Optional[str] = None

class GenerateResponse(BaseModel):
    topic: str
    clean_contents: List[str]
    final_posts: List[str] = []

class UpdateProfile(BaseModel):
    full_name: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    profession: Optional[str] = None
    preferences: Optional[Dict] = None
