import joblib
import numpy as np

# Load the trained model
model = joblib.load("model.pkl")

def predict_pm25(aod_value):
    """Predict PM2.5 based on AOD value"""
    aod_array = np.array(aod_value).reshape(-1, 1)
    pm25 = model.predict(aod_array)
    return pm25[0]
