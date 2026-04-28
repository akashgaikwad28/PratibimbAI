import pytest
from app.graph.state import GraphState


@pytest.fixture
def base_state():
    return GraphState(topic="AI in Healthcare", urls=["https://example.com"], llm_provider="groq", llm_api_key="test_key")
