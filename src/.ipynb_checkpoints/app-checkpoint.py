from flask import Flask, request, jsonify
from src.predict import FraudPredictor
from datetime import datetime
from src.config import AppConfig
import os

app = Flask(__name__)

# Initialize predictor with explicit test mode in CI
is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
predictor = FraudPredictor(test_mode=is_ci or not os.path.exists('models/fraud_model.joblib'))

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
                "test_mode": predictor.test_mode
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
        "model_loaded": not predictor.test_mode
    })

if __name__ == '__main__':
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)