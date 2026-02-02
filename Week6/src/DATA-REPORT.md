# Data Report – Day 1

## Project Overview
This report documents the data understanding, preprocessing, and exploratory analysis performed as part of Day-1 of the machine learning project. The objective is to establish a clean, reproducible, and well-structured data pipeline following industry best practices.

---

## Dataset Description

- **Domain:** Banking / Credit Risk (Loan Approval)
- **Problem Type:** Binary Classification
- **Target Variable:** `class`
  - `good` → Low credit risk (loan approved)
  - `bad` → High credit risk (loan rejected)
- **Source:** German Credit Dataset
- **Initial Shape:** 1000 rows × 21 columns

Each row represents a loan applicant, and features describe financial stability, credit history, employment, assets, and demographic information.

---

## Project Data Architecture
```text

src/
├── config/
├── data/
│ ├── external/
│ ├── processed/
│ │ └── final.csv
│ └── raw/
│ └── dataset.csv
├── DATA-REPORT.md
├── deployment/
├── evaluation/
├── features/
├── logs/
├── monitoring/
├── notebooks/
│ └── EDA.ipynb
├── pipelines/
│ ├── data_pipeline.py
│ └── models/
├── training/
└── utils/

```

This structure ensures dataset versioning, reproducibility, and clear separation of concerns.

---

## Data Loading

- Raw data is loaded strictly from:
`src/data/raw/dataset.csv`

- No direct modifications are performed on raw data.
- All transformations are applied only to processed data.

---

## Data Cleaning & Preprocessing

The following preprocessing steps were implemented in `data_pipeline.py`:

### 1. Duplicate Handling
- Duplicate rows were checked and removed.
- **Result:** No duplicate records found.

### 2. Missing Value Treatment
- Numerical features: filled using **median**
- Categorical features: filled using **mode**
- **Result:** No missing values remained after preprocessing.

### 3. Outlier Detection & Treatment
- Method used: **IQR (Interquartile Range)**
- Strategy: **Clipping instead of removal**
- Reason: Prevents data loss while reducing extreme influence
- **Result:** Minor value adjustments where applicable.

---

## Processed Dataset

- Final dataset saved at:
`src/data/processed/final.csv`

- **Final Shape:** 1000 rows × 21 columns
- Raw data integrity preserved.

---

## Exploratory Data Analysis (EDA)

EDA was performed in `src/notebooks/EDA.ipynb` with the following analyses:

### 1. Missing Values Heatmap
- Confirms absence of missing values post-cleaning.

### 2. Target Variable Distribution
- Target variable shows **class imbalance**, which will require special handling during modeling (e.g., class weights or resampling).

### 3. Feature Distributions
- Several numerical features show skewed distributions.
- Indicates potential benefit of scaling or transformation.

### 4. Correlation Analysis
- Correlation between numerical features is generally low.
- Reduced risk of multicollinearity.

---

## Key Observations

- Dataset quality is high with minimal cleaning required.
- Class imbalance is present and must be addressed in later stages.
- Feature relationships are weakly correlated, suitable for multiple model types.
- Pipeline confirms dataset readiness for feature engineering and modeling.

---

## Conclusion

Day-1 objectives have been successfully achieved:
- Professional ML project structure implemented
- Reproducible data preprocessing pipeline created
- Cleaned dataset generated and versioned
- Comprehensive EDA conducted with visual insights

This dataset is now ready for **feature engineering, splitting strategies, and model training** in subsequent stages.

---
