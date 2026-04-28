from typing import Dict, Any, Optional
from app.jobs import repository
from app.api.schemas import GenerateRequest

def initialize_job(user_id: str, request: GenerateRequest) -> str:
    """
    Business logic for setting up a new generation job.
    """
    job_data = {
        "topic": request.topic,
        "urls": request.urls,
        "tone": request.tone,
        "style": request.style,
        "platform": request.platform,
        "num_posts": request.num_posts
    }
    return repository.create_job(user_id, job_data)

def get_job_details(job_id: str) -> Optional[Dict[str, Any]]:
    return repository.get_job(job_id)

def get_user_style_context(user_id: str) -> Dict[str, Any]:
    """
    Retrieves all necessary profile and style context for agent execution.
    """
    profile = repository.get_profile(user_id) or {}
    samples = repository.get_style_samples(user_id)
    
    return {
        "profile": profile,
        "style_samples": samples,
        "profession": profile.get("profession", "expert content creator")
    }
