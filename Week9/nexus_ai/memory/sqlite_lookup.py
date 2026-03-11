import sqlite3
import os


class SQLiteLookup:

    def __init__(self, db_path=None):

        if db_path is None:
            base_dir = os.path.dirname(__file__)
            db_path = os.path.join(base_dir, "memory.db")

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        self._init_db()

    def _init_db(self):

        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            fact TEXT NOT NULL,
            category TEXT,
            importance REAL
        )
        """)

        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_category ON memories(category)"
        )

        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)"
        )

        self.conn.commit()

    def insert(self, mem_id, fact, category, importance):

        self.conn.execute(
            """
            INSERT INTO memories(id, fact, category, importance)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                fact=excluded.fact,
                category=excluded.category,
                importance=excluded.importance
            """,
            (mem_id, fact, category, importance)
        )

        self.conn.commit()

    def get_by_ids(self, ids):

        if not ids:
            return []

        ids = [str(i) for i in ids]

        placeholders = ",".join(["?"] * len(ids))

        cursor = self.conn.execute(
            f"""
            SELECT id, fact 
            FROM memories
            WHERE id IN ({placeholders})
            """,
            ids
        )

        rows = cursor.fetchall()

        mapping = {str(row["id"]): row["fact"] for row in rows}

        ordered = []

        for i in ids:
            if i in mapping:
                ordered.append(mapping[i])

        return ordered

    def delete(self, mem_id):

        self.conn.execute(
            "DELETE FROM memories WHERE id=?",
            (mem_id,)
        )

        self.conn.commit()

    def clear(self):

        self.conn.execute("DELETE FROM memories")
        self.conn.commit()

    def close(self):
        self.conn.close()