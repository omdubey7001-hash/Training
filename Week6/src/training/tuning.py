import pandas as pd
import json
import joblib
import os
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Paths
FEATURE_PATH = "src/features/processed"
FEATURE_LIST_PATH = "src/features/feature_list.json"
OUTPUT_PATH = "src/tuning"

os.makedirs(OUTPUT_PATH, exist_ok=True)

def tune_model():
    print("Loading data...")

    X_train = pd.read_csv(f"{FEATURE_PATH}/X_train.csv")
    y_train = pd.read_csv(f"{FEATURE_PATH}/y_train.csv").values.ravel()

    X_test = pd.read_csv(f"{FEATURE_PATH}/X_test.csv")
    y_test = pd.read_csv(f"{FEATURE_PATH}/y_test.csv").values.ravel()

    with open(FEATURE_LIST_PATH) as f:
        features = json.load(f)

    X_train = X_train[features]
    X_test = X_test[features]

    print("Starting hyperparameter tuning...")

    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5]
    }

    model = RandomForestRegressor(random_state=42, n_jobs=-1)

    grid = GridSearchCV(
        model,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        n_jobs=-1
    )

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    print("Best parameters found:", grid.best_params_)

    # -------------------------
    # Evaluate best model
    # -------------------------
    y_pred = best_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"RMSE: {rmse}")
    print(f"R2 Score: {r2}")

    # Save model
    joblib.dump(best_model, "src/models/best_model.pkl")

    # Save tuning results
    with open(f"{OUTPUT_PATH}/grid_results.json", "w") as f:
        json.dump({
            "best_params": grid.best_params_,
            "cv_rmse": (-grid.best_score_) ** 0.5,
            "test_rmse": rmse,
            "test_r2": r2
        }, f, indent=4)

    print("Tuning completed and best model saved.")

if __name__ == "__main__":
    tune_model()