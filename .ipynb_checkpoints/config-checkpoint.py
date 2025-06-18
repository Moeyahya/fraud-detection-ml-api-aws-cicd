# config.py
from pathlib import Path
from datetime import datetime

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'Fraud.csv'
MODEL_PATH = PROJECT_ROOT / 'models' / 'fraud_model.joblib'

# Data loading
N_ROWS = 100000 

# Feature engineering
AMOUNT_PERCENTILE = 0.95
BALANCE_PERCENTILE = 0.9

# Model training
RANDOM_STATE = 42
TEST_SIZE = 0.3
SMOTE_RATIO = 0.3

class AppConfig:
    # API Settings
    HOST = "0.0.0.0"
    PORT = 8080
    DEBUG = False
    
    # Model Monitoring
    PREDICTION_LOGS = PROJECT_ROOT / "logs" / "predictions.log"
    DRIFT_THRESHOLD = 0.15

    @classmethod
    def ensure_dirs_exist(cls):
        """Create required directories"""
        (PROJECT_ROOT / "logs").mkdir(exist_ok=True)
        (PROJECT_ROOT / "models").mkdir(exist_ok=True)

# Initialize directories
AppConfig.ensure_dirs_exist()