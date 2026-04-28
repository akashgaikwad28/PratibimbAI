from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

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

class IdeaRequest(BaseModel):
    topic: str
    llm_provider: Optional[str] = None

class FinalizeRequest(BaseModel):
    job_id: str
    content: str
    platform: str

# --- Source Schemas ---

class SourceCreate(BaseModel):
    url: str
    source_type: Optional[str] = "website"
    poll_interval_hours: Optional[int] = 6

class SourceUpdate(BaseModel):
    url: Optional[str] = None
    source_type: Optional[str] = None
    poll_interval_hours: Optional[int] = None
    is_active: Optional[bool] = None

class SourceResponse(BaseModel):
    id: str
    url: str
    source_type: str
    poll_interval_hours: int
    last_polled_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Style Sample Schemas ---

class StyleSampleCreate(BaseModel):
    content: str
    platform: Optional[str] = "LinkedIn"

class StyleSampleResponse(BaseModel):
    id: str
    content: str
    platform: str
    created_at: datetime

    class Config:
        from_attributes = True
