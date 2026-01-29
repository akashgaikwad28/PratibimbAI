from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.graph.graph import build_graph
from app.api.schemas import GenerateRequest
from app.jobs.store import jobs, create_job, JobStatus
from app.jobs.store import jobs, create_job, JobStatus
from app.utils.logger import get_logger
from app.config import config

router = APIRouter()
logger = get_logger("api.generate")

graph = build_graph()

def run_agent(job_id: str, request: GenerateRequest):
    logger.info(f"Job {job_id} started")

    jobs[job_id]["status"] = JobStatus.RUNNING

    try:
        result = graph.invoke({
            "topic": request.topic,
            "urls": request.urls,
            "raw_contents": [],
            "clean_contents": [],
            "ranked_contents": None,
            "clean_contents": [],
            "ranked_contents": None,
            "final_post": None,
            "llm_provider": config.LLM_PROVIDER,
            "llm_api_key": config.get_api_key()
        })

        jobs[job_id]["status"] = JobStatus.COMPLETED
        jobs[job_id]["result"] = result

        logger.info(f"Job {job_id} completed")

    except Exception as e:
        jobs[job_id]["status"] = JobStatus.FAILED
        jobs[job_id]["error"] = str(e)
        logger.error(f"Job {job_id} failed: {str(e)}")

@router.post("/generate")
def generate_async(
    request: GenerateRequest,
    background_tasks: BackgroundTasks
):
    job_id = create_job()

    background_tasks.add_task(run_agent, job_id, request)

    return {
        "job_id": job_id,
        "status": "queued"
    }

@router.get("/job/{job_id}")
def get_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]
