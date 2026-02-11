import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE

RAW_PATH = "src/data/raw/dataset.csv"
PROCESSED_PATH = "src/data/processed/final.csv"
EDA_PATH = "src/data/processed/eda"
TARGET_COL = "class"
os.makedirs(EDA_PATH, exist_ok=True)

def load_data():
    df = pd.read_csv(RAW_PATH)
    print(" Data loaded:", df.shape)
    return df

def clean_data(df):
    df = df.drop_duplicates()

    # Handle missing values
    for col in df.select_dtypes(include=np.number):
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include=["object", "string"]):

        df[col] = df[col].fillna(df[col].mode()[0])

    # Remove outliers using IQR
    for col in df.select_dtypes(include=np.number):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    print("Data cleaned:", df.shape)
    if TARGET_COL in df.columns:

        print("\nClass Distribution BEFORE:")
        print(df[TARGET_COL].value_counts())

        X = df.drop(columns=[TARGET_COL])
        y = df[TARGET_COL]

        # Only numeric features for SMOTE
        X_num = pd.get_dummies(X, drop_first=True)

        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_num, y)

        df_resampled = pd.concat(
            [pd.DataFrame(X_resampled), pd.Series(y_resampled, name=TARGET_COL)],
            axis=1
        )
        print("\nClass Distribution AFTER SMOTE:")
        print(df_resampled[TARGET_COL].value_counts())

        print("Final Shape:", df_resampled.shape)

        df = df_resampled

    return df

def save_processed(df):
    df.to_csv(PROCESSED_PATH, index=False)
    print("Processed data saved")

def generate_eda(df):
    # Correlation heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(f"{EDA_PATH}/correlation.png")
    plt.close()

    # Feature distributions
    df.hist(figsize=(12, 10))
    plt.savefig(f"{EDA_PATH}/distributions.png")
    plt.close()

    # Missing values heatmap
    plt.figure(figsize=(8, 4))
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Missing Values")
    plt.savefig(f"{EDA_PATH}/missing_values.png")
    plt.close()

    # Target distribution (FIXED)
    if "target" in df.columns:
        plt.figure(figsize=(6, 4))
        df["target"].value_counts().plot(kind="bar")
        plt.title("Target Distribution")
        plt.savefig(f"{EDA_PATH}/target_distribution.png")
        plt.close()

    print("EDA generated")

def main():
    df = load_data()
    df = clean_data(df)
    save_processed(df)
    generate_eda(df)

if __name__ == "__main__":
    main()
