import pytest
from app.services.llm.factory import get_llm


def test_invalid_provider_raises():
    with pytest.raises(ValueError, match="Unsupported LLM provider"):
        get_llm("unknown_provider", "some_key")


def test_valid_providers_dont_raise_on_init():
    for provider in ["groq", "gemini", "openai"]:
        try:
            get_llm(provider, "dummy_key")
        except ValueError:
            pytest.fail(f"get_llm raised ValueError for valid provider: {provider}")
