# perplexity_scraper.py
import requests
from bs4 import BeautifulSoup

class PerplexityJobScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.search_url = "https://www.perplexity.ai/search"

    def fetch_jobs(self, query_keywords):
        query = f"site:upwork.com {' OR '.join(query_keywords)}"
        response = requests.get(f"https://www.perplexity.ai/search?q={query}", headers=self.headers)
        
        if response.status_code != 200:
            print("Failed to fetch search results.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        job_list = []

        for link in soup.find_all("a", href=True):
            url = link["href"]
            if "upwork.com" in url and "/jobs/" in url:
                title = link.get_text().strip()
                if title:
                    job_list.append({
                        "title": title,
                        "description": "No description available (scraped via Perplexity)",
                        "url": url,
                        "budget": 0,
                        "days_old": 0,
                        "applicants": 0,
                        "client_name": "Unknown"
                    })

        return job_list

# Example Usage
if __name__ == "__main__":
    scraper = PerplexityJobScraper()
    results = scraper.fetch_jobs(["Make.com", "Chatling", "Langchain", "Retell AI", "n8n"])
    for job in results:
        print(job)
