# src/predict.py
from joblib import load
import pandas as pd
from src.config import MODEL_PATH, AppConfig
import json
from datetime import datetime
import logging
import os

class FraudPredictor:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.model = None
        self.pt = None
        self.feature_order = []
        self._init_logging()
        
        if not test_mode:
            try:
                self._load_model()
            except Exception as e:
                print(f"⚠️ Failed to load model: {str(e)}")
                # Fallback to test mode if model loading fails
                self.test_mode = True

    def _load_model(self):
        """Load model artifacts with validation"""
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            
        artifacts = load(MODEL_PATH)
        
        # Validate all required components exist
        required_keys = {'model', 'transformer', 'feature_order'}
        missing_keys = required_keys - set(artifacts.keys())
        if missing_keys:
            raise ValueError(f"Missing required keys in model file: {missing_keys}")
            
        self.model = artifacts['model']
        self.pt = artifacts['transformer']
        self.feature_order = artifacts.get('feature_order', [])
        
        print("✅ Model loaded successfully")
        print(f"Model trained on: {artifacts.get('metadata', {}).get('training_date', 'unknown')}")

    def _init_logging(self):
        """Set up prediction logging"""
        os.makedirs(os.path.dirname(AppConfig.PREDICTION_LOGS), exist_ok=True)
        logging.basicConfig(
            filename=AppConfig.PREDICTION_LOGS,
            format='%(asctime)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def _validate_input(self, data: dict) -> None:
        """Ensure minimum required fields exist"""
        required_fields = {
            'amount', 'oldbalanceOrg', 'newbalanceOrig',
            'oldbalanceDest', 'newbalanceDest', 'step',
            'isFlaggedFraud', 'type'
        }
        missing = required_fields - set(data.keys())
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

    def log_prediction(self, data: dict, prediction: int):
        """Log prediction with context"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": {k: v for k, v in data.items() if k != 'type'},
            "prediction": prediction,
            "model_version": "1.0.0",
            "test_mode": self.test_mode
        }
        self.logger.info(json.dumps(log_entry))

    def preprocess(self, transaction_data: dict):
        """Recreate features EXACTLY as during training"""
        df = pd.DataFrame([transaction_data])
        
        # Feature engineering
        df['amount_to_balance'] = df['amount'] / (df['oldbalanceOrg'] + 1)
        df['high_amount_flag'] = (df['amount'] > 10000).astype(int)
        df['balance_change_abs'] = df['oldbalanceOrg'] - df['newbalanceOrig']
        df['suspicious_withdrawal'] = (
            (df['balance_change_abs'] > 5000) & 
            (df['amount_to_balance'] > 0.5)
        ).astype(int)
        
        # Time features
        df['hour_of_day'] = ((df['step'] - 1) % 24) + 1
        df['day_of_week'] = ((df['step'] - 1) // 24) % 7
        df['is_weekend'] = ((df['day_of_week'] == 5) | (df['day_of_week'] == 6)).astype(int)
        
        # Transaction type handling
        valid_types = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']
        for t in valid_types:
            df[f'type_{t}'] = 0
        if 'type' in df and df['type'].iloc[0] in valid_types:
            df[f'type_{df["type"].iloc[0]}'] = 1
            
        # Verify feature match
        missing = set(self.feature_order) - set(df.columns)
        if missing:
            raise ValueError(f"Missing features after processing: {missing}")
            
        return self.pt.transform(df[self.feature_order])

    def predict(self, transaction_data: dict) -> int:
        """Make a fraud prediction"""
        if self.test_mode:
            self.log_prediction(transaction_data, 0)
            return 0  # Dummy prediction in test mode
            
        try:
            self._validate_input(transaction_data)
            processed = self.preprocess(transaction_data)
            prediction = int(self.model.predict(processed)[0])
            self.log_prediction(transaction_data, prediction)
            return prediction
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")

# For testing the predictor directly
if __name__ == '__main__':
    predictor = FraudPredictor(test_mode=True)
    test_data = {
        "amount": 100,
        "oldbalanceOrg": 1000,
        "newbalanceOrig": 900,
        "oldbalanceDest": 500,
        "newbalanceDest": 600,
        "step": 1,
        "isFlaggedFraud": 0,
        "type": "TRANSFER"
    }
    print("Test prediction:", predictor.predict(test_data))