import sqlite3


class DBTool:

    def __init__(self, db_path="tools/tool_db.db"):
        self.conn = sqlite3.connect(db_path)

    def run_query(self, query):

        try:
            cur = self.conn.execute(query)
            rows = cur.fetchall()

            return {
                "success": True,
                "rows": rows[:20]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
