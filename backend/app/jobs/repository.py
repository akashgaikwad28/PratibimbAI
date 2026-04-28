from typing import Dict, Optional, Any, List
from uuid import uuid4
from datetime import datetime
from app.services.database import queries
from app.jobs.schemas import JobStatus # We'll create this next

def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
    return queries.get_profile_by_id(user_id)

def update_profile(user_id: str, data: Dict[str, Any]):
    return queries.update_profile_by_id(user_id, data)

def create_job(user_id: str, data: Dict[str, Any] = None) -> str:
    job_id = str(uuid4())
    insert_data = {
        "id": job_id,
        "user_id": user_id,
        "status": JobStatus.PENDING,
        "created_at": datetime.utcnow().isoformat(),
    }
    if data:
        insert_data.update(data)
    queries.insert_job(insert_data)
    return job_id

def update_job(job_id: str, data: Dict[str, Any]):
    return queries.update_job_by_id(job_id, data)

def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    return queries.get_job_by_id(job_id)

def get_sources(user_id: str) -> List[Dict[str, Any]]:
    return queries.get_sources_by_user(user_id)

def create_source(user_id: str, url: str, source_type: str = "website", poll_interval: int = 6) -> Dict[str, Any]:
    data = {"user_id": user_id, "url": url, "source_type": source_type, "poll_interval_hours": poll_interval}
    res = queries.insert_source(data)
    return res.data[0] if res.data else {}

def update_source(source_id: str, data: Dict[str, Any]):
    return queries.update_source_by_id(source_id, data)

def delete_source(source_id: str, user_id: str):
    return queries.delete_source_by_id(source_id, user_id)

def store_memory(user_id: str, content: str, platform: str, embedding: List[float], job_id: str = None, is_style_sample: bool = False):
    data = {
        "user_id": user_id, "content": content, "platform": platform,
        "embedding": embedding, "job_id": job_id, "is_style_sample": is_style_sample,
    }
    return queries.insert_memory(data)

def search_memory(user_id: str, embedding: List[float], limit: int = 3):
    return queries.match_memory_rpc(embedding, 0.5, limit, user_id)

def get_style_samples(user_id: str) -> List[Dict[str, Any]]:
    return queries.get_style_samples_by_user(user_id)

def delete_memory(memory_id: str, user_id: str):
    return queries.delete_memory_by_id(memory_id, user_id)
