import optuna
import pandas as pd
import json
import joblib
import os
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold

# =============================
# Paths
# =============================
FEATURE_PATH = "src/features/processed"
FEATURE_LIST_PATH = "src/features/feature_list.json"
MODEL_PATH = "src/models/best_model.pkl"
OUTPUT_PATH = "src/tuning"

os.makedirs(OUTPUT_PATH, exist_ok=True)


def objective(trial):
    # -----------------------------
    # Load data
    # -----------------------------
    X = pd.read_csv(f"{FEATURE_PATH}/X_train.csv")
    y = pd.read_csv(f"{FEATURE_PATH}/y_train.csv").values.ravel()

    with open(FEATURE_LIST_PATH) as f:
        features = json.load(f)

    X = X[features]

    # -----------------------------
    # Suggest hyperparameters
    # -----------------------------
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 400),
        "max_depth": trial.suggest_int("max_depth", 5, 30),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5),
        "max_features": trial.suggest_categorical(
            "max_features", ["sqrt", "log2"]
        ),
        "random_state": 42,
        "n_jobs": -1
    }

    model = RandomForestRegressor(**params)

    # -----------------------------
    # 5-fold cross validation
    # -----------------------------
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    rmse = np.sqrt(
        -cross_val_score(
            model,
            X,
            y,
            scoring="neg_mean_squared_error",
            cv=kf,
            n_jobs=-1
        ).mean()
    )

    return rmse   # Optuna will MINIMIZE this


def main():
    print("Starting Optuna hyperparameter tuning...")

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=30)

    print("Best RMSE:", study.best_value)
    print("Best parameters:", study.best_params)

    # -----------------------------
    # Train final model with best params
    # -----------------------------
    X = pd.read_csv(f"{FEATURE_PATH}/X_train.csv")
    y = pd.read_csv(f"{FEATURE_PATH}/y_train.csv").values.ravel()

    with open(FEATURE_LIST_PATH) as f:
        features = json.load(f)

    X = X[features]

    best_model = RandomForestRegressor(
        **study.best_params,
        random_state=42,
        n_jobs=-1
    )

    best_model.fit(X, y)

    # Save model
    joblib.dump(best_model, MODEL_PATH)

    # Save tuning results
    with open(f"{OUTPUT_PATH}/opotuna_results.json", "w") as f:
        json.dump({
            "best_rmse": study.best_value,
            "best_params": study.best_params
        }, f, indent=4)

    print("Optuna tuning completed and best model saved.")


if __name__ == "__main__":
    main()