import pandas as pd
import numpy as np
import json
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

DATA_PATH = "src/data/processed/final.csv"
FEATURE_LIST_PATH = "src/features/feature_list.json"

TARGET_COL = "class"   

SPLIT_PATH = "src/data/splits"
os.makedirs(SPLIT_PATH, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)

    # 🔑 FORCE string columns to object dtype (IMPORTANT)
    for col in df.select_dtypes(include=["string"]):
        df[col] = df[col].astype("object")

    return df


def split_data(df):
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    return train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

def build_pipeline(X):
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X.select_dtypes(include=["object", "string"]).columns

    numeric_pipeline = Pipeline([
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, num_cols),
        ("cat", categorical_pipeline, cat_cols)
    ])

    return preprocessor, num_cols, cat_cols

def save_feature_list(num_cols, cat_cols):
    feature_info = {
        "numerical_features": list(num_cols),
        "categorical_features": list(cat_cols)
    }

    with open(FEATURE_LIST_PATH, "w") as f:
        json.dump(feature_info, f, indent=4)

def main():
    df = load_data()
    X_train, X_test, y_train, y_test = split_data(df)

    preprocessor, num_cols, cat_cols = build_pipeline(X_train)

    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # 🔑 SAVE PREPROCESSOR (THIS WAS MISSING)
    joblib.dump(preprocessor, "src/models/preprocessor.pkl")


    joblib.dump(X_train_transformed, f"{SPLIT_PATH}/X_train.pkl")
    joblib.dump(X_test_transformed, f"{SPLIT_PATH}/X_test.pkl")
    joblib.dump(y_train, f"{SPLIT_PATH}/y_train.pkl")
    joblib.dump(y_test, f"{SPLIT_PATH}/y_test.pkl")

    print("Train/Test splits saved")


    save_feature_list(num_cols, cat_cols)

    print("Feature engineering completed")
    print("X_train shape:", X_train_transformed.shape)
    print("X_test shape:", X_test_transformed.shape)

if __name__ == "__main__":
    main()
