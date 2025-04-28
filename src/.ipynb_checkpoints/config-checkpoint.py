from pathlib import Path
from datetime import datetime
import os
import sys

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent

# Data configuration
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Try these data files in order (first found will be used)
DATA_PATHS = [
    DATA_DIR / 'sample_fraud.csv',  # Small sample for CI/testing (should be committed)
    DATA_DIR / 'Fraud.csv',        # Full dataset for local development (gitignored)
    Path(r'C:\Projects\fraud_detection\data\Fraud.csv')  # Fallback to original location
]

DATA_PATH = None
for path in DATA_PATHS:
    if path.exists():
        DATA_PATH = path
        break

if DATA_PATH is None:
    print("\nERROR: No suitable data file found. Please:", file=sys.stderr)
    print("1. Add 'sample_fraud.csv' to project's data/ folder for testing", file=sys.stderr)
    print("2. Or add 'Fraud.csv' to project's data/ folder for development", file=sys.stderr)
    print(f"3. Or keep original at C:\\Projects\\fraud_detection\\data\\Fraud.csv", file=sys.stderr)
    print("\nCreating empty data directory...", file=sys.stderr)
    (DATA_DIR / '.gitkeep').touch()
    sys.exit(1)

print(f"\nℹ️ Using data file at: {DATA_PATH}")

# Model configuration
MODEL_DIR = PROJECT_ROOT / 'models'
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / 'fraud_model.joblib'

# Logs configuration
LOG_DIR = PROJECT_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Data processing parameters
N_ROWS = None  # Set to None to use all rows, or specify a number (e.g., 100000)
AMOUNT_PERCENTILE = 0.95
BALANCE_PERCENTILE = 0.9

# Model training parameters
RANDOM_STATE = 42
TEST_SIZE = 0.3
SMOTE_RATIO = 0.3

class AppConfig:
    # API Settings
    HOST = "0.0.0.0"
    PORT = 8080
    DEBUG = False
    
    # Model Monitoring
    PREDICTION_LOGS = LOG_DIR / "predictions.log"
    DRIFT_THRESHOLD = 0.15
    
    # Performance
    MAX_REQUEST_SIZE = 1024 * 1024  # 1MB
    
    @classmethod
    def validate_paths(cls):
        """Ensure all required directories exist"""
        required_dirs = [
            DATA_DIR,
            MODEL_DIR,
            LOG_DIR
        ]
        for directory in required_dirs:
            directory.mkdir(exist_ok=True)
            
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Data file not found at {DATA_PATH}")

# Initialize directories
AppConfig.validate_paths()

# Environment detection
IS_CI = os.getenv('CI') == 'true'
IS_TEST = os.getenv('TEST_MODE') == 'true'

if __name__ == '__main__':
    print("\nCurrent Configuration:")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data File: {DATA_PATH}")
    print(f"Model Path: {MODEL_PATH}")
    print(f"Log Directory: {LOG_DIR}")
    print(f"CI Mode: {IS_CI}")
    print(f"Test Mode: {IS_TEST}")