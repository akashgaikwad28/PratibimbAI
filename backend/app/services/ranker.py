from app.services.llm.factory import get_llm
from app.utils.logger import get_logger

logger = get_logger("services.ranker")

class LLMError(Exception):
    pass

def rank_with_llm(contents: list[str], topic: str, provider: str = "openai", api_key: str = None):
    try:
        llm = get_llm(provider, api_key)
        
        prompt = f"Rank these based on relevance to '{topic}'. Return ONLY a python list of indices like [0, 2].\n\n"
        for i, c in enumerate(contents):
            prompt += f"[{i}] {c[:500]}...\n"

        response = llm.generate(prompt)
        
        # simplistic parsing (robustness would need JSON/OutputParser)
        import ast
        # find list in string
        start = response.find('[')
        end = response.rfind(']') + 1
        indices = ast.literal_eval(response[start:end])
        
        return [contents[i] for i in indices if i < len(contents)]
    except Exception as e:
        logger.error(f"LLM ranking failed: {e}")
        raise LLMError(str(e))

def heuristic_rank(contents: list[str], topic: str, top_k: int = 3):
    topic_words = set(topic.lower().split())

    scored = []
    for text in contents:
        if text.startswith("ERROR"):
            continue

        words = text.lower().split()
        score = sum(1 for w in words if w in topic_words)
        score += len(text) / 1000  # reward richer content

        scored.append((score, text))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [text for _, text in scored[:top_k]]
