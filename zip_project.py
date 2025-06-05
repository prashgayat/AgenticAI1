import zipfile
import os

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        # Exclude unwanted directories
        if any(x in root for x in ['venv', '__pycache__', '.git']):
            continue
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, path)
            ziph.write(filepath, arcname)

project_dir = "../AgenticAI1"  # Go up one level and point to full folder
output_zip = "AgenticAI_latest.zip"

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(project_dir, zipf)

print("✅ Zip completed.")
