import feedparser
from typing import List, Dict
from app.utils.logger import get_logger

logger = get_logger("trend_service")

# Popular technical/AI feeds
FEEDS = {
    "hacker_news": "https://news.ycombinator.com/rss",
    "product_hunt": "https://www.producthunt.com/feed"
}

def get_latest_trends(source: str = "hacker_news", limit: int = 5) -> List[Dict]:
    """
    Fetch the latest items from an RSS feed.
    """
    url = FEEDS.get(source)
    if not url:
        return []

    try:
        # Note: feedparser handles XML/RSS parsing
        feed = feedparser.parse(url)
        results = []
        
        for entry in feed.entries[:limit]:
            results.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", entry.title)
            })
            
        return results
    except Exception as e:
        logger.error(f"Trend fetch failed for {source}: {e}")
        return []

def discover_all_trends() -> List[Dict]:
    all_results = []
    for source in FEEDS:
        all_results.extend(get_latest_trends(source))
    return all_results
