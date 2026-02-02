import streamlit as st
import requests

API_URL = "http://backend:8000/predict"

st.set_page_config(page_title="Credit Risk Predictor", layout="centered")

st.title("💳 Credit Risk Prediction")
st.write("Enter applicant details to predict credit risk.")

with st.form("prediction_form"):
    checking_status = st.selectbox("Checking Status", ["<0", "0<=X<200", ">=200", "no checking"])
    duration = st.number_input("Duration (months)", 1, 100, 6)
    credit_history = st.selectbox(
        "Credit History",
        [
            "no credits/all paid",
            "all paid",
            "existing paid",
            "delayed previously",
            "critical/other existing credit"
        ]
    )
    purpose = st.selectbox(
        "Purpose",
        ["radio/tv", "education", "furniture/equipment", "car", "business", "other"]
    )
    credit_amount = st.number_input("Credit Amount", 100, 100000, 1000)
    savings_status = st.selectbox(
        "Savings Status",
        ["<100", "100<=X<500", "500<=X<1000", ">=1000", "no known savings"]
    )
    employment = st.selectbox(
        "Employment",
        ["unemployed", "<1", "1<=X<4", "4<=X<7", ">=7"]
    )
    installment_commitment = st.slider("Installment Commitment", 1, 4, 2)
    personal_status = st.selectbox(
        "Personal Status",
        ["male single", "female div/dep/mar", "male mar/wid", "male div/sep"]
    )
    other_parties = st.selectbox("Other Parties", ["none", "co applicant", "guarantor"])
    residence_since = st.slider("Residence Since (years)", 1, 4, 2)
    property_magnitude = st.selectbox(
        "Property",
        ["real estate", "life insurance", "car", "no known property"]
    )
    age = st.number_input("Age", 18, 100, 30)
    other_payment_plans = st.selectbox("Other Payment Plans", ["none", "bank", "stores"])
    housing = st.selectbox("Housing", ["own", "rent", "free"])
    existing_credits = st.slider("Existing Credits", 1, 4, 1)
    job = st.selectbox("Job", ["unskilled", "skilled", "high qualif/self emp"])
    num_dependents = st.selectbox("Number of Dependents", [1, 2])
    own_telephone = st.selectbox("Own Telephone", ["yes", "no"])
    foreign_worker = st.selectbox("Foreign Worker", ["yes", "no"])

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "checking_status": checking_status,
        "duration": duration,
        "credit_history": credit_history,
        "purpose": purpose,
        "credit_amount": credit_amount,
        "savings_status": savings_status,
        "employment": employment,
        "installment_commitment": installment_commitment,
        "personal_status": personal_status,
        "other_parties": other_parties,
        "residence_since": residence_since,
        "property_magnitude": property_magnitude,
        "age": age,
        "other_payment_plans": other_payment_plans,
        "housing": housing,
        "existing_credits": existing_credits,
        "job": job,
        "num_dependents": num_dependents,
        "own_telephone": own_telephone,
        "foreign_worker": foreign_worker
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        if response.status_code == 200:
            st.success(f"Prediction: **{result['prediction'].upper()}**")
            st.info(f"Confidence: **{result['confidence']}**")
        else:
            st.error(result)

    except Exception as e:
        st.error(f"API error: {e}")
