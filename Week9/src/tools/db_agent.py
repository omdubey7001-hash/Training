import sqlite3
import re
from typing import Dict, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool



# SQL Safety Rules
BLOCKED_SQL = re.compile(
    r"\b(UPDATE|DELETE|DROP|ALTER|TRUNCATE|ATTACH|DETACH|PRAGMA)\b",
    re.IGNORECASE
)

INSERT_ALLOWED = re.compile(r"^\s*INSERT\s+INTO\b", re.IGNORECASE)


# Database Utilities
class SQLiteHelper:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_tables(self, payload: Optional[dict] = None) -> Dict:

        conn = self._connect()

        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )

            tables = [r[0] for r in cursor.fetchall()]

            return {"tables": tables}

        finally:
            conn.close()

    def get_schema(self, payload: Dict) -> Dict:

        tables = payload.get("tables")

        if not tables:
            raise ValueError("Payload must include 'tables'")

        conn = self._connect()

        try:

            schema_info = {}

            for table in tables:

                cursor = conn.execute(f"PRAGMA table_info({table})")

                schema_info[table] = [
                    {
                        "column": r[1],
                        "type": r[2],
                        "primary_key": bool(r[5])
                    }
                    for r in cursor.fetchall()
                ]

            return {"schema": schema_info}

        finally:
            conn.close()

    def run_query(self, payload: Dict) -> Dict:

        sql = payload.get("sql")
        allow_write = payload.get("allow_write", False)

        if not sql:
            raise ValueError("SQL query missing")

        sql_clean = sql.strip()

        # Safety validation
        if BLOCKED_SQL.search(sql_clean):
            raise ValueError("Dangerous SQL command blocked")

        is_insert = bool(INSERT_ALLOWED.match(sql_clean))

        if is_insert and not allow_write:
            raise ValueError("Write operation not permitted")

        conn = self._connect()

        try:

            cursor = conn.execute(sql_clean)

            if cursor.description:

                cols = [d[0] for d in cursor.description]
                rows = cursor.fetchall()

                data = [dict(zip(cols, r)) for r in rows]

                return {"rows": data, "count": len(data)}

            conn.commit()

            return {"rows_affected": cursor.rowcount}

        finally:
            conn.close()


# System Prompt
DB_AGENT_PROMPT = """
You are a database agent.

When retrieving data follow this order:

1. list_tables() → see available tables
2. get_schema({"tables": [...]}) → understand structure
3. run_query({"sql": "SELECT ... LIMIT 50"}) → retrieve data

Always inspect schema before querying.

Return results clearly.
"""


# Agent Factory
def create_db_agent(name: str, db_path: str, model_client):

    db = SQLiteHelper(db_path)

    tools = [

        FunctionTool(
            name="list_tables",
            description="Return list of tables in the database",
            func=db.get_tables,
        ),

        FunctionTool(
            name="get_schema",
            description="Return schema of specific tables. Payload: {'tables': ['table1']}",
            func=db.get_schema,
        ),

        FunctionTool(
            name="run_query",
            description="Execute SQL SELECT query. Payload: {'sql': 'SELECT ... LIMIT 50'}",
            func=db.run_query,
        ),
    ]

    return AssistantAgent(
        name=name,
        system_message=DB_AGENT_PROMPT,
        model_client=model_client,
        tools=tools,
        max_tool_iterations=8,
    )