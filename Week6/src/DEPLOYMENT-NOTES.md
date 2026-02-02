# Deployment Notes – Credit Risk Prediction System

## 1. Overview
This document describes the deployment architecture, API design, Docker setup, logging, and monitoring strategy for the Credit Risk Prediction system.

The system is deployed as a **containerized, production-style ML service** consisting of:
- Backend ML inference API
- Frontend user interface
- Monitoring utilities

---

## 2. Deployment Architecture

### Components
- **Backend**: FastAPI-based inference service
- **Frontend**: Streamlit web interface
- **Model**: Tuned RandomForestClassifier
- **Preprocessor**: Saved sklearn pipeline
- **Containerization**: Docker + Docker Compose

### Architecture Flow

`User → Streamlit UI → FastAPI API → ML Model → Prediction + Logs`


---

## 3. API Design

### Endpoint

`POST /predict`


### Input Format
The API accepts **raw, human-readable features** (no manual encoding required).

Example:
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
Response Format:
```json
{
  "request_id": "uuid",
  "prediction": "good",
  "confidence": 0.69,
  "model_version": "v1"
}
```

## 4. Production Features Implemented
- Input Validation

    - Implemented using Pydantic models

    - Ensures correct data types and required fields

- Request ID Tracking

    - Unique UUID generated for every request

    - Enables traceability across logs and monitoring

- Versioned Model Loading

    - Model version controlled using environment variables

    - Allows safe future upgrades and rollbacks

- Consistent Preprocessing

    - Same preprocessing pipeline used in training and inference

    - Prevents training–serving skew

## 5. Prediction Logging

**All predictions are logged to:**

`prediction_logs.csv`

**Logged Fields**

- `request_id`

- `timestamp`

- `prediction`

- `probability`

- `model_version`

- `raw input features`

**This enables:**

- Auditability

- Debugging

- Drift detection

## 6. Dockerized Deployment
**Containers**

- Backend Container

    - Runs FastAPI via Uvicorn

    - Exposes port 8000

- Frontend Container

    - Runs Streamlit

    - Exposes port 8501

- Start System
    - `docker compose up --build`

- Access

    - Backend API → `http://localhost:8000`

    - API Docs → `http://localhost:8000/docs`

    - Frontend UI → `http://localhost:8501`

## 7. Monitoring & Drift Detection
- Drift Detection Script
    - `src/monitoring/drift_checker.py`

- Method

    - Compares training feature distributions with recent prediction data

    - Uses statistical tests (e.g., KS-test)

    - Prints a drift report to terminal

- Execution
    - `python src/monitoring/drift_checker.py`