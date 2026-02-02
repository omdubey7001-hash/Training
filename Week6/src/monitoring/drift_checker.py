import pandas as pd
from scipy.stats import ks_2samp

REFERENCE_DATA = "src/data/processed/final.csv"
CURRENT_DATA = "prediction_logs.csv"

NUMERIC_FEATURES = [
    "duration",
    "credit_amount",
    "installment_commitment",
    "residence_since",
    "age",
    "existing_credits",
    "num_dependents"
]

def check_drift():
    ref = pd.read_csv(REFERENCE_DATA)
    cur = pd.read_csv(CURRENT_DATA)

    print("\nDATA DRIFT REPORT\n")

    for col in NUMERIC_FEATURES:
        if col not in cur.columns:
            continue

        stat, p_value = ks_2samp(ref[col], cur[col])

        drift_status = "DRIFT" if p_value < 0.05 else "NO DRIFT"

        print(
            f"{col:25s} | KS p-value: {p_value:.4f} | {drift_status}"
        )

if __name__ == "__main__":
    check_drift()
