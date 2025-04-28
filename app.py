from flask import Flask, request, jsonify
from src.predict import FraudPredictor
from datetime import datetime
from src.config import AppConfig
import os

app = Flask(__name__)

# Initialize predictor with test mode if MODEL_PATH doesn't exist
try:
    predictor = FraudPredictor(test_mode=not os.path.exists('models/fraud_model.joblib'))
    print("ℹ️ Predictor initialized in test mode" if predictor.test_mode else "✅ Predictor initialized with model")
except Exception as e:
    print(f"❌ Failed to initialize predictor: {str(e)}")
    raise

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON provided"}), 400
            
        request_meta = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": "predict",
            "client_ip": request.remote_addr
        }
        
        prediction = predictor.predict(data)
        
        return jsonify({
            "fraud_prediction": prediction,
            "meta": request_meta,
            "model_info": {
                "version": "1.0.0",
                "type": "RandomForest",
                "test_mode": predictor.test_mode
            },
            "status": "success"
        })
        
    except ValueError as e:
        return jsonify({"error": str(e), "status": "input_error"}), 400
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