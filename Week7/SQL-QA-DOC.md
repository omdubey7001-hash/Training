# SQL Question Answering System (Day 4)

This document describes the design and implementation of a **Text → SQL → Answer**
pipeline that converts natural language questions into SQL queries, executes them
safely on a database, and summarizes the results.

---

## 1. Objective

Build a **SQL Question Answering Engine** that can:

- Convert natural language → SQL
- Understand database schema
- Validate generated SQL
- Execute queries safely
- Summarize query results for users

---

## 2. System Architecture

Text Query  
↓  
LLM (SQL Generation)  
↓  
SQL Validation  
↓  
SQLite Execution  
↓  
Result Summarization  

---

## 3. Database Setup

### 3.1 Dataset
- File: `products-10000.csv`
- Rows: 10,000
- Stored in: `src/data/raw/products-10000.csv`

### 3.2 Database
- Engine: **SQLite**
- File: `src/data/products.db`

### 3.3 Import Command
```bash
sqlite3 src/data/products.db
.mode csv
.import src/data/raw/products-10000.csv products
```

Verification:
```bash
sqlite3 src/data/products.db "SELECT COUNT(*) FROM products;"
```

## 4. Schema Loader
### File
```bash
src/utils/schema_loader.py
```
### Purpose

- Automatically extract table schema

- Provide schema context to the LLM

### Output Example
```pysql
products(Index, Name, Description, Brand, Category, Price, Currency, Stock, EAN, Color, Size, Availability, Internal ID)
```

## 5. SQL Generator (LLM)
### File
```bash
src/generator/sql_generator.py
```

### Model Used

- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

### Why TinyLLaMA?

- Lightweight (runs locally)

- Fast inference

- Good instruction-following

- No external API dependency

### Prompting Strategy

- Schema-aware prompting

- Strict SQL-only output

- No explanations or comments

### Example Prompt:
```pgsql
You are an expert SQL generator.
Only generate valid SELECT queries.
Use the provided schema strictly.
```

## 6. SQL Validation
### File
```bash
src/utils/sql_validator.py
```
### Validation Rules

- Only SELECT allowed

- No DROP, DELETE, UPDATE, INSERT

- Prevent SQL injection

- Uses sqlparse

## 7. SQL Execution
### File
```bash
src/utils/sql_executor.py
```

### Safety Features

- Read-only execution

- SQLite cursor execution

- Error handling for malformed SQL

### 8. SQL Pipeline Orchestration
### File
```bash
src/pipelines/sql_pipeline.py
```

### Pipeline Flow

1. Accept user question

2. Load database schema

3. Generate SQL using LLM

4. Validate SQL

5. Execute SQL

6. Print results

7. Summarize output

## 9. Example Run
### User Input
```pgsql
Show total products by category
```

### Generated SQL
```sql
SELECT COUNT(*) AS TotalProducts, Category
FROM products
GROUP BY Category
ORDER BY TotalProducts DESC;
```

### Output
```python-repl
Clothing & Apparel — 320
Kitchen Appliances — 319
Team Sports — 316
...
```

## 10. Result Summarization

- Raw SQL rows are converted into readable output

- Column names preserved

- Suitable for LLM-based explanation in future

## 11. Models & Tools Used

| Component         | Technique     | Model / Tool        |
|-------------------|---------------|---------------------|
| SQL Generation    | LLM           | TinyLLaMA 1.1B      |
| Schema Parsing    | Rule-based    | Python              |
| SQL Validation    | Parsing       | sqlparse            |
| Database          | Relational    | SQLite              |
| Execution         | Safe cursor   | sqlite3             |

## 12. Key Features Achieved

✔ Schema-aware SQL generation
✔ Injection-safe queries
✔ Fully local execution
✔ Deterministic SQL output
✔ Modular pipeline design

