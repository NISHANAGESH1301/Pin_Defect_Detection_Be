import os
import pandas as pd
import pyodbc
from fastapi import FastAPI
from dotenv import load_dotenv
from sklearn.ensemble import IsolationForest

# Load env file
load_dotenv()
SQL_CONN = os.getenv("SQL_CONN")

app = FastAPI()

# -------------------------
# Helper: Fetch data from DB
# -------------------------
def get_data():
    conn = pyodbc.connect(SQL_CONN)
    query = "SELECT id, machine_no, reading_time, value FROM dbo.MachineData ORDER BY reading_time ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# -------------------------
# API 1: Get all machine records
# -------------------------
@app.get("/machines")
def get_machines():
    try:
        df = get_data()
        return {"status": "success", "data": df.to_dict(orient="records")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------
# API 2: Detect anomalies
# -------------------------
@app.get("/anomalies")
def detect_anomalies():
    try:
        df = get_data()
        if df.empty:
            return {"status": "error", "message": "No data available"}

        # --- Method 1: Statistical Z-score ---
        mean_val = df["value"].mean()
        std_val = df["value"].std()
        df["z_score"] = (df["value"] - mean_val) / std_val
        df["stat_anomaly"] = df["z_score"].apply(lambda x: -1 if abs(x) > 3 else 1)

        # --- Method 2: IsolationForest ---
        model = IsolationForest(
            n_estimators=200,
            contamination=0.15,  # up to 15% anomalies
            random_state=42
        )
        df["iforest_anomaly"] = model.fit_predict(df[["value"]])

        # --- Final anomaly flag (either method) ---
        df["final_anomaly"] = df.apply(
            lambda row: -1 if (row["stat_anomaly"] == -1 or row["iforest_anomaly"] == -1) else 1,
            axis=1
        )

        anomalies = df[df["final_anomaly"] == -1]

        return {
            "status": "success",
            "total_records": len(df),
            "anomalies_found": len(anomalies),
            "anomalies": anomalies.to_dict(orient="records"),
            "all_data": df.to_dict(orient="records")  # keep full for debugging
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
