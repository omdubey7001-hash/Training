import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np

# Load model and test data
model = joblib.load("src/models/tuned_model.pkl")
X_test = joblib.load("src/data/splits/X_test.pkl")
y_test = joblib.load("src/data/splits/y_test.pkl").map({"bad": 0, "good": 1})

# SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# ---- IMPORTANT FIX ----
# If shap_values is 3D (samples, features, classes),
# take the positive class (class=1)
if isinstance(shap_values, list):
    shap_matrix = shap_values[1]
elif shap_values.ndim == 3:
    shap_matrix = shap_values[:, :, 1]
else:
    shap_matrix = shap_values

# SHAP summary plot
plt.figure()
shap.summary_plot(shap_matrix, X_test, show=False)
plt.tight_layout()
plt.savefig("src/evaluation/shap_summary.png")
plt.close()

# Feature importance (mean absolute SHAP)
importance = np.abs(shap_matrix).mean(axis=0)
top_idx = np.argsort(importance)[-10:]

plt.figure(figsize=(8, 5))
plt.barh(range(len(top_idx)), importance[top_idx])
plt.yticks(range(len(top_idx)), [f"f{i}" for i in top_idx])
plt.title("Top 10 Feature Importance (SHAP)")
plt.tight_layout()
plt.savefig("src/evaluation/feature_importance.png")
plt.close()

print("SHAP explainability generated")
