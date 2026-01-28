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
