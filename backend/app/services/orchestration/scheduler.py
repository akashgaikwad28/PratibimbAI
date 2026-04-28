import asyncio
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from app.jobs.store import update_source, create_job, JobStatus, get_profile
from app.services.database.supabase_client import get_supabase
from app.services.ingestion.web_scraper import fetch_website_text
from app.services.ingestion.youtube import get_video_transcript
from app.services.orchestration.agent import run_agent
from app.api.schemas import GenerateRequest
from app.utils.logger import get_logger

logger = get_logger("services.orchestration.scheduler")

def calculate_hash(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()

async def check_source_for_updates(source: Dict[str, Any]):
    source_id = source['id']
    user_id = source['user_id']
    url = source['url']
    source_type = source['source_type']
    last_hash = source.get('last_content_hash')
    
    logger.info(f"Checking source {url} ({source_type}) for user {user_id}")
    
    try:
        content = ""
        if source_type == 'youtube':
            content = get_video_transcript(url)
        else:
            content = fetch_website_text(url)
            
        if not content or content.startswith("ERROR"):
            logger.warning(f"Empty or error content for {url}")
            return

        new_hash = calculate_hash(content)
        
        if new_hash != last_hash:
            logger.info(f"🚨 NEW CONTENT detected for {url}! Triggering agent...")
            
            # Create a background job for this update
            profile = get_profile(user_id)
            job_id = create_job(user_id, {
                "topic": f"Automated News: {url[:30]}...",
                "urls": [url],
                "tone": profile.get('preferences', {}).get('default_tone', 'Professional'),
                "style": profile.get('preferences', {}).get('default_style', 'Concise'),
                "platform": profile.get('preferences', {}).get('default_platform', 'LinkedIn'),
            })
            
            request = GenerateRequest(
                topic=f"Update from {url}",
                urls=[url]
            )
            run_agent(job_id, request)
            
            # Update source with new hash
            update_source(source_id, {
                "last_content_hash": new_hash,
                "last_polled_at": datetime.now(timezone.utc).isoformat()
            })
        else:
            logger.info(f"No changes for {url}")
            update_source(source_id, {
                "last_polled_at": datetime.now(timezone.utc).isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error polling source {url}: {e}")

async def scheduler_loop():
    logger.info("Starting background scheduler loop...")
    while True:
        try:
            supabase = get_supabase()
            response = supabase.table("monitored_sources").select("*").eq("is_active", True).execute()
            
            if response.data:
                now = datetime.now(timezone.utc)
                for source in response.data:
                    last_polled = source.get('last_polled_at')
                    interval = source.get('poll_interval_hours', 6)
                    
                    should_poll = False
                    if not last_polled:
                        should_poll = True
                    else:
                        lp_dt = datetime.fromisoformat(last_polled.replace('Z', '+00:00'))
                        if now - lp_dt > timedelta(hours=interval):
                            should_poll = True
                    
                    if should_poll:
                        await check_source_for_updates(source)
                        
        except Exception as e:
            logger.error(f"Error in scheduler loop: {e}")
            
        await asyncio.sleep(300) # Check every 5 minutes

def start_scheduler():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_loop())
