import pandas as pd
from sklearn.preprocessing import PowerTransformer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from src.config import DATA_PATH, N_ROWS, TEST_SIZE, RANDOM_STATE, SMOTE_RATIO
from src.feature_engineer import engineer_features

def load_and_preprocess():
    """Load and preprocess data with proper error handling"""
    try:
        print(f"Loading data from: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH, nrows=N_ROWS)
        
        print("Applying feature engineering...")
        df = engineer_features(df)
        
        X = df.drop(['isFraud', 'nameOrig', 'nameDest'], axis=1)
        y = df['isFraud']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
        
        # Scaling
        pt = PowerTransformer(method='yeo-johnson')
        X_train_scaled = pt.fit_transform(X_train)
        X_test_scaled = pt.transform(X_test)
        
        # Resampling
        smote = SMOTE(sampling_strategy=SMOTE_RATIO, random_state=RANDOM_STATE)
        X_res, y_res = smote.fit_resample(X_train_scaled, y_train)
        
        return X_res, y_res, X_test_scaled, y_test, pt
        
    except Exception as e:
        print(f"Error in preprocessing: {str(e)}")
        raise