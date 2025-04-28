# src/train.py
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
from src.preprocess import load_and_preprocess
from src.config import MODEL_PATH, RANDOM_STATE
from sklearn.metrics import classification_report
import pandas as pd
import os

def train_model():
    print("🚀 Starting model training...")
    
    # Load and preprocess data
    print("🔍 Loading and preprocessing data...")
    X_res, y_res, X_test, y_test, pt = load_and_preprocess()
    
    # Initialize model
    print("🤖 Initializing Random Forest model...")
    model = RandomForestClassifier(
        class_weight='balanced',
        n_estimators=50,
        max_depth=7,
        max_samples=0.8,
        n_jobs=-1,
        random_state=RANDOM_STATE
    )
    
    # Train model
    print("⚡ Training model...")
    model.fit(X_res, y_res)
    
    # Evaluate
    print("🧪 Evaluating model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save ALL required artifacts
    artifacts = {
        'model': model,
        'transformer': pt,
        'feature_order': X_res.columns.tolist() if hasattr(X_res, 'columns') else [],
        'metadata': {
            'training_date': datetime.now().isoformat(),
            'git_commit': os.getenv('GIT_COMMIT', 'unknown'),
            'python_version': os.getenv('PYTHON_VERSION', 'unknown')
        }
    }
    
    dump(artifacts, MODEL_PATH)
    print(f"\n✅ Model successfully saved to {MODEL_PATH}")
    
if __name__ == '__main__':
    train_model()