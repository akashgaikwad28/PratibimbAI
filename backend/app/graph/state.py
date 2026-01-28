# backend/app/graph/state.py
from typing import List, Optional, TypedDict


class GraphState(TypedDict):
    topic: str
    urls: List[str]

    # collected data
    raw_contents: List[str]

    # processed data
    clean_contents: List[str]

    # future (we'll fill later)
    ranked_contents: Optional[List[str]]
    final_post: Optional[str]
