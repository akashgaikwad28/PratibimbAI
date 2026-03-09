import requests
from typing import List
from app.config import config
from app.utils.logger import get_logger

logger = get_logger("embedding_service")

# Note: Using a lightweight, free model from HuggingFace
# Dimensions: 384
HF_MODEL_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

def get_embeddings(text: str) -> List[float]:
    """
    Generate vector embeddings for a given text.
    Uses HuggingFace Inference API (Free Tier).
    """
    headers = {}
    # If the user has a HF token, it can be used, otherwise it uses public rate limits
    # For now, we attempt public access or use a placeholder if needed
    
    try:
        response = requests.post(
            HF_MODEL_URL,
            # headers=headers,
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
