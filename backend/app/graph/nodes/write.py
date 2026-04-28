from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.utils.logger import get_logger
from app.services.llm.factory import get_llm
from app.utils.prompt_loader import load_prompt

logger = get_logger(__name__)


def fallback_post(state: GraphState) -> list:
    base = "\n".join(state.clean_contents[:2])
    return [f"Latest updates on {state.topic}:\n\n{base}"]


from app.graph.wrappers.retry import retry_node
from app.utils.metrics import instrument_node

@instrument_node("write")
@retry_node(max_retries=2)
def write_post_node(state: GraphState):
    logger.info(f"[{state.execution_id}] write_post_node — has_ranked={bool(state.ranked_contents)}")

    if not state.ranked_contents:
        logger.warning(f"[{state.execution_id}] No ranked contents, using fallback")
        return {"final_posts": fallback_post(state)}

    try:
        llm = get_llm(provider=state.llm_provider, api_key=state.llm_api_key)
    except Exception as e:
        logger.warning(f"[{state.execution_id}] LLM init failed: {e}")
        return {"final_posts": fallback_post(state)}

    prompt_template = load_prompt("content.txt", domain="generation")
    insights = "\n".join(state.ranked_contents[:3])

    prompt = (
        prompt_template
        .replace("{{topic}}", state.topic)
        .replace("{{insights}}", insights)
        .replace("{{tone}}", state.tone)
        .replace("{{style}}", state.style)
        .replace("{{platform}}", state.platform)
        .replace("{{num_posts}}", str(state.num_posts))
        .replace("{{profession}}", state.profession or "expert content creator")
    )

    if state.hook:
        logger.info(f"[{state.execution_id}] Injecting generated hook")
        prompt += f"\n\nUSE THIS OPENING HOOK:\n{state.hook}"

    if state.critic_feedback:
        logger.info(f"[{state.execution_id}] Injecting critic feedback")
        prompt += f"\n\nCRITIC FEEDBACK FROM PREVIOUS DRAFT:\n{state.critic_feedback}\nAddress this feedback to improve quality."

    if state.context_memories:
        logger.info(f"[{state.execution_id}] Injecting {len(state.context_memories)} style memories")
        memory_block = "\n\nPAST SUCCESSFUL POSTS (Match this voice/style):\n"
        for i, mem in enumerate(state.context_memories):
            memory_block += f"--- MEMORY {i+1} ---\n{mem}\n"
        prompt = memory_block + prompt

    try:
        raw_response = llm.generate(prompt)
        posts = [p.strip() for p in raw_response.split("---POST SEPARATOR---") if p.strip()]
        if not posts:
            logger.warning(f"[{state.execution_id}] LLM returned empty output")
            return {"final_posts": fallback_post(state)}
        return {"final_posts": posts}
    except Exception as e:
        logger.error(f"[{state.execution_id}] LLM generation failed: {e}")
        return {"final_posts": fallback_post(state)}
