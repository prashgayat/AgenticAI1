# run_pipeline.py – Step 4–7: Agentic AI Job Search Agent
import os
from dotenv import load_dotenv
from agents import crew

# === Load API keys and environment variables ===
load_dotenv()

print("\n🤖 STEP 4–7: Launching autonomous agent loop...")

try:
    result = crew.kickoff()
except IndexError:
    print("⚠️ Agent loop finished, but no tools were called. Likely no valid jobs or empty input.")
    result = "No tool actions executed."
except Exception as e:
    print(f"❌ Unexpected error during agent loop: {e}")
    result = str(e)

print("\n🎯 Final Result:\n", result)
