# agents.py – All 4 agents + crew task definition for Agentic AI Job Search Assistant

from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew
from tools import JobSearchTool, JobEvaluatorTool, ProposalTool, MemoryTool

# 🎯 Agent 1: ScoutAgent – fetches relevant freelance job listings
ScoutAgent = Agent(
    role="Job Scout",
    goal="Identify relevant GenAI freelance projects using job search tools",
    backstory=(
        "You're a scouting agent assisting an AI freelancer. Your mission is to scan freelance "
        "platforms like Upwork to discover jobs involving LangChain, RAG, or no-code tools."
    ),
    tools=[JobSearchTool()],
    verbose=True
)

# 🧠 Agent 2: EvaluatorAgent – re-ranks and filters based on fit
EvaluatorAgent = Agent(
    role="Job Evaluator",
    goal="Assess the relevance and quality of freelance job listings",
    backstory=(
        "You evaluate projects based on budget, scope, and tech stack relevance. Use hybrid scoring "
        "to prioritize high-fit opportunities."
    ),
    tools=[JobEvaluatorTool(), MemoryTool()],
    verbose=True
)

# 📝 Agent 3: WriterAgent – drafts proposals based on selected jobs
WriterAgent = Agent(
    role="Proposal Writer",
    goal="Write compelling proposals tailored to each client's job description",
    backstory=(
        "You're an AI copywriter trained to generate persuasive Upwork proposals that align with the job context "
        "and freelancer’s unique strengths. You switch tone based on the client's sophistication."
    ),
    tools=[ProposalTool()],
    verbose=True
)

# 💾 Agent 4: MemoryAgent – stores final leads and proposals
MemoryAgent = Agent(
    role="Memory Logger",
    goal="Store the best job leads and their tailored proposals for follow-up",
    backstory=(
        "You're responsible for saving high-quality job leads and the proposals written, so the freelancer can track "
        "what was applied to and revisit later."
    ),
    tools=[MemoryTool()],
    verbose=True
)

# 🧩 Define task for crew coordination
job_search_task = Task(
    description="Run a full GenAI job search and proposal generation pipeline using the agents.",
    agent=ScoutAgent,
    expected_output="Top matching jobs found, evaluated, proposed, and logged."
)

# 🧠 Crew: Orchestrates the full pipeline
crew = Crew(
    agents=[ScoutAgent, EvaluatorAgent, WriterAgent, MemoryAgent],
    tasks=[job_search_task],
    verbose=True
)
