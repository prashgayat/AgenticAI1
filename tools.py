# tools.py

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, List
import json
import csv
import os


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
        ranked_jobs = score_and_rank_jobs(jobs)
        return ranked_jobs

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")


# === 2. Job Evaluator Tool ===

class JobEvaluationInput(BaseModel):
    job: str
    distance: float
    score: float


class JobEvaluatorTool(BaseTool):
    name: str = "Job Evaluator Tool"
    description: str = "Evaluate a job listing based on distance and score"
    args_schema: Type[BaseModel] = JobEvaluationInput

    def _run(self, job: str, distance: float, score: float):
        # Simple evaluation rule
        if distance < 1.5 and score > 0.1:
            return f"{job} is highly suitable"
        elif distance < 2.0:
            return f"{job} is moderately suitable"
        else:
            return f"{job} is not very relevant"
    
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")


# === 3. Proposal Generator Tool ===

class ProposalInput(BaseModel):
    job_description: str
    job_link: str
    freelancer_skills: Optional[str] = None


class ProposalTool(BaseTool):
    name: str = "Proposal Generator Tool"
    description: str = "Generate a proposal for a given job"
    args_schema: Type[BaseModel] = ProposalInput

    def _run(self, job_description: str, job_link: str, freelancer_skills: Optional[str] = None):
        return (
            "Hi, I'm experienced in building LangChain/RAG pipelines and "
            f"can help you develop the AI system for 'Untitled Project'."
        )

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")


# === 4. Memory Logger Tool ===

class MemoryInput(BaseModel):
    job_title: str
    job_link: str
    proposal: str
    application_status: Optional[str] = "applied"


class MemoryTool(BaseTool):
    name: str = "Memory Tool"
    description: str = "Log job and proposal data to persistent storage"
    args_schema: Type[BaseModel] = MemoryInput

    def _run(self, job_title: str, job_link: str, proposal: str, application_status: Optional[str] = "applied"):
        os.makedirs("memory", exist_ok=True)
        entry = {
            "job_title": job_title,
            "job_link": job_link,
            "proposal": proposal,
            "status": application_status
        }

        # Append to JSON
        json_path = os.path.join("memory", "memory_log.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                memory_data = json.load(f)
        else:
            memory_data = []

        memory_data.append(entry)
        with open(json_path, "w") as f:
            json.dump(memory_data, f, indent=2)

        # Append to CSV
        csv_path = os.path.join("memory", "memory_log.csv")
        write_header = not os.path.exists(csv_path)
        with open(csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["job_title", "job_link", "proposal", "status"])
            if write_header:
                writer.writeheader()
            writer.writerow(entry)

        return f"✅ Logged job: {job_title}"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")
