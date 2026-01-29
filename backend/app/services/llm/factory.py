from app.services.llm.gemini import GeminiLLM
from app.services.llm.groq import GroqLLM
from app.services.llm.openai import OpenAILLM

def get_llm(provider: str, api_key: str):
    provider = provider.lower()

    if provider == "gemini":
        return GeminiLLM(api_key)
    elif provider == "groq":
        return GroqLLM(api_key)
    elif provider == "openai":
        return OpenAILLM(api_key)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
