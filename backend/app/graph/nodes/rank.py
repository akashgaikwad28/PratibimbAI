from app.utils.metrics import instrument_node
from app.graph.wrappers.retry import retry_node
from app.graph.state import GraphState
from app.utils.logger import get_logger
from app.services.processing.ranker import heuristic_rank, rank_with_llm, LLMError

logger = get_logger(__name__)


@instrument_node("rank")
@retry_node(max_retries=2)
def rank_node(state: GraphState):
    logger.info(f"[{state.execution_id}] Starting rank_node")
    start = time.time()
    try:
        ranked = rank_with_llm(
            state.clean_contents,
            state.topic,
            provider=state.llm_provider,
            api_key=state.llm_api_key
        )
        method = "LLM"
    except LLMError as e:
        logger.warning(f"[{state.execution_id}] LLM ranking failed, using heuristic: {e}")
        ranked = heuristic_rank(state.clean_contents, state.topic)
        method = "heuristic"
    logger.info(f"[{state.execution_id}] rank_node done via {method} in {round(time.time()-start,2)}s")
    return {"ranked_contents": ranked}
