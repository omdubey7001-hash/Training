import joblib
import optuna
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

# Load saved splits
X_train = joblib.load("src/data/splits/X_train.pkl")
y_train = joblib.load("src/data/splits/y_train.pkl").map({"bad": 0, "good": 1})


RESULTS_PATH = "src/tuning/results.json"
MODEL_PATH = "src/models/tuned_model.pkl"

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 5, 30),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5),
        "random_state": 42,
        "n_jobs": -1
    }

    model = RandomForestClassifier(**params)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(
        model, X_train, y_train, cv=cv, scoring="f1"
    )

    return scores.mean()

def main():
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)

    best_params = study.best_params
    best_score = study.best_value

    best_model = RandomForestClassifier(**best_params, random_state=42)
    best_model.fit(X_train, y_train)

    joblib.dump(best_model, MODEL_PATH)

    results = {
        "best_f1_score": best_score,
        "best_params": best_params
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print("Hyperparameter tuning completed")
    print("Best F1 Score:", best_score)
    print("Best Parameters:", best_params)

if __name__ == "__main__":
    main()
