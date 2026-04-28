from app.utils.logger import get_logger

logger = get_logger("llm.factory")

PROVIDER_ORDER = ["groq", "gemini", "openai"]


def get_llm(provider: str, api_key: str, tier: str = "strong"):
    """
    Returns an LLM instance based on provider and tier (strong vs cheap).
    Task 5: LLM Optimization
    """
    provider = (provider or "groq").lower()
    
    # Simple tiering logic
    # In production, 'cheap' would map to GPT-3.5 or Llama-3-70b/8b
    # 'strong' would map to GPT-4o or Gemini-1.5-Pro
    
    # For now, we use the same class but we could pass a 'model' parameter
    if provider == "groq":
        from app.services.llm.groq import GroqLLM
        # Map cheap to 8b, strong to 70b in the actual GroqLLM class implementation
        return GroqLLM(api_key, model="llama3-8b-8192" if tier == "cheap" else "llama3-70b-8192")
    elif provider == "gemini":
        from app.services.llm.gemini import GeminiLLM
        return GeminiLLM(api_key, model="gemini-1.5-flash" if tier == "cheap" else "gemini-1.5-pro")
    elif provider == "openai":
        from app.services.llm.openai import OpenAILLM
        return OpenAILLM(api_key, model="gpt-3.5-turbo" if tier == "cheap" else "gpt-4o")
    
    raise ValueError(f"Unsupported LLM provider: {provider}")


def get_llm_with_fallback(profile: dict, system_keys: dict):
    for provider in PROVIDER_ORDER:
        key = profile.get(f"{provider}_api_key") or system_keys.get(provider)
        if not key:
            continue
        try:
            llm = get_llm(provider, key)
            logger.info(f"LLM selected via fallback chain: {provider}")
            return llm, provider
        except Exception as e:
            logger.warning(f"Provider {provider} init failed: {e}")
    raise RuntimeError("All LLM providers exhausted. Check your API keys.")
