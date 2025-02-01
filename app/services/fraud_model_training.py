import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Generate dummy transaction data
X = np.random.rand(1000, 3) * 10000  # Features: [amount, balance, time_of_day]
y = np.random.randint(0, 2, 1000)    # Labels: 0 for normal, 1 for fraud

# Train a Random Forest model
model = RandomForestClassifier()
model.fit(X, y)

# Save the trained model
joblib.dump(model, "app/services/fraud_model.pkl")
print("Fraud detection model trained and saved!")
