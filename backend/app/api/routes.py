from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.jobs.store import (
    create_job, update_job, get_job, get_profile, update_profile, 
    JobStatus, get_sources, create_source, update_source, delete_source
)
from app.api.schemas import GenerateRequest, UpdateProfile, SourceCreate, SourceUpdate, SourceResponse, IdeaRequest, FinalizeRequest
from app.services.agent import run_agent
from app.services.llm.factory import get_llm
from app.utils.prompt_loader import load_prompt
from app.jobs.store import store_memory
from app.services.embedding import get_embeddings
from app.utils.logger import get_logger
from app.config import config
from app.utils.auth import get_current_user
from fastapi import Depends
try:
    from gotrue import User
except ImportError:
    from typing import Any as User

router = APIRouter()
logger = get_logger("api.generate")

@router.post("/generate")
def generate_async(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
):
    user_id = user.id

    job_id = create_job(user_id, {
        "topic": request.topic,
        "urls": request.urls,
        "tone": request.tone,
        "style": request.style,
        "platform": request.platform,
        "num_posts": request.num_posts
    })

    background_tasks.add_task(run_agent, job_id, request)

    return {
        "job_id": job_id,
        "status": "queued"
    }

@router.get("/job/{job_id}")
def get_job_route(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@router.get("/profile")
def get_user_profile(user: User = Depends(get_current_user)):
    user_id = user.id
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/profile")
def update_user_profile(
    request: UpdateProfile,
    user: User = Depends(get_current_user)
):
    user_id = user.id
    
    # Filter out None values to avoid overwriting existing data with null
    update_data = {k: v for k, v in request.dict().items() if v is not None}
    
    try:
        update_profile(user_id, update_data)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Profile update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Source Management Routes ---

@router.get("/sources", response_model=list[SourceResponse])
def list_sources(user: User = Depends(get_current_user)):
    return get_sources(user.id)

@router.post("/sources", response_model=SourceResponse)
def add_source(request: SourceCreate, user: User = Depends(get_current_user)):
    try:
        return create_source(
            user.id, 
            request.url, 
            request.source_type, 
            request.poll_interval_hours
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/sources/{source_id}")
def update_monitored_source(
    source_id: str, 
    request: SourceUpdate, 
    user: User = Depends(get_current_user)
):
    update_data = {k: v for k, v in request.dict().items() if v is not None}
    update_source(source_id, update_data)
    return {"status": "success"}

@router.delete("/sources/{source_id}")
def remove_source(source_id: str, user: User = Depends(get_current_user)):
    delete_source(source_id, user.id)
    return {"status": "success"}

@router.post("/ideas")
def get_content_ideas(request: IdeaRequest, user: User = Depends(get_current_user)):
    try:
        profile = get_profile(user.id)
        selected_provider = request.llm_provider or (profile.get("groq_api_key") and "groq") or config.LLM_PROVIDER
        active_key = profile.get(f"{selected_provider}_api_key") or config.get_api_key(selected_provider)
        
        llm = get_llm(selected_provider, active_key)
        prompt_template = load_prompt("idea_gen.txt")
        prompt = prompt_template.replace("{{topic}}", request.topic)
        
        response = llm.generate(prompt)
        
        # Parse JSON
        import json
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
            
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Idea generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history/finalize")
def finalize_job(request: FinalizeRequest, user: User = Depends(get_current_user)):
    """
    Captures the final edited version of a post and stores it in memory.
    """
    try:
        # 1. Generate Embedding
        vector = get_embeddings(request.content)
        if not vector:
            return {"status": "error", "message": "Failed to generate embedding"}
            
        # 2. Store in Memory
        store_memory(
            user_id=user.id,
            content=request.content,
            platform=request.platform,
            embedding=vector,
            job_id=request.job_id
        )
        
        return {"status": "success", "message": "Memories stored"}
    except Exception as e:
        logger.error(f"Finalization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends")
def fetch_trends(source: str = "hacker_news"):
    from app.services.trends import get_latest_trends
    return get_latest_trends(source)
