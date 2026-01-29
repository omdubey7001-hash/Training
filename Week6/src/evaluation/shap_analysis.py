import pandas as pd
import joblib
import json
import shap
import matplotlib.pyplot as plt

# Load data
X_test = pd.read_csv("src/features/processed/X_test.csv")
y_test = pd.read_csv("src/features/processed/y_test.csv").values.ravel()

with open("src/features/feature_list.json") as f:
    features = json.load(f)

X_test = X_test[features]

# Load model
model = joblib.load("src/models/best_model.pkl")

# SHAP explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("src/evaluation/shap_summary.png")
plt.close()