from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.database.supabase_client import get_supabase

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    supabase = get_supabase()
    
    try:
        # Verify token and get user
        response = supabase.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return response.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")
