# 🏦 Credit Risk Prediction System (End-to-End MLOps)

An end-to-end **Machine Learning + MLOps** project that builds, explains, deploys, and monitors a **credit risk prediction model** using the German Credit dataset.

This project demonstrates **real-world ML pipeline design**, from raw data ingestion to production deployment with monitoring.

---

## 📌 Project Highlights

✔ Cleaned & versioned datasets  
✔ Automated feature engineering  
✔ Multiple models trained & compared  
✔ Hyperparameter tuning (Optuna)  
✔ Explainability (SHAP + Feature Importance)  
✔ Production-ready API (FastAPI)  
✔ Frontend UI (Streamlit)  
✔ Dockerized deployment (Backend + Frontend)  
✔ Prediction logging & request tracking  
✔ Data drift detection  
✔ Full documentation  

---

## 📂 Project Structure

```
Week6
├── src
│   ├── config
│   ├── data
│   │   ├── external
│   │   ├── processed
│   │   │   ├── eda
│   │   │   │   ├── correlation.png
│   │   │   │   ├── distributions.png
│   │   │   │   └── missing_values.png
│   │   │   └── final.csv
│   │   ├── raw
│   │   │   └── dataset.csv
│   │   └── splits
│   │       ├── X_train.pkl
│   │       ├── X_test.pkl
│   │       ├── y_train.pkl
│   │       └── y_test.pkl
│   │
│   ├── pipelines
│   │   └── data_pipeline.py
│   │
│   ├── features
│   │   ├── build_features.py
│   │   ├── feature_selector.py
│   │   └── feature_list.json
│   │
│   ├── training
│   │   ├── train.py
│   │   └── tuning.py
│   │
│   ├── tuning
│   │   └── results.json
│   │
│   ├── evaluation
│   │   ├── shap_analysis.py
│   │   ├── shap_summary.png
│   │   ├── feature_importance.png
│   │   ├── error_analysis_heatmap.png
│   │   └── metrics.json
│   │
│   ├── models
│   │   ├── best_model.pkl
│   │   ├── tuned_model.pkl
│   │   ├── preprocessor.pkl
│   │   └── feature_columns.pkl
│   │
│   ├── deployment
│   │   ├── api.py
│   │   ├── Dockerfile.api
│   │   └── requirements.txt
│   │
│   ├── frontend
│   │   ├── app.py
│   │   └── Dockerfile.frontend
│   │
│   ├── monitoring
│   │   └── drift_checker.py
│   │
│   ├── notebooks
│   │   └── EDA.ipynb
│   │
│   ├── logs
│   │   └── prediction_logs.csv
│   │
│   ├── utils
│   │
│   ├── DATA-REPORT.md
│   ├── FEATURE-ENGINEERING.md
│   ├── MODEL-COMPARISON.md
│   ├── MODEL-INTERPRETATION.md
│   └── DEPLOYMENT-NOTES.md
│
├── README.md
├── docker-compose.yml

```
---

## 🧠 Problem Statement

Predict whether a loan applicant is **GOOD** or **BAD credit risk** based on financial and personal attributes.

This is a **binary classification problem** where:
- `good` → low credit risk  
- `bad` → high credit risk  

---

## ⚙️ ML Pipeline Overview

### 1️⃣ Data Engineering
- Loaded raw data from `/data/raw`
- Handled missing values & duplicates
- Generated EDA reports (correlation, distributions)
- Saved clean dataset to `/data/processed/final.csv`

### 2️⃣ Feature Engineering
- Numerical scaling (StandardScaler)
- Categorical encoding (OneHotEncoder)
- ColumnTransformer-based preprocessing
- Feature selection using model importance

### 3️⃣ Model Training
- Logistic Regression (baseline)
- Random Forest (final model)
- Stratified train/test split

### 4️⃣ Hyperparameter Tuning
- Optuna optimization
- Optimized for **F1 score**
- Best parameters stored in `/tuning/results.json`

### 5️⃣ Model Explainability
- SHAP summary plot
- Feature importance chart
- Error analysis heatmap

---

## 🚀 Deployment

### Backend (FastAPI)
- Endpoint: `POST /predict`
- Accepts **raw feature JSON**
- Applies saved preprocessing pipeline
- Returns prediction + confidence
- Logs every prediction with request ID

### Example Request
```json
{
  "checking_status": "<0",
  "duration": 6,
  "credit_history": "no credits/all paid",
  "purpose": "radio/tv",
  "credit_amount": 1000,
  "savings_status": "<100",
  "employment": "unemployed",
  "installment_commitment": 2,
  "personal_status": "male single",
  "other_parties": "none",
  "residence_since": 2,
  "property_magnitude": "real estate",
  "age": 30,
  "other_payment_plans": "none",
  "housing": "rent",
  "existing_credits": 1,
  "job": "skilled",
  "num_dependents": 1,
  "own_telephone": "yes",
  "foreign_worker": "yes"
}
```

---

### 🖥️ Frontend (Streamlit)

- User-friendly form for applicant details

- Sends request to backend API

- Displays prediction & confidence score

---

### 🐳 Dockerized Setup

- Both backend and frontend are containerized and run together.

- Start Entire System

`docker compose up --build`

- Services

    - Backend → `http://localhost:8000`

    - API Docs → `http://localhost:8000/docs`

    - Frontend → `http://localhost:8501`

---

#### Prediction Logging
 
**All predictions are stored in:**

`src/logs/prediction_logs.csv`


- Logged fields:

    - `request_id`

    - `timestamp`

    - `prediction`

    - `probability`

    - `model_version`

    - `raw input features`

- Data Drift Detection

    - Run: `python src/monitoring/drift_checker.py`


- Uses statistical tests (KS-test) to compare:

    - Training data distribution

    - Recent production predictions

    - Outputs a data drift report.

---

### 📄 Documentation

- `DATA-REPORT.md` → Dataset analysis & EDA

- `FEATURE-ENGINEERING.md` → Feature pipeline details

- `MODEL-COMPARISON.md` → Model evaluation results

- `MODEL-INTERPRETATION.md` → Explainability & SHAP

- `DEPLOYMENT-NOTES.md` → Docker & deployment notes

---

# --- THANK YOU ---
