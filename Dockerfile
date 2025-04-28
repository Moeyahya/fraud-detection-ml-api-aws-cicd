FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY app.py .
COPY config.py .

# Create directories
RUN mkdir -p /app/models /app/logs

# Environment variables
ENV MODEL_PATH=/app/models/fraud_model.joblib
ENV FLASK_APP=app.py
ENV PYTHONPATH=/app

# Copy model file (if exists)
COPY models/fraud_model.joblib /app/models/ || echo "No model file found, will run in test mode"

EXPOSE 8080
CMD ["python", "-c", "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=8080)"]