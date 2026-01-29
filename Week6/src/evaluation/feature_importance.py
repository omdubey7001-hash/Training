import pandas as pd
import joblib
import json
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("src/models/best_model.pkl")

# Load training data
X_train = pd.read_csv("src/features/processed/X_train.csv")

# Load selected features
with open("src/features/feature_list.json") as f:
    features = json.load(f)

X_train = X_train[features]

# Get feature importance (Random Forest)
importances = model.feature_importances_

# Create DataFrame
importance_df = pd.DataFrame({
    "feature": features,
    "importance": importances
})

# Sort by importance
importance_df = importance_df.sort_values(
    by="importance", ascending=False
).head(15)   # top 15 features

# Plot
plt.figure(figsize=(10, 6))
plt.barh(importance_df["feature"], importance_df["importance"])
plt.gca().invert_yaxis()
plt.title("Top 15 Feature Importances")
plt.xlabel("Importance Score")
plt.tight_layout()

# Save plot
plt.savefig("src/evaluation/feature_importance.png")
plt.close()

print("Feature importance chart saved.")