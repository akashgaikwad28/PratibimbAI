from typing import Dict, Optional, Any
from enum import Enum
from uuid import uuid4
from datetime import datetime
from app.services.database.supabase_client import get_supabase

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase()
    response = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if response.data:
        return response.data[0]
    return None

def create_job(user_id: str, data: Dict[str, Any] = None) -> str:
    supabase = get_supabase()
    job_id = str(uuid4())
    
    insert_data = {
        "id": job_id,
        "user_id": user_id,
        "status": JobStatus.PENDING,
        "created_at": datetime.utcnow().isoformat()
    }
    
    if data:
        insert_data.update(data)

    supabase.table("jobs").insert(insert_data).execute()
    return job_id

def update_job(job_id: str, data: Dict[str, Any]):
    supabase = get_supabase()
    supabase.table("jobs").update(data).eq("id", job_id).execute()

def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase()
    response = supabase.table("jobs").select("*").eq("id", job_id).execute()
    if response.data:
        return response.data[0]
    return None
def update_profile(user_id: str, data: Dict[str, Any]):
    supabase = get_supabase()
    supabase.table("profiles").update(data).eq("id", user_id).execute()
