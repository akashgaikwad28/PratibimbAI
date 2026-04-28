from app.graph.state import GraphState
from app.utils.logger import get_logger

logger = get_logger(__name__)


def heuristic_rank_node(state: GraphState):
    logger.warning(f"[{state.execution_id}] Using heuristic ranking fallback")
    ranked = [text[:500] for text in state.clean_contents]
    return {"ranked_contents": ranked[:3], "fallback_used": True}
