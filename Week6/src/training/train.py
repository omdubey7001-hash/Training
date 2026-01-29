import pandas as pd
import json
import joblib
import os
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import KFold, cross_val_score

# =============================
# Paths
# =============================
FEATURE_PATH = "src/features/processed"
FEATURE_LIST_PATH = "src/features/feature_list.json"
MODEL_DIR = "src/models"
EVAL_DIR = "src/evaluation"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)


def train_models():
    print("Loading data...")

    # -----------------------------
    # Load feature data
    # -----------------------------
    X_train = pd.read_csv(f"{FEATURE_PATH}/X_train.csv")
    y_train = pd.read_csv(f"{FEATURE_PATH}/y_train.csv").values.ravel()

    with open(FEATURE_LIST_PATH) as f:
        selected_features = json.load(f)

    X_train = X_train[selected_features]

    # -----------------------------
    # Define models (4 models)
    # -----------------------------
    models = {
        "LinearRegression": LinearRegression(),

        "RandomForest": RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        ),

        "GradientBoosting": GradientBoostingRegressor(
            random_state=42
        ),

        "NeuralNetwork": MLPRegressor(
            hidden_layer_sizes=(64, 32),
            max_iter=500,
            random_state=42
        )
    }

    # -----------------------------
    # 5-Fold Cross Validation
    # -----------------------------
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    results = {}

    for name, model in models.items():
        print(f"Running 5-fold CV for {name}...")

        mae = -cross_val_score(
            model,
            X_train,
            y_train,
            scoring="neg_mean_absolute_error",
            cv=kf
        ).mean()

        rmse = np.sqrt(
            -cross_val_score(
                model,
                X_train,
                y_train,
                scoring="neg_mean_squared_error",
                cv=kf
            ).mean()
        )

        r2 = cross_val_score(
            model,
            X_train,
            y_train,
            scoring="r2",
            cv=kf
        ).mean()

        results[name] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }

    # -----------------------------
    # Select best model (lowest RMSE)
    # -----------------------------
    best_model_name = min(results, key=lambda x: results[x]["RMSE"])
    best_model = models[best_model_name]

    print(f"Best model selected: {best_model_name}")

    # -----------------------------
    # Train best model on full data
    # -----------------------------
    best_model.fit(X_train, y_train)

    # -----------------------------
    # Save model and metrics
    # -----------------------------
    joblib.dump(best_model, f"{MODEL_DIR}/best_model.pkl")

    with open(f"{EVAL_DIR}/metrics.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Training completed successfully.")


if __name__ == "__main__":
    train_models()