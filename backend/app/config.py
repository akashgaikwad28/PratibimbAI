import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # App Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_api_key(cls, provider: str = None) -> str:
        provider = provider or cls.LLM_PROVIDER
        if provider == "openai":
            return cls.OPENAI_API_KEY
        elif provider == "groq":
            return cls.GROQ_API_KEY
        elif provider == "gemini":
            return cls.GEMINI_API_KEY
        return None

config = Config()
