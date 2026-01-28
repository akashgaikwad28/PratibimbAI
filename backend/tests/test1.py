# backend/tests/test1.py

import sys
import os

# Add backend/app to Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app.graph.graph import build_graph


def run_test():
    graph = build_graph()

    result = graph.invoke({
        "topic": "AI Agents",
        "urls": ["https://huggingface.co/blog"],
        "raw_contents": [],
        "clean_contents": [],
        "ranked_contents": None,
        "final_post": None
    })

    print("\n--- CLEANED CONTENT (Preview) ---\n")
    print(result["clean_contents"][0][:500])


if __name__ == "__main__":
    run_test()
