# quick_test_tool.py

from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables

from tools import JobSearchTool

tool = JobSearchTool()

result = tool._run("LangChain, GenAI")
print("\n🧠 Tool Output:\n", result)
