import pandas as pd
from .model_loader import model, features
from .feature_builder import build_features


def predict_win_probability(input_data):
    processed_data = build_features(input_data)

    df = pd.DataFrame([processed_data])
    df = df[features]

    probability = model.predict_proba(df)[0]

    return {
        "win_probability": round(probability[1] * 100, 2),
        "lose_probability": round(probability[0] * 100, 2),
        "computed_features": processed_data
    }
