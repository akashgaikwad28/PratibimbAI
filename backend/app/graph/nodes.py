# backend/app/graph/nodes.py

from bs4 import BeautifulSoup
from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.services.web_scraper import fetch_website_text
from app.services.youtube import get_video_transcript
from app.utils.logger import get_logger
from app.services.llm.factory import get_llm
from app.services.ranker import heuristic_rank, rank_with_llm, LLMError
from app.utils.prompt_loader import load_prompt
import time

logger = get_logger(__name__)


def fallback_post(state):
    return [f"Latest updates on {state.topic}:\n\n" + "\n".join(state.clean_contents[:2])]


@instrument_node("collect")
def collect_node(state: GraphState) -> GraphState:
    """
    Fetch raw HTML/text from all URLs
    """
    raw_contents = []

    for url in state.urls:
        logger.info(f"Fetching {url}")
        try:
            if "youtube.com" in url or "youtu.be" in url:
                content = get_video_transcript(url)
            else:
                content = fetch_website_text(url)
            
            raw_contents.append(content)
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
            state.topic,
            provider=state.llm_provider,
            api_key=state.llm_api_key
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

@instrument_node("write")
def write_post_node(state):
    logger.info("Starting write_post_node")

    if not state.ranked_contents:
        state.final_posts = fallback_post(state)
        return state

    try:
        llm = get_llm(
            provider=state.llm_provider,
            api_key=state.llm_api_key
        )
    except Exception as e:
        logger.warning(f"LLM init failed: {e}")
        state.final_posts = fallback_post(state)
        return state

    prompt_template = load_prompt("content_gen.txt")

    insights = "\n".join(state.ranked_contents[:3])

    prompt = prompt_template \
        .replace("{{topic}}", state.topic) \
        .replace("{{insights}}", insights) \
        .replace("{{tone}}", state.tone) \
        .replace("{{style}}", state.style) \
        .replace("{{platform}}", state.platform) \
        .replace("{{num_posts}}", str(state.num_posts)) \
        .replace("{{profession}}", state.profession or "expert content creator")

    try:
        raw_response = llm.generate(prompt)
        
        # Split by the separator defined in content_gen.txt
        separator = "---POST SEPARATOR---"
        parts = raw_response.split(separator)
        
        # Clean up parts (strip whitespace and filter empty)
        posts = [p.strip() for p in parts if p.strip()]
        
        state.final_posts = posts
        logger.info(f"Generated {len(posts)} posts successfully")
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        state.final_posts = fallback_post(state)

    return state
