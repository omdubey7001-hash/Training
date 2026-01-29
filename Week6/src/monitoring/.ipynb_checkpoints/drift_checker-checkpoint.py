import pandas as pd
import ast

# Load training data
train_df = pd.read_csv("src/features/processed/X_train.csv")

# Load prediction logs
logs = pd.read_csv("prediction_logs.csv")

# Convert input string back to dict
logs["input"] = logs["input"].apply(ast.literal_eval)

# Extract year from logs
log_years = logs["input"].apply(lambda x: x.get("year"))

print("Training year range:")
print(train_df["year"].min(), "to", train_df["year"].max())

print("\nLogged prediction year range:")
print(log_years.min(), "to", log_years.max())

# Simple drift check
if log_years.max() > train_df["year"].max():
    print("\n⚠️ WARNING: Year drift detected!")
else:
    print("\n✅ No year drift detected.")