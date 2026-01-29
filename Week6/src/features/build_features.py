import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# ==============================
# Paths
# ==============================
DATA_PATH = "src/data/processed/final.csv"
OUTPUT_DIR = "src/features/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def build_features():
    print("Loading clean data...")
    df = pd.read_csv(DATA_PATH)

    # ==============================
    # 1. Separate target and inputs
    # ==============================
    print("Separating target and features...")
    y = df["value"]                  # target variable
    X = df.drop(columns=["value"])   # input features

    # ==============================
    # 2. Identify column types
    # ==============================
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X.select_dtypes(include=["object", "str"]).columns

    # ==============================
    # 3. Encode categorical features
    # ==============================
    print("Encoding categorical features...")
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False   # IMPORTANT: new sklearn versions
    )

    encoded_cat = encoder.fit_transform(X[cat_cols])

    encoded_cat_df = pd.DataFrame(
        encoded_cat,
        columns=encoder.get_feature_names_out(cat_cols),
        index=X.index
    )

    # ==============================
    # 4. Scale numerical features
    # ==============================
    print("Scaling numerical features...")
    scaler = StandardScaler()
    scaled_num = scaler.fit_transform(X[num_cols])

    scaled_num_df = pd.DataFrame(
        scaled_num,
        columns=num_cols,
        index=X.index
    )

    # ==============================
    # 5. Combine all features
    # ==============================
    print("Combining numerical and categorical features...")
    X_final = pd.concat([scaled_num_df, encoded_cat_df], axis=1)

    # ==============================
    # 6. Train-test split
    # ==============================
    print("Splitting train and test data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_final,
        y,
        test_size=0.2,
        random_state=42
    )

    # ==============================
    # 7. Save processed features
    # ==============================
    print("Saving processed feature files...")
    X_train.to_csv(f"{OUTPUT_DIR}/X_train.csv", index=False)
    X_test.to_csv(f"{OUTPUT_DIR}/X_test.csv", index=False)
    y_train.to_csv(f"{OUTPUT_DIR}/y_train.csv", index=False)
    y_test.to_csv(f"{OUTPUT_DIR}/y_test.csv", index=False)

    print("Feature building completed successfully.")


if __name__ == "__main__":
    build_features()