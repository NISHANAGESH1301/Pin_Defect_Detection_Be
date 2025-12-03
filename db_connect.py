import pyodbc
import pandas as pd

# 🔹 Your SQL Server connection string
# Replace with your actual server, database, user, and password
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=machine;"
    "UID=daimler;"       
    "PWD=nisha@1997;"
    # If using Windows Auth, replace UID/PWD with Trusted_Connection=yes;
)

try:
    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    print("✅ Connection successful!")

    # Example: fetch machine data
    query = "SELECT TOP 10 * FROM dbo.Machine"   # replace with your table
    df = pd.read_sql(query, conn)

    print("✅ Data fetched successfully:")
    print(df)

    conn.close()

except Exception as e:
    print("Error:", e)
