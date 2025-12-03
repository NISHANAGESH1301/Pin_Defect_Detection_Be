from fastapi import APIRouter
import os
import pandas as pd
import pyodbc
from dotenv import load_dotenv
from sklearn.ensemble import IsolationForest
from scipy import stats
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter()

# Load environment variables
load_dotenv()

SQL_CONN = os.getenv("SQL_CONN")
SQL_QUERY = "SELECT id, machine_no, reading_time, value FROM dbo.MachineData ORDER BY reading_time"


def detect_anomalies(df):
    df["z_score"] = stats.zscore(df["value"])
    df["stat_anomaly"] = df["z_score"].apply(lambda x: -1 if abs(x) > 3 else 1)
    iso = IsolationForest(contamination=0.1, random_state=42)
    df["iforest_anomaly"] = iso.fit_predict(df[["value"]])
    df["final_anomaly"] = df.apply(
        lambda row: -1 if (row["stat_anomaly"] == -1 or row["iforest_anomaly"] == -1) else 1,
        axis=1
    )
    return df


def generate_graph(df):
    plt.figure(figsize=(10, 5))
    normal = df[df['final_anomaly'] == 1]
    plt.scatter(normal['reading_time'], normal['value'], c='blue', label='Normal')
    anomalies = df[df['final_anomaly'] == -1]
    plt.scatter(anomalies['reading_time'], anomalies['value'], c='red', label='Anomaly')
    plt.xlabel("Reading Time")
    plt.ylabel("Value")
    plt.title("Machine Readings with Anomalies")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64


@router.get("/anomaly_graph")
def anomaly_detection():
    try:
        conn = pyodbc.connect(SQL_CONN)
        df = pd.read_sql(SQL_QUERY, conn)
        conn.close()

        if df.empty:
            return {"status": "error", "message": "No data found"}

        df = detect_anomalies(df)
        graph_base64 = generate_graph(df)
        anomalies = df[df["final_anomaly"] == -1].to_dict(orient="records")

        return {
            "status": "success",
            "total_records": len(df),
            "anomalies_found": len(anomalies),
            "anomalies": anomalies,
            "graph_base64": graph_base64
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
