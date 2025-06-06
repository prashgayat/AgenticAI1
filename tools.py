# tools.py

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, List
import json
import csv
import os


# =========================
# Pydantic JobPosting Model
# =========================

class JobPosting(BaseModel):
    title: str
    description: str
    link: str
    score: float
    distance: float


# =========================
# 1. Job Search Tool
# =========================

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
        return [job.dict() for job in ranked_jobs]  # Return list of dicts


# =========================
# 2. Job Evaluator Tool
# =========================

class JobEvaluationInput(BaseModel):
    job: str = Field(..., description="JSON stringified job object")
    score: float
    distance: float


class JobEvaluatorTool(BaseTool):
    name: str = "Job Evaluator Tool"
    description: str = "Evaluates the job relevance using semantic and keyword match score"
    args_schema: Type[BaseModel] = JobEvaluationInput

    def _run(self, job: str, score: float, distance: float):
        job_data = json.loads(job)
        title = job_data.get("title", "Unknown Job")
        return f"The job '{title}' has a relevance score of {score} (distance: {distance})."


# =========================
# 3. Proposal Writer Tool
# =========================

class ProposalInput(BaseModel):
    job_title: str
    job_description: str


class ProposalTool(BaseTool):
    name: str = "Proposal Writer Tool"
    description: str = "Generates a freelance proposal for the given job"
    args_schema: Type[BaseModel] = ProposalInput

    def _run(self, job_title: str, job_description: str):
        return (
            f"Dear Client,\n\n"
            f"I am excited to apply for the {job_title}. With experience in similar projects, I believe I can "
            f"deliver exceptional results tailored to your needs. My approach is solution-oriented and client-focused.\n\n"
            f"Let's connect to discuss your goals in more detail.\n\n"
            f"Best regards,\n"
            f"Gayatri"
        )


# =========================
# 4. Memory Logger Tool
# =========================

class MemoryLogInput(BaseModel):
    job_title: str
    job_link: str
    proposal: str
    application_status: str = "applied"


class MemoryTool(BaseTool):
    name: str = "Memory Logger Tool"
    description: str = "Logs applied jobs and proposals for record keeping"
    args_schema: Type[BaseModel] = MemoryLogInput

    def _run(self, job_title: str, job_link: str, proposal: str, application_status: str = "applied"):
        record = {
            "job_title": job_title,
            "job_link": job_link,
            "proposal": proposal,
            "application_status": application_status
        }

        os.makedirs("memory", exist_ok=True)

        # JSON logging
        json_path = "memory/memory_log.json"
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(record)
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        # CSV logging
        csv_path = "memory/memory_log.csv"
        file_exists = os.path.isfile(csv_path)
        with open(csv_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["job_title", "job_link", "proposal", "application_status"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)

        return f"Logged job '{job_title}' with status '{application_status}'."
