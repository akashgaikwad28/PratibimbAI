from app.graph.graph import build_graph
from app.jobs.store import update_job, get_job, get_profile, JobStatus
from app.utils.logger import get_logger
from app.config import config
from app.api.schemas import GenerateRequest

logger = get_logger("services.agent")
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
