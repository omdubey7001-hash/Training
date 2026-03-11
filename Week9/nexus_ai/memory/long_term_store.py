from .sqlite_lookup import SQLiteLookup


class LongTermMemory:

    def __init__(self):
        self.db = SQLiteLookup()

    def store(self, mem_id, fact, category, importance):

        if not fact:
            return

        self.db.insert(
            mem_id,
            str(fact),
            category or "general",
            float(importance)
        )

    def get_identity_facts(self, limit: int = 10):

        cursor = self.db.conn.execute(
            """
            SELECT fact 
            FROM memories 
            WHERE category='identity'
            ORDER BY importance DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return [r[0] for r in rows] if rows else []

    def get_by_ids(self, ids, limit: int | None = None):

        if not ids:
            return []

        facts = self.db.get_by_ids(ids)

        if not facts:
            return []

        # remove duplicates + preserve order
        seen = set()
        ordered = []

        for f in facts:
            if f not in seen:
                ordered.append(f)
                seen.add(f)

        if limit:
            ordered = ordered[:limit]

        return ordered

    def get_top_facts(self, limit: int = 10):

        cursor = self.db.conn.execute(
            """
            SELECT fact 
            FROM memories
            ORDER BY importance DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return [r[0] for r in rows] if rows else []

    def delete(self, mem_id):
        self.db.delete(mem_id)

    def clear(self):
        self.db.clear()