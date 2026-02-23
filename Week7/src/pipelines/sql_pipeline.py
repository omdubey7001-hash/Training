from src.generator.sql_generator import SQLGenerator
from src.utils.schema_loader import load_schema
from src.utils.sql_validator import validate_sql
from src.utils.sql_executor import execute_sql


def ask_sql(question):
    schema = load_schema()
    print("\n--- DATABASE SCHEMA ---")
    print(schema)

    generator = SQLGenerator()
    sql = generator.generate(question, schema)

    print("\n--- GENERATED SQL ---")
    print(sql)

    validate_sql(sql)

    cols, rows = execute_sql(sql)

    return cols, rows

