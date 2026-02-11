from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import uuid
from datetime import datetime
import os

# ---------------- CONFIG ----------------
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")

MODEL_PATH = "models/tuned_model.pkl"
PREPROCESSOR_PATH = "models/preprocessor.pkl"
LOG_PATH = "logs/prediction_logs.csv"

# ---------------- LOAD ARTIFACTS ----------------
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

app = FastAPI(title="Credit Risk Prediction API")

# ---------------- INPUT SCHEMA ----------------
class CreditInput(BaseModel):
    checking_status: str
    duration: int
    credit_history: str
    purpose: str
    credit_amount: int
    savings_status: str
    employment: str
    installment_commitment: int
    personal_status: str
    other_parties: str
    residence_since: int
    property_magnitude: str
    age: int
    other_payment_plans: str
    housing: str
    existing_credits: int
    job: str
    num_dependents: int
    own_telephone: str
    foreign_worker: str

# ---------------- ROUTES ----------------
@app.get("/")
def health():
    return {
        "status": "running",
        "model_version": MODEL_VERSION
    }

@app.post("/predict")
def predict(input_data: CreditInput):
    request_id = str(uuid.uuid4())

    # Convert input to DataFrame
    df = pd.DataFrame([input_data.dict()])

    # APPLY SAME PREPROCESSING AS TRAINING
    X_processed = preprocessor.transform(df)

    prediction = model.predict(X_processed)[0]
    probability = model.predict_proba(X_processed)[0][1]

    # Logging
    log_row = {
    "request_id": request_id,
    "timestamp": datetime.utcnow().isoformat(),
    "prediction": int(prediction),
    "probability": float(probability),
    "model_version": MODEL_VERSION,
}

    # 🔑 ADD RAW INPUT FEATURES FOR DRIFT
    log_row.update(input_data.dict())


    pd.DataFrame([log_row]).to_csv(
        LOG_PATH,
        mode="a",
        header=not os.path.exists(LOG_PATH),
        index=False
    )

    return {
        "request_id": request_id,
        "prediction": "good" if prediction == 1 else "bad",
        "confidence": round(probability, 3),
        "model_version": MODEL_VERSION
    }
