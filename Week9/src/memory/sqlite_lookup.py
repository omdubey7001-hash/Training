import sqlite3
import os


class SQLiteLookup:

    def __init__(self, db_path="src/memory/memory.db"):

        self.db_path = db_path

        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY,
            fact TEXT,
            category TEXT,
            importance REAL
        )
        """)

        self.conn.commit()

    def insert(self, mem_id, fact, category, importance):

        self.conn.execute(
            "INSERT INTO memories VALUES (?, ?, ?, ?)",
            (mem_id, fact, category, importance)
        )

        self.conn.commit()

    def get_by_ids(self, ids):

        if not ids:
            return []

        placeholders = ",".join(["?"] * len(ids))

        cursor = self.conn.execute(
            f"SELECT fact FROM memories WHERE id IN ({placeholders})",
            ids
        )

        rows = cursor.fetchall()

        return [r[0] for r in rows]

    def delete(self, mem_id):

        self.conn.execute(
            "DELETE FROM memories WHERE id=?",
            (mem_id,)
        )

        self.conn.commit()

    def clear(self):

        self.conn.execute("DELETE FROM memories")

        self.conn.commit()