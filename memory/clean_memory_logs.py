# clean_memory_logs.py

import json
import csv
import os

json_path = "memory/memory_log.json"
csv_path = "memory/memory_log.csv"

# Clean memory_log.json
if os.path.exists(json_path):
    with open(json_path, "w") as jf:
        json.dump([], jf, indent=2)
    print("✅ Cleared memory_log.json")
else:
    print("⚠️ memory_log.json not found")

# Clean memory_log.csv
if os.path.exists(csv_path):
    with open(csv_path, "w", newline="") as cf:
        writer = csv.writer(cf)
        writer.writerow(["job_title", "job_link", "proposal", "application_status"])
    print("✅ Cleared memory_log.csv and wrote headers")
else:
    print("⚠️ memory_log.csv not found")
