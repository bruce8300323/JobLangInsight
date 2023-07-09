import pyodbc
from pyodbc import Connection
import json
import os

def GetJobsFromDb(server="127.0.0.1", user="sa", password="Aa123456", dbName="JobLangInsight") -> set[str]:
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        f"Server={server};"
        f"Database={dbName};"
        f"UID={user};"
        f"PWD={password};"
    )
    cursor = conn.cursor()
    cursor.execute("select id from Job")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    jobIds = set(row.id.strip() for row in rows)
    return jobIds

def GetJobsFromDir(folder="data") -> set[str]:
    files = os.listdir(folder)
    return set(os.path.splitext(f)[0] for f in files if not os.path.isdir(os.path.join(folder, f)))

if __name__ == "__main__":
    jobs = GetJobsFromDir()
    print("xxxxx" in jobs)