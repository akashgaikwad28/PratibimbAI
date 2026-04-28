import asyncio
from playwright.async_api import async_playwright
from app.utils.logger import get_logger

logger = get_logger("services.browser_scraper")

async def fetch_dynamic_content(url: str) -> str:
    """
    Scrapes a website using Playwright to handle JavaScript-heavy content.
    """
    logger.info(f"Starting browser scraping for {url}")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            # Navigate and wait for network to be idle
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Extract visible text from the body
            content = await page.evaluate("document.body.innerText")
            
            await browser.close()
            logger.info(f"Successfully scraped {url} via Playwright")
            return content
            
        except Exception as e:
            logger.error(f"Playwright scraping failed for {url}: {e}")
            return f"ERROR (Playwright): {str(e)}"

async def smart_fetch(url: str) -> str:
    """
    High-level scraper that chooses between dynamic and static methods.
    """
    from app.services.web_scraper import fetch_website_text_async
    
    # Try dynamic first for production grade
    content = await fetch_dynamic_content(url)
    
    if content.startswith("ERROR") or len(content) < 200:
        logger.warning(f"Dynamic scrape failed or returned low quality for {url}. Falling back to static.")
        return await fetch_website_text_async(url)
        
    return content
