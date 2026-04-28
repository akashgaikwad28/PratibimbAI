import redis
from rq import Queue
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger("services.queue")

# Initialize Redis and RQ Queue
try:
    redis_conn = redis.from_url(getattr(settings, "REDIS_URL", "redis://localhost:6379/0"))
    work_queue = Queue("pratibimb_jobs", connection=redis_conn)
    logger.info("RQ Queue initialized")
except Exception as e:
    logger.error(f"Failed to initialize RQ Queue: {e}")
    work_queue = None

def enqueue_agent_job(job_id: str, request_data: dict):
    """
    Enqueues the agent execution task.
    """
    if not work_queue:
        logger.warning("Queue not available. Falling back to immediate execution (not recommended for production)")
        from app.services.agent import run_agent
        from app.api.schemas import GenerateRequest
        # This fallback is just for development ease
        return run_agent(job_id, GenerateRequest(**request_data))

    logger.info(f"Enqueuing job {job_id}")
    work_queue.enqueue(
        "app.jobs.worker.execute_job",
        args=(job_id, request_data),
        job_id=job_id,
        retry=3 # Task 2: Retry support
    )
