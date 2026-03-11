# TOOL-CHAIN.md

## AI Agent Tool Chain Architecture (Day-3)

This document explains how the **Tool Chain system** works in the Agent framework.
The system allows an AI orchestrator to automatically choose the correct tool (File, Database, or Code) to solve a user query.

---

# 1. System Overview

The tool-chain architecture follows this pipeline:

```
User Query
   │
   ▼
Orchestrator (Planner Agent)
   │
   ▼
Execution Plan (JSON Steps)
   │
   ▼
Selected Tool Agent
 ┌──────────────┬──────────────┬──────────────┐
 │ File Agent   │ DB Agent     │ Code Agent   │
 │ (filesystem) │ (SQLite DB)  │ (Python exec)│
 └──────────────┴──────────────┴──────────────┘
   │
   ▼
Results collected in Context
   │
   ▼
Answer Agent (final response)
```

The **Orchestrator decides which tool to use** based on the user's request.

---

# 2. Core Components

## 2.1 Orchestrator

The orchestrator is responsible for:

* Understanding the user query
* Creating a structured **execution plan**
* Running tool agents sequentially
* Passing outputs between steps

Example execution plan:

```json
{
  "steps": [
    {
      "agent": "file",
      "task": "find sales.csv in the project",
      "input_keys": [],
      "output_key": "sales_path"
    },
    {
      "agent": "code",
      "task": "analyze the CSV and generate insights",
      "input_keys": ["sales_path"],
      "output_key": "analysis"
    }
  ]
}
```

---

# 3. Tool Agents

The system contains **three main tool agents**.

---

# 3.1 File Agent

Purpose:

* Search files
* Read files
* Write files
* Locate project resources

Typical tasks:

```
Find sales.csv
Read a txt file
Create a file
List files in directory
```

Example query:

```
Find sales.csv in the project
```

Example output:

```
src/data/sales.csv
```

---

# 3.2 Database Agent

Purpose:

* Query SQLite database
* Inspect schema
* Retrieve records
* Insert new rows

Security rules:

Allowed operations:

```
SELECT
INSERT
```

Blocked operations:

```
UPDATE
DELETE
DROP
ALTER
```

Example query:

```
Show top 5 sales records
```

Example SQL executed:

```sql
SELECT * FROM sales LIMIT 5;
```

---

# 3.3 Code Agent

Purpose:

* Execute Python code
* Perform data analysis
* Process CSV files
* Generate results

The Code Agent uses a **Python execution tool**.

Example tasks:

```
Analyze sales.csv
Generate insights
Create files
Run data processing
```

Example generated code:

```python
import pandas as pd

df = pd.read_csv("src/data/sales.csv")

print(df.head())
```

---

# 4. Context Passing

Each step in the plan can depend on outputs from previous steps.

Example:

```
Step 1 → File Agent
Output → sales_path

Step 2 → Code Agent
Input → sales_path
```

Context dictionary example:

```
{
  "sales_path": "src/data/sales.csv",
  "analysis": "Top product is Laptop"
}
```

---

# 5. Execution Flow Example

User query:

```
Analyze sales.csv and generate top 5 insights
```

Execution flow:

```
User Query
   │
   ▼
Orchestrator
   │
   ▼
Plan Created
   │
   ▼
Step 1 → File Agent
Find CSV path
   │
   ▼
Step 2 → Code Agent
Analyze CSV
   │
   ▼
Results Stored
   │
   ▼
Answer Agent
   │
   ▼
Final Output
```

---

# 6. Example Tool-Chain Use Cases

## File Analysis

```
User: Analyze sales.csv
```

Tools used:

```
File Agent → find CSV
Code Agent → analyze dataset
```

---

## Database Query

```
User: Show all sales records
```

Tools used:

```
DB Agent → run SQL query
```

---

## File Creation

```
User: Create file report.txt and write insights
```

Tools used:

```
Code Agent → generate file
```

---

# 7. Project Directory Structure

Example project layout:

```
Week9/
│
├── database/
│   └── sample.db
│
├── src/
│   ├── agents/
│   ├── tools/
│   │   ├── file_agent.py
│   │   ├── db_agent.py
│   │   └── code_executor.py
│   │
│   ├── data/
│   │   └── sales.csv
│   │
│   ├── orchestrator.py
│   └── main(day3).py
```

---

# 8. Advantages of Tool Chain Architecture

Benefits:

✔ Modular system
✔ Scalable tool integration
✔ Automatic tool selection
✔ Multi-step reasoning
✔ Real-world automation capability

---

# 9. Future Extensions

Possible improvements:

Add tools for:

```
Web search
Email sending
API calls
Vector databases
Memory systems
```

This will transform the system into a **fully autonomous AI agent platform**.

---

# 10. Summary

The Tool Chain system allows the AI agent to:

* Plan tasks
* Select the correct tool
* Execute multi-step workflows
* Combine results into a final answer

The architecture enables **real-world automation using AI agents**.
