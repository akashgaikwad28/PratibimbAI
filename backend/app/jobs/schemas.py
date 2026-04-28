from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    final_posts: Optional[List[str]] = None
    critic_feedback: Optional[str] = None
    errors: Optional[List[str]] = None
