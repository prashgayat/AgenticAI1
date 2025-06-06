# quick_test_scraper.py

from scraper import run_scraper

keywords = ["LangChain", "GenAI"]
print(f"🔍 Running job scraper for query: {keywords}")

results = run_scraper(keywords)
print(f"✅ Scraper returned {len(results)} jobs.")

for job in results:
    print(job)
