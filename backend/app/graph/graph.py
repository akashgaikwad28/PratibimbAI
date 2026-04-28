# backend/app/graph/graph.py
from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes import (
    collect_node, clean_node, rank_node, write_post_node,
    critic_node, verify_node, hook_node, 
    retrieve_context_node, heuristic_rank_node
)
from app.utils.logger import get_logger

logger = get_logger("graph")


def needs_fallback(state: GraphState) -> bool:
    return len(state.clean_contents) == 0

def should_retry(state: GraphState) -> bool:
    if not state.scores or state.retry_count >= 2:
        return False
    score_values = list(state.scores.values())
    avg_score = sum(score_values) / len(score_values)
    do_retry = avg_score < 7.0
    if do_retry:
        logger.info(f"Critic loop triggered: avg_score={avg_score:.2f}, retry={state.retry_count}")
    return do_retry


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("collect", collect_node)
    builder.add_node("clean", clean_node)
    builder.add_node("fallback_rank", heuristic_rank_node)
    builder.add_node("rank", rank_node)
    builder.add_node("retrieve_mem", retrieve_context_node)
    builder.add_node("hook", hook_node) # Task 4
    builder.add_node("write", write_post_node)
    builder.add_node("critic", critic_node)
    builder.add_node("verify", verify_node) # Task 4

    builder.set_entry_point("collect")
    builder.add_edge("collect", "clean")

    builder.add_conditional_edges(
        "clean",
        needs_fallback,
        {
            True: "fallback_rank",
            False: "rank"
        }
    )

    builder.add_edge("fallback_rank", "retrieve_mem")
    builder.add_edge("rank", "retrieve_mem")
    
    # New Flow: memory -> hook -> write
    builder.add_edge("retrieve_mem", "hook")
    builder.add_edge("hook", "write")
    
    # After write, go to critic
    builder.add_edge("write", "critic")
    
    # After critic, go to verify
    builder.add_edge("critic", "verify")
    
    # Conditional edge from verify: back to write or END
    builder.add_conditional_edges(
        "verify",
        should_retry,
        {
            True: "write",
            False: END
        }
    )

    return builder.compile()
