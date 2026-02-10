import sqlparse

FORBIDDEN = {"DROP", "DELETE", "UPDATE", "INSERT", "ALTER"}

def validate_sql(sql: str):
    parsed = sqlparse.parse(sql)
    if not parsed:
        raise ValueError("Invalid SQL")

    tokens = [t.value.upper() for t in parsed[0].tokens if t.value]

    for bad in FORBIDDEN:
        if bad in tokens:
            raise ValueError(f"Forbidden keyword detected: {bad}")

    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")

    return True
