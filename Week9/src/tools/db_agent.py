import sqlite3
import re
from typing import Dict, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool


BLOCKED_SQL = re.compile(
    r"\b(UPDATE|DELETE|DROP|ALTER|TRUNCATE|ATTACH|DETACH|PRAGMA)\b",
    re.IGNORECASE
)

INSERT_ALLOWED = re.compile(r"^\s*INSERT\s+INTO\b", re.IGNORECASE)

VALID_TABLE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

MAX_RETURN_ROWS = 200


class SQLiteHelper:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=5
        )

    def get_tables(self, payload: Optional[dict] = None) -> Dict:

        conn = self._connect()

        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )

            tables = [r[0] for r in cursor.fetchall()]

            return {"tables": tables}

        finally:
            conn.close()

    def get_schema(self, payload: Dict) -> Dict:

        tables = payload.get("tables")

        if not tables:
            raise ValueError("Payload must include tables")

        conn = self._connect()

        try:

            schema_info = {}

            for table in tables:

                if not VALID_TABLE.match(table):
                    raise ValueError(f"Invalid table name: {table}")

                cursor = conn.execute(
                    f"SELECT * FROM {table} LIMIT 0"
                )

                schema_info[table] = [
                    {
                        "column": d[0],
                        "type": d[1]
                    }
                    for d in cursor.description
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

        if BLOCKED_SQL.search(sql_clean):
            raise ValueError("Dangerous SQL blocked")

        is_insert = bool(INSERT_ALLOWED.match(sql_clean))

        if is_insert and not allow_write:
            raise ValueError("Write not permitted")

        if "limit" not in sql_clean.lower():
            sql_clean += f" LIMIT {MAX_RETURN_ROWS}"

        conn = self._connect()

        try:

            cursor = conn.execute(sql_clean)

            if cursor.description:

                cols = [d[0] for d in cursor.description]
                rows = cursor.fetchmany(MAX_RETURN_ROWS)

                data = [dict(zip(cols, r)) for r in rows]

                return {
                    "rows": data,
                    "count": len(data)
                }

            conn.commit()

            return {"rows_affected": cursor.rowcount}

        finally:
            conn.close()


DB_AGENT_PROMPT = """
You are a SQL database agent.

RULES:

- If task already contains valid SQL → directly execute run_query tool.
- Otherwise follow reasoning flow:
  1. list_tables
  2. inspect schema
  3. run_query

Always return query results clearly.
Never stop after schema unless user asked for schema.
"""


# ---------- SINGLETON CACHE ---------- #

_db_agent_cache = {}


def create_db_agent(name: str, db_path: str, model_client):

    cache_key = f"{name}:{db_path}"

    if cache_key in _db_agent_cache:
        return _db_agent_cache[cache_key]

    db = SQLiteHelper(db_path)

    tools = [

        FunctionTool(
            name="list_tables",
            description="List tables",
            func=db.get_tables
        ),

        FunctionTool(
            name="get_schema",
            description="Get schema of tables",
            func=db.get_schema
        ),

        FunctionTool(
            name="run_query",
            description="Execute SQL query directly if SQL is already provided",
            func=db.run_query,
        ),
    ]

    agent = AssistantAgent(
        name=name,
        system_message=DB_AGENT_PROMPT,
        model_client=model_client,
        tools=tools,
        max_tool_iterations=6,
    )

    _db_agent_cache[cache_key] = agent

    return agent