# backend/app/graph/graph.py
from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes import collect_node, clean_node, rank_node, write_post_node, critic_node, retrieve_context_node
from app.graph.nodes_rank_fallback import heuristic_rank_node


def needs_fallback(state: GraphState) -> bool:
    return len(state.clean_contents) == 0

def should_retry(state: GraphState) -> bool:
    # Average score below threshold (e.g., 7.0) AND retry_count < 1
    scores = state.scores.values()
    avg_score = sum(scores) / len(scores) if scores else 0
    
    do_retry = avg_score < 7.0 and state.retry_count < 1
    if do_retry:
        print(f"--- LOOPING BACK: Score {avg_score:.1f} is too low ---")
    return do_retry


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("collect", collect_node)
    builder.add_node("clean", clean_node)
    builder.add_node("fallback_rank", heuristic_rank_node)
    builder.add_node("rank", rank_node)
    builder.add_node("retrieve_mem", retrieve_context_node)
    builder.add_node("write", write_post_node)
    builder.add_node("critic", critic_node)

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
    
    # After memory, go to write
    builder.add_edge("retrieve_mem", "write")
    
    # After write, go to critic
    builder.add_edge("write", "critic")
    
    # Conditional edge from critic: back to write or END
    builder.add_conditional_edges(
        "critic",
        should_retry,
        {
            True: "write",
            False: END
        }
    )

    return builder.compile()
