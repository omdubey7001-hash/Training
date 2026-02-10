import sqlite3
from pathlib import Path

DB_PATH = Path("src/data/products.db")

def execute_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description]

    conn.close()
    return columns, rows
