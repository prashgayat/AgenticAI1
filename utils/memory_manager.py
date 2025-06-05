# utils/memory_manager.py

import json
from pathlib import Path

MEMORY_PATH = Path("memory.json")

def load_memory():
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory_data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory_data, f, indent=2)
