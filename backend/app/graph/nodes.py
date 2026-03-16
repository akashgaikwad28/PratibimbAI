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
import json

logger = get_logger(__name__)


def fallback_post(state):
    return [f"Latest updates on {state.topic}:\n\n" + "\n".join(state.clean_contents[:2])]


@instrument_node("collect")
def collect_node(state: GraphState):
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

    return {"raw_contents": raw_contents, "errors": state.errors}


@instrument_node("clean")
def clean_node(state: GraphState):
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

    return {"clean_contents": cleaned_contents, "errors": state.errors}


@instrument_node("rank")
def rank_node(state: GraphState):
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
        logger.warning(f"LLM ranking failed, fallback used: {e}")
        ranked = heuristic_rank(
            state.clean_contents,
            state.topic
        )
        method = "heuristic"

    duration = round(time.time() - start, 2)
    logger.info(f"Finished rank_node using {method} in {duration}s")

    return {
        "ranked_contents": ranked
    }


@instrument_node("write")
def write_post_node(state: GraphState):
    logger.info(f"Write post state.ranked_contents: {bool(state.ranked_contents)}")

    if not state.ranked_contents:
        logger.warning("No ranked contents found in write_post_node! Falling back.")
        return {"final_posts": fallback_post(state)}

    try:
        llm = get_llm(
            provider=state.llm_provider,
            api_key=state.llm_api_key
        )
    except Exception as e:
        logger.warning(f"LLM init failed: {e}")
        return {"final_posts": fallback_post(state)}

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

    # Inject Critic Feedback if this is a retry
    if state.critic_feedback:
        logger.info("Injecting critic feedback for retry")
        feedback_block = f"\n\nCRITIC FEEDBACK FROM PREVIOUS DRAFT:\n{state.critic_feedback}\nPlease address this feedback to improve the post quality."
        prompt += feedback_block

    # Inject Past Memories for Style Consistency (Phase 2)
    if state.context_memories:
        logger.info("Injecting past memories for style matching")
        memory_block = "\n\nPAST SUCCESSFUL POSTS (Match this voice/style):\n"
        for i, mem in enumerate(state.context_memories):
            memory_block += f"--- MEMORY {i+1} ---\n{mem}\n"
        prompt = memory_block + prompt

    try:
        raw_response = llm.generate(prompt)
        
        # Split by the separator defined in content_gen.txt
        separator = "---POST SEPARATOR---"
        parts = raw_response.split(separator)
        
        # Clean up parts (strip whitespace and filter empty)
        posts = [p.strip() for p in parts if p.strip()]
        
        if not posts:
            logger.warning("LLM generated empty results")
            return {"final_posts": fallback_post(state)}
            
        return {"final_posts": posts}
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return {"final_posts": fallback_post(state)}


@instrument_node("retrieve_memory")
def retrieve_context_node(state: GraphState):
    """
    Find past successful posts from this user to maintain style consistency.
    """
    from app.jobs.store import search_memory
    from app.services.embedding import get_embeddings
    
    logger.info(f"Starting retrieve_context_node for user {state.user_id}")
    
    if not state.user_id:
        return {}

    try:
        search_vector = get_embeddings(state.topic)
        if not search_vector:
            return {}
            
        memories = search_memory(
            user_id=state.user_id,
            embedding=search_vector,
            limit=3
        )
        
        if memories:
            logger.info(f"Retrieved {len(memories)} memory snippets")
            context_memories = [m["content"] for m in memories]
            
            # Phase 3: Deduplication check
            best_match = memories[0]
            if best_match.get("similarity", 0) > 0.85:
                logger.warning(f"DUPLICATE DETECTED: {best_match['similarity']:.2f} similarity.")
                return {
                    "context_memories": context_memories,
                    "critic_feedback": "This topic is very similar to a past post. PLEASE REWRITE with a completely different perspective."
                }
            
            return {"context_memories": context_memories}
            
    except Exception as e:
        logger.error(f"Memory retrieval failed: {e}")

    return {}


@instrument_node("critic")
def critic_node(state: GraphState):
    """
    Review the generated post and provide scores/feedback.
    """
    logger.info("Starting critic_node")
    
    if not state.final_posts:
        return {"retry_count": state.retry_count + 1}

    try:
        llm = get_llm(
            provider=state.llm_provider,
            api_key=state.llm_api_key
        )
    except Exception as e:
        logger.warning(f"Critic LLM init failed: {e}")
        return {"retry_count": state.retry_count + 1}

    prompt_template = load_prompt("critic.txt")
    
    # Analyze the FIRST post for grading
    primary_post = state.final_posts[0]
    
    prompt = prompt_template \
        .replace("{{topic}}", state.topic) \
        .replace("{{post}}", primary_post) \
        .replace("{{profession}}", state.profession or "expert content creator")

    try:
        raw_response = llm.generate(prompt)
        
        # Extract JSON from response
        if "```json" in raw_response:
            json_str = raw_response.split("```json")[1].split("```")[0].strip()
        else:
            json_str = raw_response.strip()
            
        result = json.loads(json_str) 
        
        scores = result.get("scores", {})
        feedback = result.get("feedback", "No specific feedback provided.")
        overall_score = result.get("overall_score", 0)
        
        logger.info(f"Critic Score: {overall_score} - Feedback: {feedback}")
        
        return {
            "scores": scores,
            "critic_feedback": feedback,
            "retry_count": state.retry_count + 1
        }
    except Exception as e:
        logger.error(f"Critic analysis failed: {e}")
        return {
            "scores": {"clarity": 0}, 
            "critic_feedback": f"Analysis error: {e}", 
            "retry_count": state.retry_count + 1
        }
