import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif

DATA_PATH = "src/data/processed/final.csv"
TARGET_COL = "class"

def select_features():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    X_encoded = pd.get_dummies(X, drop_first=True)

    mi_scores = mutual_info_classif(X_encoded, y, random_state=42)
    mi_df = pd.DataFrame({
        "feature": X_encoded.columns,
        "importance": mi_scores
    }).sort_values(by="importance", ascending=False)

    print("Top 10 Important Features:")
    print(mi_df.head(10))

if __name__ == "__main__":
    select_features()
