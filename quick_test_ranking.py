# quick_test_ranking.py

from dotenv import load_dotenv
load_dotenv()  # ✅ Load your OPENAI_API_KEY from .env

from scraper import run_scraper
from utils.ranker import score_and_rank_jobs

keywords = ["LangChain", "GenAI"]
print(f"🔍 Fetching jobs for: {keywords}")
jobs = run_scraper(keywords)

print(f"📊 Ranking {len(jobs)} job(s)...")
ranked_jobs = score_and_rank_jobs(jobs, keywords)  # ✅ Fix: pass both args

print("✅ Ranked Jobs:")
for job in ranked_jobs:
    print(job)
