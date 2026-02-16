import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
import joblib
import os


def train_model():
    # Load dataset
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

    # Logistic Regression (lightweight + good for probability)
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print("Log Loss:", log_loss(y_test, probs))

    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/model.pkl")
    joblib.dump(features, "models/features.pkl")

    print("Model saved successfully.")


if __name__ == "__main__":
    train_model()
