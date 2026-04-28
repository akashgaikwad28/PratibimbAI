from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: str = "INFO"

    LLM_PROVIDER: str = "groq"
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    API_KEY_ENCRYPTION_SECRET: Optional[str] = None
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]

    def get_api_key(self, provider: str) -> Optional[str]:
        return {
            "openai": self.OPENAI_API_KEY,
            "groq": self.GROQ_API_KEY,
            "gemini": self.GEMINI_API_KEY,
        }.get(provider)

settings = Settings()
