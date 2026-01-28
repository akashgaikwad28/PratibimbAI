# backend/app/graph/graph.py
from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.graph.nodes import collect_node, clean_node


def build_graph():
    graph = StateGraph(GraphState)

    # add nodes
    graph.add_node("collect", collect_node)
    graph.add_node("clean", clean_node)

    # define flow
    graph.set_entry_point("collect")
    graph.add_edge("collect", "clean")
    graph.add_edge("clean", END)

    return graph.compile()
