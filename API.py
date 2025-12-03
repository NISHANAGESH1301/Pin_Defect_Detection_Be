import os
import pandas as pd
import pyodbc
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SQL_CONN = os.getenv("SQL_CONN")
SQL_QUERY = "SELECT TOP 10 machine_no, machine_desc FROM dbo.Machine"

app = FastAPI()

@app.get("/machines")
def get_machines():
    try:
        # Connect to SQL Server
        conn = pyodbc.connect(SQL_CONN)
        df = pd.read_sql(SQL_QUERY, conn)
        conn.close()

        # Convert dataframe to list of dicts (JSON)
        data = df.to_dict(orient="records")
        return {"status": "success", "data": data}

    except Exception as e:
        return {"status": "error", "message": str(e)}
