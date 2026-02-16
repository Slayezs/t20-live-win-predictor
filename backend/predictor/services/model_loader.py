import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "features.pkl")

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURE_PATH)

print("Model loaded successfully.")
