from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.utils.logger import get_logger
from app.services.scheduler import start_scheduler

logger = get_logger("app")

app = FastAPI(
    title="PratibimbAI",
    description="Agent-based AI content system",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
def startup():
    logger.info("PratibimbAI API started")
    start_scheduler()

@app.get("/health")
def health_check():
    return {"status": "ok"}
