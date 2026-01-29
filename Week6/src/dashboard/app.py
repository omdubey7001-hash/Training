import streamlit as st
import requests
import json

# ============================
# Config
# ============================
API_URL = "http://127.0.0.1:8000/predict"

FEATURE_LIST_PATH = "src/features/feature_list.json"

with open(FEATURE_LIST_PATH) as f:
    FEATURES = json.load(f)

# ============================
# UI
# ============================
st.set_page_config(page_title="ML Prediction App", layout="centered")

st.title("Price Prediction Dashboard")

st.markdown("Provide inputs and get model predictions.")

# ----------------------------
# Human-friendly inputs
# ----------------------------
year = st.number_input("Year", min_value=1990, max_value=2030, value=2020)

category = st.selectbox(
    "Category",
    [
        "Gross value of production",
        "Net value",
        "Operating costs"
    ]
)

region = st.selectbox(
    "Region",
    [
        "Fruitful Rim",
        "Basin and Range",
        "Prairie Gateway"
    ]
)

model_version = st.text_input("Model Version (optional)", value="")

# ----------------------------
# Convert to model input
# ----------------------------
def build_model_input():
    data = {feature: 0 for feature in FEATURES}

    data["year"] = year
    data[f"category_{category}"] = 1
    data[f"region_{region}"] = 1

    return data

# ----------------------------
# Predict button
# ----------------------------
if st.button("Predict"):
    payload = {
        "data": build_model_input()
    }

    if model_version.strip():
        payload["model_version"] = model_version.strip()

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Prediction successful!")
            st.metric("Prediction", round(result["prediction"], 2))
            st.text(f"Request ID: {result['request_id']}")
            st.text(f"Model Version: {result['model_version']}")
    else:
        st.error("API Error")