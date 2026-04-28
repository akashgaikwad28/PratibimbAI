from app.graph.wrappers.retry import retry_node
from app.graph.state import GraphState
from app.services.ingestion.browser_scraper import smart_fetch
from app.services.ingestion.youtube import get_video_transcript
from app.utils.cache import get_cached_content, set_cached_content
from app.utils.logger import get_logger
import asyncio

from app.utils.metrics import instrument_node

logger = get_logger(__name__)


@instrument_node("collect")
@retry_node(max_retries=2)
async def collect_node(state: GraphState):
    """
    Fetch raw contents with smart caching and browser scraping.
    """
    raw_contents = []
    
    # Process URLs in parallel for performance (Task 8)
    async def process_url(url: str):
        # 1. Check Cache (Task 3)
        cached = get_cached_content(url)
        if cached:
            return cached
            
        # 2. Fetch Content
        try:
            if "youtube.com" in url or "youtu.be" in url:
                content = get_video_transcript(url) # Note: this is likely sync, could wrap in thread
            else:
                content = await smart_fetch(url) # Task 1
                
            # 3. Store in Cache if valid
            if content and not content.startswith("ERROR"):
                set_cached_content(url, content)
                
            return content
        except Exception as e:
            error_msg = f"Collect failed for {url}: {e}"
            state.errors.append(error_msg)
            logger.error(f"[{state.execution_id}] {error_msg}")
            return f"ERROR: {str(e)}"

    # Task 8: Parallel gathering
    tasks = [process_url(url) for url in state.urls]
    raw_contents = await asyncio.gather(*tasks)

    return {"raw_contents": raw_contents, "errors": state.errors}
