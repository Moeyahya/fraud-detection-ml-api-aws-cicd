from waitress import serve
from app import app  # Import your Flask app
from src.config import PROJECT_ROOT
import os
import logging

# Production configuration
MODEL_DIR = PROJECT_ROOT / 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('waitress')
logger.info('Starting server...')

if __name__ == '__main__':
    print(f"🚀 Serving fraud detection API on http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080)  # Production-ready server