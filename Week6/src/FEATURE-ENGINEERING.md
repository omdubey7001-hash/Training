# Feature Engineering & Feature Selection — Day 2

## Objective
The goal of Day 2 is to transform cleaned data into model-ready features by applying encoding, numerical transformations, feature generation, and feature selection techniques. This stage prepares high-quality input features for model training.

---

## Learning Outcomes
- Create meaningful derived features
- Apply appropriate encoding strategies
- Perform numerical feature transformations
- Select important features using statistical and model-based techniques

---

## Input Dataset
- **Source:** `src/data/processed/final.csv`
- **Type:** Tabular data
- **Task:** Binary classification (credit risk / loan approval)
- **Target Column:** `class`  
  - `good` → 1  
  - `bad` → 0  

---

## Feature Engineering Pipeline

### 1. Categorical Encoding
The following encoding strategies are applied:
- **One-Hot Encoding**
  - Used for nominal categorical variables
  - Handles unknown categories safely
- Converts categorical features into numerical format suitable for ML models

---

### 2. Numerical Feature Scaling
- **StandardScaler**
  - Centers features around mean = 0
  - Scales to unit variance
- Prevents dominance of high-magnitude features

---

### 3. Feature Generation (10+ New Features)
New features are created to capture non-linear relationships and domain insights, including:
- Credit amount per month
- Log-transformed credit amount
- Log-transformed duration
- Squared age feature
- Credit-to-age ratio
- Installment-to-credit ratio
- Binary indicators for employment
- Binary indicators for savings presence
- Young applicant flag
- Long-term loan flag

These features improve model expressiveness and predictive power.

---

## Train–Test Split
- Dataset split into:
  - **X_train, X_test**
  - **y_train, y_test**
- Stratified split ensures class distribution consistency
- Test size: 20%
- Stored it in `src/data/split/---`

---

## Feature Selection Techniques

Multiple feature selection strategies are applied to reduce noise and redundancy:

### 1. Correlation Threshold
- Highly correlated features are identified
- Prevents multicollinearity

### 2. Mutual Information
- Measures dependency between features and target
- Captures non-linear relationships

### 3. Recursive Feature Elimination (RFE)
- Iteratively removes least important features
- Uses Logistic Regression as the base estimator

### 4. Tree-Based Feature Importance
- Random Forest feature importance
- Captures non-linear interactions

Final feature scores are computed by combining multiple methods.

---

## Output Artifacts

### Generated Files

```text
src/features/
├── build_features.py
├── feature_selector.py
├── feature_list.json
├── X_train.npy
├── X_test.npy
├── y_train.npy
└── y_test.npy
```

### Complete architecture
```
src
├── config
├── data
│   ├── external
│   ├── processed
│   │   └── final.csv
│   └── raw
│       └── dataset.csv
├── DATA-REPORT.md
├── deployment
├── evaluation
├── features
│   ├── build_features.py
│   ├── feature_list.json
│   ├── feature_selector.py
│   ├── X_test.csv
│   ├── X_train.csv
│   ├── y_test.csv
│   └── y_train.csv
├── logs
├── monitoring
├── notebooks
│   └── EDA.ipynb
├── pipelines
│   ├── data_pipeline.py
│   └── models
├── training
└── utils

```


### `feature_list.json`
- Stores selected feature indices
- Tracks total feature count
- Ensures reproducibility for training

---

## Key Outcomes
- Categorical and numerical features successfully transformed
- More than 10 engineered features generated
- Feature selection applied using multiple robust techniques
- Final train-ready datasets produced

---

## Conclusion
Day-2 objectives have been successfully completed. The dataset is now transformed into a compact, informative feature set optimized for model training and evaluation in subsequent stages.

---

