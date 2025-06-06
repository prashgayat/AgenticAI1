# agents.py

from crewai import Agent, Crew, Task
from tools import JobSearchTool, JobEvaluatorTool, ProposalTool, MemoryTool
from langchain_openai import ChatOpenAI
import os

# === Setup the LLM (GPT-3.5 for now to save cost) ===
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# === Agent 1: Scout Agent ===
scout_agent = Agent(
    role="Job Scout",
    goal="Identify the best freelance job opportunities in AI and automation",
    backstory="An expert in scouring job boards like Upwork to find opportunities aligned with LangChain, RAG, and GenAI.",
    llm=llm,
    tools=[JobSearchTool],
    verbose=True,
    allow_delegation=True,
)

# === Agent 2: Evaluator Agent ===
evaluator_agent = Agent(
    role="Job Evaluator",
    goal="Evaluate job listings based on skills, client rating, and payout potential",
    backstory="An analytical expert who scores jobs based on semantic relevance, keyword match, and project quality.",
    llm=llm,
    tools=[JobEvaluatorTool],
    verbose=True,
    allow_delegation=True,
)

# === Agent 3: Proposal Writer ===
writer_agent = Agent(
    role="Proposal Writer",
    goal="Draft compelling proposals tailored to the specific job and client needs",
    backstory="A persuasive communicator that writes tailored, high-converting freelance proposals.",
    llm=llm,
    tools=[ProposalTool],
    verbose=True,
    allow_delegation=False,
)

# === Agent 4: Memory Logger ===
memory_agent = Agent(
    role="Memory Logger",
    goal="Log every job applied to along with the proposal details for future tracking",
    backstory="A meticulous recorder who ensures all job applications are saved and reusable.",
    llm=llm,
    tools=[MemoryTool],
    verbose=True,
    allow_delegation=False,
)

# === Crew Definition ===
crew = Crew(
    agents=[scout_agent, evaluator_agent, writer_agent, memory_agent],
    tasks=[],  # Populated in run_pipeline.py
    verbose=True,
)
