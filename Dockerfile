# Multi-stage Dockerfile for AI-Assisted Telemedicine Kiosk
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Initialize ML model & DB
RUN python ml/train_model.py && python -c "import database.database as db; db.init_db()"

# Expose ports: 8501 for Streamlit Frontend, 5000 for Flask REST API
EXPOSE 8501 5000

# Default entrypoint starts Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
