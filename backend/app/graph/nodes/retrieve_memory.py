from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.utils.logger import get_logger

logger = get_logger(__name__)


@instrument_node("retrieve_memory")
def retrieve_context_node(state: GraphState):
    logger.info(f"[{state.execution_id}] retrieve_context_node user={state.user_id}")

    if not state.user_id:
        return {}

    try:
        from app.jobs.store import search_memory, get_style_samples
        from app.services.processing.embedding import get_embeddings

        samples = get_style_samples(state.user_id)
        context_memories = [f"[PRIMARY STYLE REFERENCE] {s['content']}" for s in samples[:2]]

        search_vector = get_embeddings(state.topic)
        if search_vector:
            memories = search_memory(user_id=state.user_id, embedding=search_vector, limit=3)
            if memories:
                logger.info(f"[{state.execution_id}] Retrieved {len(memories)} RAG memories")
                sample_texts = {s["content"] for s in samples}
                for m in memories:
                    if m["content"] not in sample_texts:
                        context_memories.append(m["content"])

                best_match = memories[0]
                if best_match.get("similarity", 0) > 0.85:
                    logger.warning(f"[{state.execution_id}] Duplicate detected sim={best_match['similarity']:.2f}")
                    return {
                        "context_memories": context_memories[:5],
                        "critic_feedback": "This topic is very similar to a past post. REWRITE with a completely different angle.",
                    }

        return {"context_memories": context_memories[:5]}

    except Exception as e:
        logger.error(f"[{state.execution_id}] Memory retrieval failed: {e}")
        return {}
