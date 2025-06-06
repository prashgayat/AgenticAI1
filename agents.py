# agents.py

from crewai import Agent, Crew, Task
from tools import JobSearchTool, JobEvaluatorTool, ProposalTool, MemoryTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Set up LLM using GPT-3.5
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Agent 1: Scout Agent
scout_agent = Agent(
    role="Job Scout",
    goal="Identify the best freelance job opportunities in AI and automation",
    backstory="Expert at exploring platforms like Upwork to find quality projects for AI professionals.",
    tools=[JobSearchTool],
    verbose=True,
    llm=llm,
)

# Agent 2: Evaluator Agent
evaluator_agent = Agent(
    role="Job Evaluator",
    goal="Evaluate and score freelance jobs based on quality, payout, and relevance",
    backstory="Data-driven agent who analyzes each opportunity deeply before recommending.",
    tools=[JobEvaluatorTool],
    verbose=True,
    llm=llm,
)

# Agent 3: Proposal Writer Agent
writer_agent = Agent(
    role="Proposal Writer",
    goal="Write tailored, compelling proposals to win freelance jobs",
    backstory="Creative communicator skilled in persuasive writing for Upwork proposals.",
    tools=[ProposalTool],
    verbose=True,
    llm=llm,
)

# Agent 4: Memory Logger Agent
memory_agent = Agent(
    role="Memory Logger",
    goal="Log applied jobs and proposals for tracking and learning",
    backstory="Meticulous tracker that ensures all actions are saved in memory logs.",
    tools=[MemoryTool],
    verbose=True,
    llm=llm,
)

# Final Crew Assembly
crew = Crew(
    agents=[scout_agent, evaluator_agent, writer_agent, memory_agent],
    tasks=[],
    verbose=True,
)
