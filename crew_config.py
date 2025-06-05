# Upgraded crew_config.py

from crewai import Crew, Process
from agents import (
    ScoutAgent,
    EvaluatorAgent,
    WriterAgent,
    MemoryAgent
)
from tasks import (
    scout_task,
    evaluator_task,
    writer_task,
    memory_task
)
from tools import (
    JobSearchTool,
    JobEvaluatorTool,
    ProposalTemplateTool,
    MemoryTool
)

# Initialize tools
search_tool = JobSearchTool(
    keywords=[
        # Mentor 2 stack
        "Make.com", "Retell AI", "Chatling", "n8n", "Airtable", "bolt.new",

        # Mentor 1 stack (core LLM/RAG/ML)
        "Langchain", "LlamaIndex", "Pinecone", "ChromaDB", "Streamlit",
        "OpenAI", "HuggingFace", "RAG", "LLM fine-tuning", "LoRA", "QLoRA",
        "BERT", "RoBERTa", "NER", "Sentiment Analysis",
        "Docker", "AWS Bedrock", "SageMaker",
        "CNN", "YOLO", "OpenCV", "XGBoost"
    ]
)

eval_tool = JobEvaluatorTool(
    preferences={
        "low_applicants": True,
        "budget_minimum": 100,
        "job_age_days_max": 5,
        "no_code_priority": True  # give Make.com etc. higher score for breakthrough
    }
)

template_tool = ProposalTemplateTool(
    modes=["no_code_pitch", "genai_agent_pitch"]
)

memory_tool = MemoryTool()

# Assign tools to each agent
ScoutAgent.tools = [search_tool]
EvaluatorAgent.tools = [eval_tool]
WriterAgent.tools = [template_tool, memory_tool]
MemoryAgent.tools = [memory_tool]

# Build the upgraded crew
freelance_crew = Crew(
    agents=[
        ScoutAgent,
        EvaluatorAgent,
        WriterAgent,
        MemoryAgent
    ],
    tasks=[
        scout_task,
        evaluator_task,
        writer_task,
        memory_task
    ],
    process=Process.sequential,
    verbose=True
)
