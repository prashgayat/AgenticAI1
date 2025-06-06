from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

def score_and_rank_jobs(jobs: List[dict], keywords: List[str]) -> List[dict]:
    if not jobs:
        print("⚠️ No jobs provided to score.")
        return []

    print(f"📊 Ranking {len(jobs)} job(s)...")

    query_text = " ".join(keywords).lower()
    job_texts = [f"{job['title']} {job['description']}".lower() for job in jobs]

    vectorizer = TfidfVectorizer().fit([query_text] + job_texts)
    query_vec = vectorizer.transform([query_text])
    job_vecs = vectorizer.transform(job_texts)

    cosine_scores = cosine_similarity(query_vec, job_vecs)[0]

    ranked = []
    for idx, job in enumerate(jobs):
        score = float(cosine_scores[idx])
        distance = 1 - score
        ranked.append({
            "title": job["title"],
            "description": job["description"],
            "link": job.get("url") or job.get("job_link") or "https://example.com",
            "score": round(score, 4),
            "distance": round(distance, 4)
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    print(f"✅ Ranked {len(ranked)} jobs.")
    return ranked
