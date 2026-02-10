from src.generator.sql_generator import SQLGenerator
from src.utils.schema_loader import load_schema
from src.utils.sql_validator import validate_sql
from src.utils.sql_executor import execute_sql


def main():
    question = input("Ask SQL question: ")

    schema = load_schema()
    print("\n--- DATABASE SCHEMA ---")
    print(schema)

    generator = SQLGenerator()
    sql = generator.generate(question, schema)

    print("\n--- GENERATED SQL ---")
    print(sql)

    validate_sql(sql)

    cols, rows = execute_sql(sql)

    print("\n--- RESULT ---")
    print(cols)
    for r in rows[:10]:
        print(r)


if __name__ == "__main__":
    main()
