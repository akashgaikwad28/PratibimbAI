from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.services.llm.factory import get_llm
from app.utils.prompt_loader import load_prompt
from app.utils.logger import get_logger

from app.graph.wrappers.retry import retry_node

logger = get_logger("node.hook")

@instrument_node("hook")
@retry_node(max_retries=1)
def hook_node(state: GraphState):
    """
    Generates a high-impact opening hook for the post.
    """
    logger.info(f"[{state.execution_id}] Generating hook for {state.topic}")
    
    # Use a faster/cheaper model for hook
    llm = get_llm(provider=state.llm_provider, api_key=state.llm_api_key, tier="cheap")
    
    prompt = (
        load_prompt("hook.txt", domain="ideation")
        .replace("{{platform}}", state.platform)
        .replace("{{topic}}", state.topic)
        .replace("{{insights}}", " ".join(state.ranked_contents[:2]) if state.ranked_contents else "None")
    )
    
    try:
        hook = llm.generate(prompt)
        logger.info(f"[{state.execution_id}] Hook generated: {hook[:50]}...")
        return {"hook": hook}
    except Exception as e:
        logger.error(f"Hook generation failed: {e}")
        return {}
