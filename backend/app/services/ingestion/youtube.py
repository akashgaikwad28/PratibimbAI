import youtube_transcript_api
from app.utils.logger import get_logger
from urllib.parse import urlparse, parse_qs

logger = get_logger("services.ingestion.youtube")

def get_video_id(url: str) -> str:
    """
    Extracts video ID from various YouTube URL formats.
    """
    parsed = urlparse(url)
    
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    
    if parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query)['v'][0]
        if parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        if parsed.path.startswith('/v/'):
            return parsed.path.split('/')[2]
            
    raise ValueError(f"Invalid YouTube URL: {url}")

def get_video_transcript(url: str) -> str:
    try:
        video_id = get_video_id(url)
        logger.info(f"Fetching transcript for video {video_id}")
        
        # In version 1.2.4, we must instantiate the class first
        api = youtube_transcript_api.YouTubeTranscriptApi()
        
        # fetch() is an instance method that returns a FetchedTranscript object
        # which can be converted to raw data or iterated
        transcript_obj = api.fetch(video_id)
        
        # Combine text snippets
        full_text = " ".join([t['text'] for t in transcript_obj.to_raw_data()])
        return full_text
        
    except Exception as e:
        logger.error(f"Failed to fetch transcript: {e}")
        raise e
