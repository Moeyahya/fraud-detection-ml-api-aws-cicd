import pandas as pd
import numpy as np
from src.config import AMOUNT_PERCENTILE, BALANCE_PERCENTILE

def engineer_features(df):
    """Feature engineering pipeline"""
    # Transaction features
    amt_thresh = df[df['isFraud']==0]['amount'].quantile(AMOUNT_PERCENTILE)
    bal_thresh = df[df['isFraud']==0]['oldbalanceOrg'].quantile(BALANCE_PERCENTILE)
    
    df['amount_to_balance'] = df['amount'] / (df['oldbalanceOrg'] + 1)
    df['high_amount_flag'] = (df['amount'] > amt_thresh).astype(int)
    df['balance_change_abs'] = df['oldbalanceOrg'] - df['newbalanceOrig']
    df['suspicious_withdrawal'] = (
        (df['balance_change_abs'] > bal_thresh) & 
        (df['amount_to_balance'] > 0.5)
    ).astype(int)
    
    # Time features
    df['hour_of_day'] = ((df['step'] - 1) % 24) + 1
    df['day_of_week'] = ((df['step'] - 1) // 24) % 7
    df['is_weekend'] = ((df['day_of_week'] == 5) | (df['day_of_week'] == 6)).astype(int)
    
    # Categorical encoding
    df = pd.get_dummies(df, columns=['type'], prefix='type')
    
    return df