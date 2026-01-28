# backend/app/graph/nodes.py

from bs4 import BeautifulSoup
from app.graph.state import GraphState
from app.services.web_scraper import fetch_website_text


def collect_node(state: GraphState) -> GraphState:
    """
    Fetch raw HTML/text from all URLs
    """
    raw_contents = []

    for url in state["urls"]:
        html = fetch_website_text(url)
        raw_contents.append(html)

    state["raw_contents"] = raw_contents
    return state


def clean_node(state: GraphState) -> GraphState:
    """
    Clean HTML into readable text
    """
    cleaned_contents = []

    for html in state["raw_contents"]:
        if html.startswith("ERROR"):
            cleaned_contents.append(html)
            continue

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        # limit size to avoid LLM overload
        cleaned_contents.append(text[:5000])

    state["clean_contents"] = cleaned_contents
    return state
