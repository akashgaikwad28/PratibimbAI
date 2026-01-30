# backend/app/graph/graph.py
from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes import collect_node, clean_node, rank_node, write_post_node
from app.graph.nodes_rank_fallback import heuristic_rank_node


def needs_fallback(state: GraphState) -> bool:
    return len(state.clean_contents) == 0


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("collect", collect_node)
    builder.add_node("clean", clean_node)
    builder.add_node("fallback_rank", heuristic_rank_node)
    builder.add_node("rank", rank_node)
    builder.add_node("write", write_post_node)

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

    builder.add_edge("fallback_rank", "write")
    builder.add_edge("rank", "write")
    builder.add_edge("write", END)

    return builder.compile()
