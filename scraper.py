# scraper.py (Final version: keyword-safe, fallback proof, Upwork-ready)

import csv

def run_scraper(keywords):
    print(f"🔍 Running job scraper for query: {keywords}")
    try:
        # Convert keywords to lowercase list (handles string or list input)
        if isinstance(keywords, str):
            keyword_list = [kw.strip().lower() for kw in keywords.replace(",", " ").split()]
        else:
            keyword_list = [kw.strip().lower() for kw in keywords]

        jobs = []
        with open("job_data.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "").strip()
                description = row.get("description", "").strip()
                url = row.get("url") or row.get("link") or "N/A"

                # Case-insensitive keyword match in title + description
                full_text = (title + " " + description).lower()
                if any(kw in full_text for kw in keyword_list):
                    jobs.append({
                        "title": title,
                        "description": description,
                        "url": url
                    })

        # If no matches, fallback to top 3 entries
        if not jobs:
            print("⚠ No matching jobs found. Returning top 3 fallback entries.")
            with open("job_data.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                jobs = []
                for i, row in enumerate(reader):
                    if i >= 3:
                        break
                    jobs.append({
                        "title": row.get("title", "").strip(),
                        "description": row.get("description", "").strip(),
                        "url": row.get("url") or row.get("link") or "N/A"
                    })

        return jobs[:3]

    except Exception as e:
        print(f"❌ Error reading job_data.csv: {e}")
        return [
            {
                "title": "LangChain Developer",
                "description": "Mock fallback job due to CSV read error.",
                "url": "https://example.com"
            }
        ]
