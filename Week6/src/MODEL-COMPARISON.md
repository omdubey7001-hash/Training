# Model Comparison Report — Day 3

## Objective
This document compares the performance of multiple machine learning models trained for the credit risk / loan approval classification task. Models are evaluated using 5-fold cross-validation and a held-out test set.

---

## Models Evaluated
- Logistic Regression
- Random Forest
- XGBoost
- Neural Network (MLP)

---

## Evaluation Metrics
The following metrics are used for comparison:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC (primary selection metric)

---

## Cross-Validation Results (5-Fold)

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|------|---------|-----------|--------|----------|---------|
| Logistic Regression | 0.766 | 0.808 | 0.873 | 0.840 | **0.793** |
| Random Forest | 0.755 | 0.770 | **0.927** | **0.841** | 0.780 |
| XGBoost | 0.745 | 0.799 | 0.850 | 0.824 | 0.759 |
| Neural Network | 0.739 | 0.802 | 0.832 | 0.817 | 0.750 |

---

## Best Model Selection

**Selection Criterion:** ROC-AUC  
**Selected Model:** **Logistic Regression**

### Reason for Selection
- Achieved the highest ROC-AUC score during cross-validation
- Balanced precision and recall
- Lower variance and better interpretability compared to complex models
- Reduced risk of overfitting

---

## Test Set Performance (Best Model)

| Metric | Value |
|------|-------|
| Accuracy | 0.715 |
| Precision | 0.786 |
| Recall | 0.814 |
| F1 Score | 0.800 |
| ROC-AUC | 0.759 |

---

## Key Observations
- Logistic Regression outperformed more complex models in terms of ROC-AUC.
- Random Forest achieved very high recall but at the cost of lower precision.
- XGBoost and Neural Network underperformed without hyperparameter tuning.
- Simpler models proved more effective for this dataset.

---

## Conclusion
Logistic Regression was selected as the final model due to its superior ROC-AUC, stability, and interpretability. The trained model is suitable for deployment and further optimization.

---

