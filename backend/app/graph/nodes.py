# backend/app/graph/nodes.py

from bs4 import BeautifulSoup
from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.services.web_scraper import fetch_website_text
from app.utils.logger import get_logger
from app.services.llm_client import rank_with_llm, LLMError
from app.services.ranker import heuristic_rank
import time

logger = get_logger(__name__)


@instrument_node("collect")
def collect_node(state: GraphState) -> GraphState:
    """
    Fetch raw HTML/text from all URLs
    """
    raw_contents = []

    for url in state.urls:
        logger.info(f"Fetching {url}")
        try:
            html = fetch_website_text(url)
            raw_contents.append(html)
        except Exception as e:
            error_msg = f"Collect failed for {url}: {e}"
            state.errors.append(error_msg)
            logger.error(f"[{state.execution_id}] {error_msg}")

    state.raw_contents = raw_contents
    logger.info("Finished collect_node")
    return state


@instrument_node("clean")
def clean_node(state: GraphState) -> GraphState:
    """
    Clean HTML into readable text
    """
    cleaned_contents = []

    for html in state.raw_contents:
        if html.startswith("ERROR"):
            cleaned_contents.append(html)
            continue

        try:
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

            # limit size to avoid LLM overload
            cleaned_contents.append(text[:5000])
        except Exception as e:
            error_msg = f"Clean failed: {e}"
            state.errors.append(error_msg)
            logger.error(f"[{state.execution_id}] {error_msg}")

    state.clean_contents = cleaned_contents
    return state


@instrument_node("rank")
def rank_node(state):
    logger.info("Starting rank_node")
    start = time.time()

    try:
        ranked = rank_with_llm(
            state.clean_contents,
            state.topic
        )
        method = "LLM"

    except LLMError as e:
        print(f"LLM failed, fallback used: {e}")
        ranked = heuristic_rank(
            state.clean_contents,
            state.topic
        )
        method = "heuristic"

    duration = round(time.time() - start, 2)
    print(f"Finished rank_node using {method} in {duration}s")

    return {
        "ranked_contents": ranked
    }
