# agents.py

from crewai import Agent, Crew, Task
from tools import JobSearchTool, JobEvaluatorTool, ProposalTool, MemoryTool
from langchain_openai import ChatOpenAI
import os

# Define the LLM with GPT-3.5 instead of GPT-4
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Agent 1: Scout Agent - Finds and ranks jobs
scout_agent = Agent(
    role="Job Scout",
    goal="Identify the best freelance job opportunities in AI and automation",
    backstory=(
        "An expert in scouring job boards like Upwork to find opportunities that align "
        "with specific skill sets like LangChain, RAG, and GenAI."
    ),
    tools=[JobSearchTool],
    verbose=True,
    allow_delegation=True,
    llm=llm,
)

# Agent 2: Evaluator Agent - Evaluates and scores jobs
evaluator_agent = Agent(
    role="Job Evaluator",
    goal="Evaluate job listings based on skills, client rating, and payout potential",
    backstory=(
        "A highly analytical agent that scores jobs based on keyword and semantic relevance, "
        "client quality, and scope match."
    ),
    tools=[JobEvaluatorTool],
    verbose=True,
    allow_delegation=True,
    llm=llm,
)

# Agent 3: Proposal Writer Agent
writer_agent = Agent(
    role="Proposal Writer",
    goal="Draft compelling proposals tailored to the specific job and client needs",
    backstory=(
        "An articulate and persuasive communicator that crafts customized proposals "
        "with a high chance of success."
    ),
    tools=[ProposalTool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

# Agent 4: Memory Logger Agent
memory_agent = Agent(
    role="Memory Logger",
    goal="Log every job applied to along with the proposal details for future tracking",
    backstory=(
        "A meticulous recorder who ensures no opportunity is forgotten. Keeps records "
        "clean, organized, and reusable."
    ),
    tools=[MemoryTool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

# Create the crew
crew = Crew(
    agents=[scout_agent, evaluator_agent, writer_agent, memory_agent],
    tasks=[],
    verbose=True,
)
