import httpx
from app.utils.logger import get_logger

logger = get_logger("services.ingestion.web_scraper")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


async def fetch_website_text_async(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.text
    except Exception as e:
        logger.warning(f"Async fetch failed for {url}: {e}")
        return f"ERROR fetching {url}: {e}"


def fetch_website_text(url: str) -> str:
    try:
        with httpx.Client(timeout=15.0, follow_redirects=True) as client:
            response = client.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.text
    except Exception as e:
        logger.warning(f"Sync fetch failed for {url}: {e}")
        return f"ERROR fetching {url}: {e}"
