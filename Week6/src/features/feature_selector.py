import pandas as pd
import json
import os

FEATURE_DATA_PATH = "src/features/processed"
OUTPUT_PATH = "src/features"

def select_features():
    print("Loading feature data...")
    X_train = pd.read_csv(f"{FEATURE_DATA_PATH}/X_train.csv")
    y_train = pd.read_csv(f"{FEATURE_DATA_PATH}/y_train.csv")

    # Combine for correlation
    df = pd.concat([X_train, y_train], axis=1)

    print("Calculating correlation with target...")
    corr = df.corr()["value"].abs()

    # Threshold-based selection
    selected_features = corr[corr > 0.05].index.tolist()
    selected_features.remove("value")

    print(f"Selected {len(selected_features)} features.")

    # Save feature list
    with open(f"{OUTPUT_PATH}/feature_list.json", "w") as f:
        json.dump(selected_features, f, indent=4)

    print("Feature list saved successfully.")


if __name__ == "__main__":
    select_features()