# test_hybrid_rank.py

from utils.scorer import score_job

# 🔧 Mock FAISS search results (index, distance)
faiss_results = [
    (0, 0.12),
    (1, 0.29),
    (2, 0.10)
]

# 🔧 Dummy job descriptions for each FAISS index
job_descriptions = [
    "Looking for a LangChain and OpenAI expert to build a chatbot using Streamlit.",
    "Need help with OCR on scanned PDFs. Python and EasyOCR skills preferred.",
    "Seeking a RAG pipeline engineer using Pinecone and GPT-4 APIs."
]

# Optional: job metadata for display
job_titles = [
    "LangChain Chatbot Developer",
    "OCR Preprocessing Script",
    "RAG Workflow Engineer"
]
job_urls = [
    "https://upwork.com/job/1",
    "https://upwork.com/job/2",
    "https://upwork.com/job/3"
]

# ✅ Score and rank
scored_results = []
for idx, distance in faiss_results:
    score = score_job(idx, distance, job_descriptions)
    scored_results.append({
        "title": job_titles[idx],
        "url": job_urls[idx],
        "distance": round(distance, 4),
        "score": score
    })

# ✅ Sort by hybrid score (descending)
scored_results.sort(key=lambda x: x['score'], reverse=True)

# ✅ Display results (same format as search_jobs_ranked.py)
print("🔍 💡 Top matching jobs (after hybrid scoring):\n")
for i, job in enumerate(scored_results, 1):
    print(f"[{i}] ✅ {job['title']}")
    print(f"🔗 {job['url']}")
    print(f"📏 Distance: {job['distance']} | 💬 Score: {job['score']}\n")

print(f"✅ Displayed {len(scored_results)} re-ranked results.")
