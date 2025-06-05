# scraper.py (patched for job_data.csv compatibility)

import csv

def fetch_mock_jobs():
    return [
        {
            "title": "LangChain Chatbot Developer",
            "description": "Build a chatbot using LangChain, OpenAI, and Streamlit.",
            "url": "https://upwork.com/job/1"
        },
        {
            "title": "OCR Preprocessing Script",
            "description": "Python script to clean scanned PDFs and extract text using EasyOCR.",
            "url": "https://upwork.com/job/2"
        },
        {
            "title": "RAG Workflow Engineer",
            "description": "Need someone to build a Retrieval-Augmented Generation system using Pinecone and GPT-4.",
            "url": "https://upwork.com/job/3"
        }
    ]

def run_scraper(query):
    print(f"🔍 Running job scraper for query: {query}")
    jobs = fetch_mock_jobs()  # Replace this with your real scraper later

    with open("job_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "description", "url"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Saved {len(jobs)} job listings to job_data.csv")


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "LangChain"
    run_scraper(query)
