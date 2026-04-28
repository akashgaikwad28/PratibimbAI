from app.graph.graph import build_graph
from app.jobs.store import update_job, get_job, get_profile, JobStatus
from app.utils.logger import get_logger, set_execution_id
from app.core.config import settings
from app.api.schemas import GenerateRequest

logger = get_logger("services.orchestration.agent")
_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_agent(job_id: str, request: GenerateRequest):
    set_execution_id(job_id)
    logger.info(f"Job started")
    update_job(job_id, {"status": JobStatus.RUNNING})

    try:
        job = get_job(job_id)
        if not job:
            raise Exception("Job record not found")

        user_id = job.get("user_id")
        profile = get_profile(user_id) if user_id else {}
        profile = profile or {}

        # Task 5: Use fallback chain for robustness
        from app.services.llm.factory import get_llm_with_fallback
        
        system_keys = {
            "openai": settings.OPENAI_API_KEY,
            "groq": settings.GROQ_API_KEY,
            "gemini": settings.GEMINI_API_KEY
        }
        
        _, selected_provider = get_llm_with_fallback(profile, system_keys)
        active_key = profile.get(f"{selected_provider}_api_key") or system_keys.get(selected_provider)

        result = _get_graph().invoke({
            "topic": request.topic,
            "urls": request.urls,
            "tone": request.tone,
            "style": request.style,
            "platform": request.platform,
            "num_posts": request.num_posts,
            "profession": profile.get("profession"),
            "user_id": user_id,
            "raw_contents": [],
            "clean_contents": [],
            "ranked_contents": None,
            "final_posts": [],
            "llm_provider": selected_provider,
            "llm_api_key": active_key,
        })

        update_job(job_id, {
            "status": JobStatus.COMPLETED,
            "final_posts": result.get("final_posts", []),
            "critic_feedback": result.get("critic_feedback", ""),
        })
        logger.info(f"Job completed successfully")

    except Exception as e:
        update_job(job_id, {"status": JobStatus.FAILED, "errors": [str(e)]})
        logger.error(f"Job failed: {e}")
