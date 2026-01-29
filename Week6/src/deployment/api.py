from fastapi import FastAPI
from pydantic import BaseModel, validator
import joblib
import json
import pandas as pd
from datetime import datetime
import uuid
import os
from typing import Optional, Dict

# -------------------------
# App initialization
# -------------------------
app = FastAPI(title="ML Model API")

# -------------------------
# Paths
# -------------------------
MODEL_DIR = "src/models/versions"
FEATURE_LIST_PATH = "src/features/feature_list.json"
LOG_FILE = "src/logs/prediction_logs.csv"

# -------------------------
# Load feature list
# -------------------------
with open(FEATURE_LIST_PATH) as f:
    FEATURES = json.load(f)

# -------------------------
# Utility: Load model by version
# -------------------------
def load_model(version: Optional[str] = None):
    if version:
        model_path = f"{MODEL_DIR}/model_{version}.pkl"
        if not os.path.exists(model_path):
            raise ValueError(f"Model version {version} not found")
    else:
        versions = sorted(os.listdir(MODEL_DIR))
        model_path = os.path.join(MODEL_DIR, versions[-1])

    return joblib.load(model_path), os.path.basename(model_path)

# -------------------------
# Input schema (STRICT)
# -------------------------
class PredictionInput(BaseModel):
    data: Dict[str, float]
    model_version: Optional[str] = None

    @validator("data")
    def validate_data(cls, v):
        # Missing features
        missing = set(FEATURES) - set(v.keys())
        if missing:
            raise ValueError(f"Missing features: {missing}")

        # Extra features
        extra = set(v.keys()) - set(FEATURES)
        if extra:
            raise ValueError(f"Unexpected features: {extra}")

        # Value checks
        for key, value in v.items():
            if value is None:
                raise ValueError(f"Null value for feature: {key}")
            if not isinstance(value, (int, float)):
                raise ValueError(f"Non-numeric value for feature: {key}")

        return v

# -------------------------
# Prediction logging
# -------------------------
def log_prediction(request_id, model_version, input_data, prediction):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    log_exists = os.path.exists(LOG_FILE)

    row = {
        "timestamp": datetime.utcnow(),
        "request_id": request_id,
        "model_version": model_version,
        "input": str(input_data),
        "prediction": prediction
    }

    pd.DataFrame([row]).to_csv(
        LOG_FILE,
        mode="a",
        header=not log_exists,
        index=False
    )

# -------------------------
# Routes
# -------------------------
@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/predict")
def predict(request: PredictionInput):
    request_id = str(uuid.uuid4())

    # Load model
    try:
        model, model_file = load_model(request.model_version)
    except ValueError as e:
        return {
            "request_id": request_id,
            "error": str(e)
        }

    # Predict
    X = pd.DataFrame([request.data])[FEATURES]
    prediction = model.predict(X)[0]

    # Log
    log_prediction(
        request_id=request_id,
        model_version=model_file,
        input_data=request.data,
        prediction=prediction
    )

    return {
        "request_id": request_id,
        "model_version": model_file,
        "prediction": prediction
    }