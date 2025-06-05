# search_jobs_ranked.py (Updated with scorer.py compatibility)

import faiss
import pickle
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from sentence_transformers import SentenceTransformer
from scorer import score_job  # ✅ Corrected import



# ==== Configuration ====
TOP_K_RAW = 30
DISTANCE_THRESHOLD = 0.6

# ==== Load FAISS index and metadata ====
faiss_index = faiss.read_index("faiss_index.idx")
with open("job_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

descriptions = metadata["description"]
titles = metadata["title"]
urls = metadata["url"]

model = SentenceTransformer("all-MiniLM-L6-v2")

# ==== Get user query ====
query = input("\n🔍 Enter your job search query (e.g., LangChain chatbot): ").strip()
if not query:
    print("❌ Empty query. Exiting.")
    exit()

query_vector = model.encode([query]).astype("float32")

# ==== Search FAISS ====
D, I = faiss_index.search(query_vector, TOP_K_RAW)

# ==== Score and re-rank ====
scored_results = []
for idx, dist in zip(I[0], D[0]):
    if dist > DISTANCE_THRESHOLD or idx >= len(titles):
        continue
    score = score_job(idx, dist, descriptions)
    scored_results.append({
        "title": titles[idx],
        "url": urls[idx],
        "distance": dist,
        "score": score
    })

# Sort by descending score
scored_results.sort(key=lambda x: x["score"], reverse=True)

# ==== Display results ====
if not scored_results:
    print("⚠️ No highly relevant jobs found. Try broadening your query.")
else:
    print(f"\n🔎 Top matching jobs (after hybrid scoring):\n")
    for i, job in enumerate(scored_results, 1):
        print(f"[{i}] ✅ {job['title']}\n🔗 {job['url']}\n📏 Distance: {job['distance']:.4f} | 🧠 Score: {job['score']}\n")
    print(f"\n✅ Displayed {len(scored_results)} re-ranked results.")
