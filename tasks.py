# tasks.py – Defines 4 discrete tasks for the CrewAI pipeline

from crewai import Task
from agents import ScoutAgent, EvaluatorAgent, WriterAgent, MemoryAgent

# 🔍 Task 1: Scout jobs
scout_task = Task(
    description="Use Job Search Tool to find latest Upwork jobs involving LangChain, RAG, or automation tools like Make.com.",
    expected_output="A list of 3–5 relevant job postings with title, link, distance, and score.",
    agent=ScoutAgent
)

# 🧠 Task 2: Evaluate jobs
evaluator_task = Task(
    description="Evaluate each job based on relevance, budget, clarity, and tech stack. Assign a hybrid fit score.",
    expected_output="A list of evaluated jobs with score and reason for ranking.",
    agent=EvaluatorAgent
)

# ✍️ Task 3: Write proposals
writer_task = Task(
    description="Write tailored proposals for the top-ranked jobs using Proposal Generator Tool.",
    expected_output="A list of proposals mapped to each job title.",
    agent=WriterAgent
)

# 💾 Task 4: Save to memory
memory_task = Task(
    description="Store the final shortlisted jobs and proposals in memory using MemoryTool for future reference and follow-up.",
    expected_output="Job metadata and proposal logged into memory_log.json and memory_log.csv.",
    agent=MemoryAgent
)
