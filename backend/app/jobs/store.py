from typing import Dict
from enum import Enum
from uuid import uuid4
from datetime import datetime

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

jobs: Dict[str, dict] = {}

def create_job() -> str:
    job_id = str(uuid4())
    jobs[job_id] = {
        "status": JobStatus.PENDING,
        "result": None,
        "error": None,
        "created_at": datetime.utcnow()
    }
    return job_id
