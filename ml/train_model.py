import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, log_loss
import joblib


def train_model():
    df = pd.read_csv("data/training_data.csv")

    features = [
        "current_score",
        "wickets_lost",
        "balls_left",
        "runs_left",
        "current_run_rate",
        "required_run_rate",
        "wickets_remaining"
    ]

    df = df.dropna()

    X = df[features]
    y = df["result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    base_model = RandomForestClassifier(n_estimators=150, random_state=42)
    model = CalibratedClassifierCV(base_model, method='sigmoid', cv=3)

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print("Log Loss:", log_loss(y_test, probs))

    joblib.dump(model, "models/model.pkl")
    joblib.dump(features, "models/features.pkl")

    print("Calibrated model saved successfully.")


if __name__ == "__main__":
    train_model()
