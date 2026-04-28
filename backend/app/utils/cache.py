import redis
import json
import hashlib
from typing import Optional
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger("utils.cache")

# Initialize Redis client (assumes REDIS_URL in config)
# If REDIS_URL is not provided, we fallback to a mock/disabled cache
try:
    redis_client = redis.from_url(getattr(settings, "REDIS_URL", "redis://localhost:6379/0"))
    redis_client.ping()
    logger.info("Redis cache connected")
except Exception as e:
    logger.warning(f"Redis not available, caching disabled: {e}")
    redis_client = None

def get_url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def get_cached_content(url: str) -> Optional[str]:
    if not redis_client:
        return None
    
    key = f"scrape_cache:{get_url_hash(url)}"
    cached = redis_client.get(key)
    if cached:
        logger.info(f"Cache hit for {url}")
        return cached.decode('utf-8')
    return None

def set_cached_content(url: str, content: str, ttl: int = 86400):
    if not redis_client or "ERROR" in content[:100]:
        return
    
    key = f"scrape_cache:{get_url_hash(url)}"
    try:
        redis_client.setex(key, ttl, content)
        logger.info(f"Cached content for {url}")
    except Exception as e:
        logger.error(f"Failed to set cache: {e}")
