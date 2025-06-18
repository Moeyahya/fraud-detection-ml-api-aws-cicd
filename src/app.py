from flask import Flask, request, jsonify
from src.predict import FraudPredictor
from datetime import datetime
from src.config import AppConfig
import os
from pathlib import Path

app = Flask(__name__)

def get_model_path():
    """Resolve model path for both development and Docker environments"""
    # Try multiple possible locations
    possible_paths = [
        Path('models/fraud_model.joblib'),  # Development
        Path('/app/models/fraud_model.joblib'),  # Docker
        Path(__file__).parent.parent / 'models' / 'fraud_model.joblib'  # Relative to app
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    return None

def get_data_path():
    """Resolve data file path"""
    possible_paths = [
        Path('data/sample_fraud.csv'),  # Development
        Path('/app/data/sample_fraud.csv'),  # Docker
        Path(__file__).parent.parent / 'data' / 'sample_fraud.csv'  # Relative to app
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    return None

# Initialize predictor with proper paths
model_path = get_model_path()
data_path = get_data_path()

is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
predictor = FraudPredictor(
    test_mode=is_ci or not model_path,
    model_path=model_path,
    data_path=data_path
)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON provided"}), 400
            
        # Validate required fields
        required_fields = {
            'amount', 'oldbalanceOrg', 'newbalanceOrig',
            'oldbalanceDest', 'newbalanceDest', 'step',
            'isFlaggedFraud', 'type'
        }
        missing = required_fields - set(data.keys())
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}", "status": "input_error"}), 400

        prediction = predictor.predict(data)
        
        return jsonify({
            "fraud_prediction": prediction,
            "model_info": {
                "version": "1.0.0",
                "type": "RandomForest",
                "test_mode": predictor.test_mode,
                "model_used": str(model_path) if model_path else "none",
                "data_used": str(data_path) if data_path else "none"
            },
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "server_error"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": not predictor.test_mode,
        "model_path": str(model_path) if model_path else "none",
        "data_path": str(data_path) if data_path else "none"
    })

if __name__ == '__main__':
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)