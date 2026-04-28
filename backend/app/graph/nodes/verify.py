from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.services.llm.factory import get_llm
from app.utils.logger import get_logger
from app.graph.wrappers.retry import retry_node
from app.utils.prompt_loader import load_prompt

logger = get_logger("node.verify")

@instrument_node("verify")
@retry_node(max_retries=1)
def verify_node(state: GraphState):
    """
    Validates that the rewritten post actually fixed the issues identified by the critic.
    """
    logger.info(f"[{state.execution_id}] Verifying improvement")
    
    # Task 5: Use cheaper model for verification
    llm = get_llm(provider=state.llm_provider, api_key=state.llm_api_key, tier="cheap")
    
    if not state.critic_feedback or not state.final_posts:
        return {}

    prompt = (
        load_prompt("verify.txt", domain="analysis")
        .replace("{{critic_feedback}}", state.critic_feedback)
        .replace("{{post}}", state.final_posts[0])
    )
    
    try:
        verification = llm.generate(prompt)
        logger.info(f"[{state.execution_id}] Verification result: {verification[:50]}...")
        
        if "NO" in verification.upper()[:10] and state.retry_count < 2:
            # Force one more retry if still not good
            return {"retry_count": state.retry_count} # Don't increment to force another loop or similar
            
        return {}
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return {}
