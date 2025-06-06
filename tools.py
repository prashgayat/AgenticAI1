# tools.py

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, List, Dict
import json
import csv
import os
from difflib import SequenceMatcher


# === 1. Job Search Tool ===

class JobSearchInput(BaseModel):
    keywords: Optional[List[str]] = Field(default=None, description="Search keywords for job retrieval")


class JobSearchTool(BaseTool):
    name: str = "Job Search Tool"
    description: str = "Search for relevant jobs based on keyword relevance and semantic distance"
    args_schema: Type[BaseModel] = JobSearchInput

    def _run(self, keywords: Optional[List[str]] = None):
        from scraper import run_scraper
        from utils.ranker import score_and_rank_jobs

        jobs = run_scraper(keywords)
        ranked_jobs = score_and_rank_jobs(jobs, keywords)
        return ranked_jobs


# === 2. Job Evaluator Tool ===

class SingleJobInput(BaseModel):
    job: Dict[str, str] = Field(..., description="A single job dict with 'title' and 'description'")


class JobEvaluatorTool(BaseTool):
    name: str = "Job Evaluator Tool"
    description: str = "Evaluates the job relevance using semantic and keyword match score"
    args_schema: Type[BaseModel] = SingleJobInput

    def _run(self, job: Dict[str, str]):
        title = job.get("title", "").lower()
        desc = job.get("description", "").lower()
        content = f"{title} {desc}"

        keywords = ["langchain", "rag", "genai", "automation tools", "no-code"]

        keyword_hits = sum(1 for k in keywords if k in content)
        keyword_score = keyword_hits / len(keywords)

        base_relevance = SequenceMatcher(None, title, desc).ratio()

        final_score = 0.6 * keyword_score + 0.4 * base_relevance

        return {
            "title": title,
            "score": round(final_score, 3),
            "keyword_hits": keyword_hits,
            "base_relevance": round(base_relevance, 3)
        }


# === 3. Proposal Writer Tool ===

class ProposalInput(BaseModel):
    job_title: str
    job_description: str


class ProposalTool(BaseTool):
    name: str = "Proposal Writer Tool"
    description: str = "Generate a tailored proposal based on job title and description"
    args_schema: Type[BaseModel] = ProposalInput

    def _run(self, job_title: str, job_description: str):
        proposal = f"""Dear Client,

I am excited to apply for the {job_title}. With experience in similar projects, I believe I can deliver exceptional results tailored to your needs. My approach is solution-oriented and client-focused.

Let's connect to discuss your goals in more detail.

Best regards,
Gayatri"""
        return proposal


# === 4. Memory Logger Tool ===

class MemoryLogInput(BaseModel):
    job_title: str
    job_link: str
    proposal: str


class MemoryTool(BaseTool):
    name: str = "Memory Logger Tool"
    description: str = "Logs applied jobs and proposals for record keeping"
    args_schema: Type[BaseModel] = MemoryLogInput

    def _run(self, job_title: str, job_link: str, proposal: str):
        memory_dir = "memory"
        os.makedirs(memory_dir, exist_ok=True)

        json_path = os.path.join(memory_dir, "memory_log.json")
        csv_path = os.path.join(memory_dir, "memory_log.csv")

        log_entry = {
            "job_title": job_title,
            "job_link": job_link,
            "proposal": proposal,
            "application_status": "applied"
        }

        # Append to JSON
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(log_entry)
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        # Append to CSV
        file_exists = os.path.exists(csv_path)
        with open(csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=log_entry.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)

        return f"Logged job '{job_title}' with status 'applied'."
