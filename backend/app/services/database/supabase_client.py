from supabase import create_client, Client
from app.config import config

def get_supabase() -> Client:
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY missing in environment variables")
    return create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
