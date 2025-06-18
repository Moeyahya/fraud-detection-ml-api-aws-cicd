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

# Create data directory and copy sample data
RUN mkdir -p /app/data
COPY data/sample_fraud.csv /app/data/

# Copy model file (must exist in build context)
COPY models/fraud_model.joblib /app/models/

# Environment variables
ENV MODEL_PATH=/app/models/fraud_model.joblib
ENV FLASK_APP=app.py
ENV PYTHONPATH=/app

EXPOSE 8080
CMD ["python", "-c", "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=8080)"]