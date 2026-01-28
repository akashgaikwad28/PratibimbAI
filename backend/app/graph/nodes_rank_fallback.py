from app.graph.state import GraphState
from app.utils.logger import get_logger

logger = get_logger("fallback_ranker")

def heuristic_rank_node(state: GraphState) -> GraphState:
    logger.warning(
        f"[{state.execution_id}] Using heuristic ranking fallback"
    )

    ranked = []

    for text in state.clean_contents:
        score = len(text)  # simple heuristic
        ranked.append({
            "content": text[:300],
            "score": score
        })

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)
    state.ranked_contents = ranked[:3]
    state.fallback_used = True

    return state
