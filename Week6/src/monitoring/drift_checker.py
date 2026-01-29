import pandas as pd
import ast

# Load RAW training data (before scaling)
raw_train = pd.read_csv("src/data/raw/dataset.csv")

# Load prediction logs
logs = pd.read_csv("src/logs/prediction_logs.csv")

# Convert input string back to dict
logs["input"] = logs["input"].apply(ast.literal_eval)

# Extract raw years
train_years = raw_train["year"]
log_years = logs["input"].apply(lambda x: x.get("year"))

print("Training (RAW) year range:")
print(train_years.min(), "to", train_years.max())

print("\nLogged prediction year range:")
print(log_years.min(), "to", log_years.max())

# Correct drift check
if log_years.min() < train_years.min() or log_years.max() > train_years.max():
    print("\n WARNING: Year drift detected!")
else:
    print("\n No year drift detected.")