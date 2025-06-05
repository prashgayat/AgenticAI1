# utils/ranker.py

KEYWORDS = ["LangChain", "OpenAI", "Streamlit", "RAG", "GPT"]

# Configurable weights for scoring
WEIGHTS = {
    "semantic": 0.7,  # Based on FAISS distance
    "keyword": 0.3    # Based on presence of key terms
}

def score_job(idx, distance, descriptions):
    """
    Compute a hybrid relevance score for a job.
    - idx: index from FAISS result
    - distance: semantic distance from FAISS
    - descriptions: list of job descriptions
    Returns: float score between 0 and 1 (higher is better)
    """
    if idx >= len(descriptions):
        return 0.0

    desc = descriptions[idx].lower()
    max_distance = 1.0  # Normalization factor (FAISS distances are typically <1.0)

    # Semantic relevance (inverted distance)
    semantic_score = 1.0 - min(distance / max_distance, 1.0)

    # Keyword presence
    keyword_hits = sum(1 for kw in KEYWORDS if kw.lower() in desc)
    keyword_score = keyword_hits / len(KEYWORDS)

    # Final weighted score
    final_score = WEIGHTS["semantic"] * semantic_score + WEIGHTS["keyword"] * keyword_score
    return round(final_score, 4)
