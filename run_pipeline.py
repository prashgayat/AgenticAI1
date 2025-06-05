# run_pipeline.py – Full Pipeline: Steps 1–7

from search_jobs import run_search_pipeline
from agents import crew

print("\n🧲 STEP 1–3: Running job search pipeline...")
run_search_pipeline("LangChain, Make.com, automation")

print("\n🤖 STEP 4–7: Launching autonomous agent loop...")

try:
    result = crew.kickoff()
except IndexError:
    print("⚠️ Agent loop finished, but no tools were called. Likely no valid jobs or empty input.")
    result = "No tool actions executed."

print("\n🎯 Final Result:\n", result)
