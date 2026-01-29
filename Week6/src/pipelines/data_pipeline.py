import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from scipy import stats

RAW_PATH = "src/data/raw/dataset.csv"
PROCESSED_PATH = "src/data/processed/final.csv"


def load_data(path):
    print("Loading raw data...")
    return pd.read_csv(path)


def handle_missing_values(df):
    print("Handling missing values...")
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df


def remove_duplicates(df):
    print("Removing duplicates...")
    return df.drop_duplicates()


def handle_outliers(df):
    print("Handling outliers using Z-score...")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    z_scores = np.abs(stats.zscore(df[numeric_cols]))
    df = df[(z_scores < 3).all(axis=1)]
    return df


def scale_features(df):
    print("Scaling numerical features...")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df


def save_processed_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Processed data saved at {path}")


def run_pipeline():
    df = load_data(RAW_PATH)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = handle_outliers(df)
    df = scale_features(df)
    save_processed_data(df, PROCESSED_PATH)


if __name__ == "__main__":
    run_pipeline()