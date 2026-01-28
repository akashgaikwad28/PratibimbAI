import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMError(Exception):
    pass


def rank_with_llm(contents: list[str], topic: str, top_k: int = 3):
    if not openai.api_key:
        raise LLMError("No API key")

    prompt = f"""
You are ranking content for relevance.

Topic: {topic}

Return ONLY a Python list of indices (0-based) for the top {top_k} most relevant items.

Contents:
"""

    for i, c in enumerate(contents):
        prompt += f"\n[{i}] {c[:1000]}\n"

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            timeout=15
        )

        text = resp.choices[0].message.content.strip()
        indices = eval(text)  # controlled format

        return [contents[i] for i in indices]

    except Exception as e:
        raise LLMError(str(e))
