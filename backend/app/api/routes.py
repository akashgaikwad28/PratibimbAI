from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.graph.graph import build_graph
from app.jobs.store import create_job, update_job, get_job, get_profile, update_profile, JobStatus
from app.utils.logger import get_logger
from app.config import config
from app.utils.auth import get_current_user
from fastapi import Depends
from gotrue import User

router = APIRouter()
logger = get_logger("api.generate")

graph = build_graph()

def run_agent(job_id: str, request: GenerateRequest):
    logger.info(f"Job {job_id} started")

    update_job(job_id, {"status": JobStatus.RUNNING})

    try:
        # 1. Fetch Job and User Profile
        job = get_job(job_id)
        if not job:
            raise Exception("Job record not found")
        
        user_id = job.get("user_id")
        profile = get_profile(user_id) if user_id else None
        
        # 2. Extract User-Specific API Key with Priority
        # Priority: Groq -> Gemini -> OpenAI
        selected_provider = None
        active_key = None
        
        if profile:
            if profile.get("groq_api_key"):
                selected_provider = "groq"
                active_key = profile.get("groq_api_key")
            elif profile.get("gemini_api_key"):
                selected_provider = "gemini"
                active_key = profile.get("gemini_api_key")
            elif profile.get("openai_api_key"):
                selected_provider = "openai"
                active_key = profile.get("openai_api_key")
        
        # 3. Fallback to Request choice or System defaults if no user key found
        if not active_key:
            selected_provider = request.llm_provider or config.LLM_PROVIDER
            active_key = config.get_api_key(selected_provider)
            logger.info(f"Using fallback/default provider {selected_provider}")
        else:
            logger.info(f"Using user-provided key for {selected_provider}")

        # 4. Invoke Graph with dynamic keys
        result = graph.invoke({
            "topic": request.topic,
            "urls": request.urls,
            "tone": request.tone,
            "style": request.style,
            "platform": request.platform,
            "num_posts": request.num_posts,
            "profession": profile.get("profession") if profile else None,
            "raw_contents": [],
            "clean_contents": [],
            "ranked_contents": None,
            "final_posts": [],
            "llm_provider": selected_provider,
            "llm_api_key": active_key
        })

        update_job(job_id, {
            "status": JobStatus.COMPLETED,
            "final_posts": result.get("final_posts", [])
        })

        logger.info(f"Job {job_id} completed")

    except Exception as e:
        update_job(job_id, {
            "status": JobStatus.FAILED,
            "errors": [str(e)]
        })
        logger.error(f"Job {job_id} failed: {str(e)}")

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
