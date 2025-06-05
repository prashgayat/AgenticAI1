# main.py

from dotenv import load_dotenv
load_dotenv()  # Load .env variables, including OPENAI_API_KEY

from crew_config import freelance_crew

def run_freelance_assistant():
    print("\n🚀 Running Freelance Project Finder Agent Crew...\n")

    # Start the multi-agent crew process using the updated method
    results = freelance_crew.kickoff()

    # Print all results
    print("\n📋 Final Output:\n")
    for result in results:
        print(result)
        print("-" * 80)

if __name__ == "__main__":
    run_freelance_assistant()
