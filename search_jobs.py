# search_jobs.py (Automated Version – No Manual Input)

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import sys
import os

# Ensure the utils module is on the path
sys.path.append(os.path.dirname(__file__))

from utils.ranker import score_job  # ✅ Corrected import

# ==== Configuration ====
TOP_K_RAW = 30
DISPLAY_LIMIT = 10

# ==== Load FAISS index and metadata ====
faiss_index = faiss.read_index("faiss_index.idx")
with open("job_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

descriptions = metadata["description"]
titles = metadata["title"]
urls = metadata["url"]

model = SentenceTransformer("all-MiniLM-L6-v2")


def run_search_pipeline(query: str):
    """
    Run search pipeline over FAISS index with hybrid scoring.
    Returns top job leads.
    """
    if not query:
        raise ValueError("❌ Empty query received by search pipeline.")

    query_vector = model.encode([query]).astype("float32")
    D, I = faiss_index.search(query_vector, TOP_K_RAW)

    scored_results = []
    for idx, dist in zip(I[0], D[0]):
        if idx == -1 or idx >= len(descriptions):
            continue

        score = score_job(idx, dist, descriptions)
        scored_results.append({
            "title": titles[idx],
            "url": urls[idx],
            "distance": round(dist, 4),
            "score": score
        })

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return scored_results[:DISPLAY_LIMIT]
