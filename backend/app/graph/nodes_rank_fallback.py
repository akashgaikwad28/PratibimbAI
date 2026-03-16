from app.graph.state import GraphState
from app.utils.logger import get_logger

logger = get_logger("fallback_ranker")

def heuristic_rank_node(state: GraphState) -> GraphState:
    logger.warning(
        f"[{state.execution_id}] Using heuristic ranking fallback"
    )

    ranked = []

    for text in state.clean_contents:
        ranked.append(text[:500])  # store snippet strings

    return {
        "ranked_contents": ranked[:3],
        "fallback_used": True
    }
