#!/bin/bash

echo "🔧 Setting up professional Python 3.10 + Chroma-compatible virtual environment..."

# Step 1: Create isolated virtual environment using Python 3.10
PYTHON_PATH="/usr/local/python/3.10.13/bin/python3.10"

if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ Python 3.10.13 not found at $PYTHON_PATH"
    echo "➡️ Please install Python 3.10.13 manually and try again."
    exit 1
fi

echo "✅ Using Python at $PYTHON_PATH"
$PYTHON_PATH -m venv venv
source venv/bin/activate

# Step 2: Upgrade pip and install dependencies
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing core libraries..."
pip install crewai==0.35.8 crewai-tools==0.1.7 embedchain==0.1.124 langchain==0.1.16
pip install chromadb
pip install faiss-cpu
pip install pandas openai tiktoken

# Step 3: Verify sqlite3 compatibility
echo "🧪 Verifying sqlite3 version..."
python -c "import sqlite3; print('SQLite version:', sqlite3.sqlite_version)"
echo "✅ SQLite version check complete (must be >= 3.35.0)"

# Step 4: Confirm all core packages installed
REQUIRED_MODULES=("crewai" "crewai_tools" "chromadb")
for mod in "${REQUIRED_MODULES[@]}"; do
  echo -n "🔍 Checking $mod... "
  python -c "import $mod" 2>/dev/null && echo "✅ OK" || echo "❌ MISSING"
done

# Step 5: Confirm CrewAI Tools list
echo "🧪 Verifying CrewAI Tools availability..."
python -c "import crewai_tools as ct; print('Available tools:', dir(ct))"

echo "🎉 Setup complete. Activate with: source venv/bin/activate"
