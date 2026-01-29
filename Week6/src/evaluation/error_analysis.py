import pandas as pd
import joblib
import json
import seaborn as sns
import matplotlib.pyplot as plt

X_test = pd.read_csv("src/features/processed/X_test.csv")
y_test = pd.read_csv("src/features/processed/y_test.csv").values.ravel()

with open("src/features/feature_list.json") as f:
    features = json.load(f)

X_test = X_test[features]

model = joblib.load("src/models/best_model.pkl")
preds = model.predict(X_test)

errors = y_test - preds

error_df = pd.DataFrame({
    "actual": y_test,
    "predicted": preds,
    "error": errors
})

sns.histplot(error_df["error"], kde=True)
plt.title("Error Distribution")
plt.savefig("src/evaluation/error_distribution.png")
plt.close()