from fastapi import APIRouter, HTTPException
from app.graph.graph import build_graph
from app.api.schemas import GenerateRequest, GenerateResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger("api.generate")

graph = build_graph()  # build once (important)

@router.post("/generate", response_model=GenerateResponse)
def generate_content(request: GenerateRequest):
    logger.info(f"Request received | topic={request.topic}")

    try:
        result = graph.invoke({
            "topic": request.topic,
            "urls": request.urls,
            "raw_contents": [],
            "clean_contents": [],
            "ranked_contents": None,
            "final_post": None
        })

        return GenerateResponse(
            topic=request.topic,
            clean_contents=result["clean_contents"],
            final_post=result.get("final_post")
        )

    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Agent execution failed")
