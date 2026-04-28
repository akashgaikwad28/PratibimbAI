from typing import Dict, Any, Optional, List
from app.services.database.supabase_client import get_supabase

# --- Profiles ---
def get_profile_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    res = get_supabase().table("profiles").select("*").eq("id", user_id).execute()
    return res.data[0] if res.data else None

def update_profile_by_id(user_id: str, data: Dict[str, Any]):
    return get_supabase().table("profiles").update(data).eq("id", user_id).execute()

# --- Jobs ---
def insert_job(data: Dict[str, Any]):
    return get_supabase().table("jobs").insert(data).execute()

def update_job_by_id(job_id: str, data: Dict[str, Any]):
    return get_supabase().table("jobs").update(data).eq("id", job_id).execute()

def get_job_by_id(job_id: str) -> Optional[Dict[str, Any]]:
    res = get_supabase().table("jobs").select("*").eq("id", job_id).execute()
    return res.data[0] if res.data else None

# --- Monitored Sources ---
def get_active_sources() -> List[Dict[str, Any]]:
    res = get_supabase().table("monitored_sources").select("*").eq("is_active", True).execute()
    return res.data or []

def get_sources_by_user(user_id: str) -> List[Dict[str, Any]]:
    res = get_supabase().table("monitored_sources").select("*").eq("user_id", user_id).execute()
    return res.data or []

def insert_source(data: Dict[str, Any]):
    return get_supabase().table("monitored_sources").insert(data).execute()

def update_source_by_id(source_id: str, data: Dict[str, Any]):
    return get_supabase().table("monitored_sources").update(data).eq("id", source_id).execute()

def delete_source_by_id(source_id: str, user_id: str):
    return get_supabase().table("monitored_sources").delete().eq("id", source_id).eq("user_id", user_id).execute()

# --- Memory Embeddings ---
def insert_memory(data: Dict[str, Any]):
    return get_supabase().table("memory_embeddings").insert(data).execute()

def match_memory_rpc(query_embedding: List[float], match_threshold: float, match_count: int, user_id: str):
    return get_supabase().rpc("match_memory", {
        "query_embedding": query_embedding,
        "match_threshold": match_threshold,
        "match_count": match_count,
        "p_user_id": user_id,
    }).execute()

def get_style_samples_by_user(user_id: str) -> List[Dict[str, Any]]:
    res = get_supabase().table("memory_embeddings").select("*").eq("user_id", user_id).eq("is_style_sample", True).execute()
    return res.data or []

def delete_memory_by_id(memory_id: str, user_id: str):
    return get_supabase().table("memory_embeddings").delete().eq("id", memory_id).eq("user_id", user_id).execute()
