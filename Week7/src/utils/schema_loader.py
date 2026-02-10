# src/utils/schema_loader.py
import sqlite3


def load_schema(db_path="src/data/products.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table';
    """)

    tables = cursor.fetchall()
    schema = []

    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        cols = cursor.fetchall()
        col_names = [c[1] for c in cols]
        schema.append(f"{table}({', '.join(col_names)})")

    conn.close()
    return "\n".join(schema)
