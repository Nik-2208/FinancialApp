import joblib
import numpy as np

# Load pre-trained fraud detection model
model = joblib.load("app/services/fraud_model.pkl")

def predict_fraud(transaction_amount: float, account_balance: float, transaction_time: int) -> bool:
    """Predict fraud based on transaction features"""
    features = np.array([[transaction_amount, account_balance, transaction_time]])
    prediction = model.predict(features)
    return bool(prediction[0])
