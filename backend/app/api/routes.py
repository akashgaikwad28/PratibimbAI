from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.graph.graph import build_graph
from app.api.schemas import GenerateRequest
from app.jobs.store import create_job, update_job, get_job, JobStatus
from app.utils.logger import get_logger
from app.config import config

router = APIRouter()
logger = get_logger("api.generate")

graph = build_graph()

def run_agent(job_id: str, request: GenerateRequest):
    logger.info(f"Job {job_id} started")

    update_job(job_id, {"status": JobStatus.RUNNING})

    try:
        result = graph.invoke({
            "topic": request.topic,
            "urls": request.urls,
            "tone": request.tone,
            "style": request.style,
            "platform": request.platform,
            "num_posts": request.num_posts,
            "raw_contents": [],
            "clean_contents": [],
            "ranked_contents": None,
            "final_posts": [],
            "llm_provider": config.LLM_PROVIDER,
            "llm_api_key": config.get_api_key()
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
    background_tasks: BackgroundTasks
):
    # Store initial request metadata in DB
    job_id = create_job({
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
