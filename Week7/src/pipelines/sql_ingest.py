import sqlite3
import pandas as pd
from pathlib import Path

CSV_PATH = Path("src/data/raw/products-10000.csv")
DB_PATH = Path("src/sql/products.db")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("products", conn, if_exists="replace", index=False)

    conn.close()
    print("✅ SQLite DB created with table: products")

if __name__ == "__main__":
    main()
