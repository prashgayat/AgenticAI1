# launcher.py (fixed)

from dotenv import load_dotenv
load_dotenv()

import os
from agents import crew

def main():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("❌ OPENAI_API_KEY not loaded")
        return

    print("🚀 Running Agentic Job Search Crew...")
    final_output = crew.kickoff()
    print("\n✅ Crew completed! Final Output:\n")
    print(final_output)

if __name__ == "__main__":
    main()
