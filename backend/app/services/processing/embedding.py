import requests
from typing import List
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger("services.processing.embedding")

# Note: Using a lightweight, free model from HuggingFace
# Dimensions: 384
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2"

def get_embeddings(text: str) -> List[float]:
    """
    Generate vector embeddings for a given text.
    Uses HuggingFace Inference API (Free Tier).
    """
    try:
        response = requests.post(
            HF_MODEL_URL,
            json={"inputs": text},
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"HF Embedding failed ({response.status_code}): {response.text}")
            return []
            
        return response.json()
    except Exception as e:
        logger.error(f"Embedding service error: {e}")
        return []

def get_batch_headings(texts: List[str]) -> List[List[float]]:
    # HF API supports batching
    try:
        response = requests.post(
            HF_MODEL_URL,
            json={"inputs": texts},
            timeout=20
        )
        return response.json()
    except Exception as e:
        logger.error(f"Batch embedding error: {e}")
        return []
