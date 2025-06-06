# agents.py

from dotenv import load_dotenv
load_dotenv()

import os
from langchain.chat_models import ChatOpenAI
from crewai import Agent, Crew, Task
from tools import JobSearchTool, JobEvaluatorTool, ProposalTool, MemoryTool

# === LLM ===
llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",  # ✅ Switched from gpt-4 to gpt-3.5-turbo
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# === TOOLS ===
tools = [JobSearchTool(), JobEvaluatorTool(), ProposalTool(), MemoryTool()]

# === AGENTS ===
ScoutAgent = Agent(
    role="Job Scout",
    goal="Find the most relevant freelance jobs based on keyword filters and budget",
    backstory="You are an expert freelance job scout who knows how to find high-value and relevant jobs for a GenAI freelancer.",
    verbose=True,
    allow_delegation=True,
    tools=tools,
    llm=llm,
)

EvaluatorAgent = Agent(
    role="Job Evaluator",
    goal="Score and rank jobs based on semantic and keyword relevance",
    backstory="You're skilled at assessing freelance job quality and match potential using hybrid relevance metrics.",
    verbose=True,
    allow_delegation=True,
    tools=tools,
    llm=llm,
)

WriterAgent = Agent(
    role="Proposal Writer",
    goal="Write a compelling proposal for the best job match",
    backstory="You are a top-tier proposal writer with a knack for personalized and persuasive freelance proposals.",
    verbose=True,
    allow_delegation=False,
    tools=tools,
    llm=llm,
)

MemoryAgent = Agent(
    role="Memory Logger",
    goal="Save job details and proposals to persistent memory for tracking",
    backstory="You handle meticulous record-keeping of all applications made, proposals sent, and statuses.",
    verbose=True,
    allow_delegation=False,
    tools=tools,
    llm=llm,
)

# === TASKS ===
task1 = Task(
    description="Search for the latest freelance jobs on Upwork using keywords like 'LangChain', 'RAG', 'GenAI', 'automation tools', and 'no-code'. Return the top matches.",
    expected_output="A list of 3 shortlisted jobs relevant to GenAI and automation skills.",
    agent=ScoutAgent,
)

task2 = Task(
    description="Evaluate the shortlisted jobs based on semantic and keyword relevance. Rank them and select the best fit.",
    expected_output="The best-fit job among the list based on hybrid scoring criteria.",
    agent=EvaluatorAgent,
)

task3 = Task(
    description="Write a proposal tailored to the best-fit job selected by the Evaluator Agent.",
    expected_output="A compelling and concise proposal ready to submit on Upwork.",
    agent=WriterAgent,
)

task4 = Task(
    description="Save the job details and proposal into memory for record keeping and future tracking.",
    expected_output="Confirmation that the job, proposal, and status were saved into memory.",
    agent=MemoryAgent,
)

# === CREW ===
crew = Crew(
    agents=[ScoutAgent, EvaluatorAgent, WriterAgent, MemoryAgent],
    tasks=[task1, task2, task3, task4],
    verbose=True
)
