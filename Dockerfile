# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS-level dependencies (optional but useful)
RUN apt-get update && apt-get install -y build-essential

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose a port (optional — for future API or Streamlit)
EXPOSE 8000

# Run the app
CMD ["python", "main.py"]
