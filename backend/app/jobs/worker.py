import os
from app.services.orchestration.agent import run_agent
from app.api.schemas import GenerateRequest
from app.utils.logger import get_logger

logger = get_logger("jobs.worker")

def execute_job(job_id: str, request_data: dict):
    """
    Worker entry point for executing an agent job.
    """
    logger.info(f"Worker processing job {job_id}")
    try:
        request = GenerateRequest(**request_data)
        run_agent(job_id, request)
        logger.info(f"Worker successfully completed job {job_id}")
    except Exception as e:
        logger.error(f"Worker failed job {job_id}: {e}")
        raise # Raise for RQ retry mechanism

if __name__ == "__main__":
    # This block allows running the worker directly via 'python -m app.jobs.worker'
    # but normally you use 'rq worker pratibimb_jobs'
    from rq import Worker, Queue, Connection
    import redis
    from app.core.config import settings

    redis_conn = redis.from_url(getattr(settings, "REDIS_URL", "redis://localhost:6379/0"))
    with Connection(redis_conn):
        worker = Worker([Queue("pratibimb_jobs")])
        worker.work()
