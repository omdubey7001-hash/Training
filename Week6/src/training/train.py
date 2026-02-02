import pandas as pd
import numpy as np
import json
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

DATA_PATH = "src/data/processed/final.csv"
TARGET_COL = "class"   # ⚠️ must match Day-2 target
MODEL_PATH = "src/models/best_model.pkl"
METRICS_PATH = "src/evaluation/metrics.json"

def load_data():
    df = pd.read_csv(DATA_PATH)

    X = pd.get_dummies(df.drop(columns=[TARGET_COL]), drop_first=True)
    y = df[TARGET_COL].map({"bad": 0, "good": 1})

    # 🔑 SAVE FEATURE COLUMNS
    joblib.dump(X.columns.tolist(), "src/models/feature_columns.pkl")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y



def get_models():
    return {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(random_state=42),
        "NeuralNetwork": MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=42)
    }

def evaluate_models(X, y):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc"
    }

    results = {}
    best_model = None
    best_score = 0

    for name, model in get_models().items():
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring)
        avg_f1 = scores["test_f1"].mean()

        results[name] = {
            metric: scores[f"test_{metric}"].mean()
            for metric in scoring
        }

        if avg_f1 > best_score:
            best_score = avg_f1
            best_model = model

    return results, best_model

def save_outputs(results, best_model, X, y):
    with open(METRICS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    best_model.fit(X, y)
    joblib.dump(best_model, MODEL_PATH)

    print("Best model saved")
    print("Metrics saved")

def main():
    X, y = load_data()
    results, best_model = evaluate_models(X, y)
    save_outputs(results, best_model, X, y)

    print("\nModel Performance Summary:")
    for model, metrics in results.items():
        print(model, metrics)

if __name__ == "__main__":
    main()
