from .sqlite_lookup import SQLiteLookup


class LongTermMemory:

    def __init__(self):

        self.db = SQLiteLookup()

    def store(self, mem_id, fact, category, importance):

        self.db.insert(
            mem_id,
            fact,
            category,
            importance
        )

    def get_identity_facts(self):

        cursor = self.db.conn.execute(
            "SELECT fact FROM memories WHERE category='identity'"
        )

        rows = cursor.fetchall()

        return [r[0] for r in rows]

    def get_by_ids(self, ids):

        return self.db.get_by_ids(ids)

    def delete(self, mem_id):

        self.db.delete(mem_id)

    def clear(self):

        self.db.clear()