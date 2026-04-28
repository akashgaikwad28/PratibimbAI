import json
from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.utils.logger import get_logger
from app.services.llm.factory import get_llm
from app.utils.prompt_loader import load_prompt

from app.graph.wrappers.retry import retry_node

logger = get_logger(__name__)


@instrument_node("critic")
@retry_node(max_retries=1) # Critic is less critical to retry heavily
def critic_node(state: GraphState):
    logger.info(f"[{state.execution_id}] Starting critic_node (retry={state.retry_count})")

    if not state.final_posts:
        return {"retry_count": state.retry_count + 1}

    try:
        llm = get_llm(provider=state.llm_provider, api_key=state.llm_api_key, tier="cheap")
    except Exception as e:
        logger.warning(f"[{state.execution_id}] Critic LLM init failed: {e}")
        return {"retry_count": state.retry_count + 1}

    prompt = (
        load_prompt("critic.txt", domain="analysis")
        .replace("{{topic}}", state.topic)
        .replace("{{post}}", state.final_posts[0])
        .replace("{{profession}}", state.profession or "expert content creator")
    )

    try:
        raw = llm.generate(prompt)
        json_str = raw.split("```json")[1].split("```")[0].strip() if "```json" in raw else raw.strip()
        result = json.loads(json_str)
        scores = result.get("scores", {})
        feedback = result.get("feedback", "No specific feedback provided.")
        logger.info(f"[{state.execution_id}] Critic score={result.get('overall_score')} feedback={feedback[:80]}")
        return {"scores": scores, "critic_feedback": feedback, "retry_count": state.retry_count + 1}
    except Exception as e:
        logger.error(f"[{state.execution_id}] Critic failed: {e}")
        return {"scores": {"clarity": 0}, "critic_feedback": f"Analysis error: {e}", "retry_count": state.retry_count + 1}
