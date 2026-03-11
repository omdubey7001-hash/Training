# TOOL-CHAIN.md — Multi-Agent Tool Orchestration System

## Project Overview

This project implements a **Multi-Agent Tool Orchestration System** where an intelligent **Planner Agent** dynamically decides how to solve a user task by routing it to specialized tool agents such as:

* File Agent (filesystem operations)
* Database Agent (SQLite + SQL reasoning)
* Code Agent (Python execution & analytics)
* Answer Agent (grounded final response)

The system supports **multi-step reasoning, context passing, automation, and real execution of tools.**

---

## High Level Architecture

```
User Query
   ↓
Planner Agent (Task Decomposition)
   ↓
Orchestrator (Execution Controller)
   ↓
Tool Agents (File | DB | Code)
   ↓
Context Aggregation / Memory
   ↓
Answer Agent (Final User Response)
```

---

## Core Components

### Planner Agent — Brain of System

**Responsibilities**

* Understand user intent
* Break task into ordered execution steps
* Decide which tool agent to use
* Generate STRICT JSON execution plan

**Example Plan**

```json
{
  "steps": [
    {
      "agent": "file",
      "task": "Locate sales.csv",
      "input_keys": [],
      "output_key": "file_path"
    },
    {
      "agent": "code",
      "task": "Analyze CSV and generate insights",
      "input_keys": ["file_path"],
      "output_key": "analysis"
    }
  ]
}
```

---

### Orchestrator — Execution Manager

**Responsibilities**

* Calls planner agent
* Parses execution plan
* Runs tool agents sequentially
* Maintains execution context
* Handles step failures
* Summarizes outputs

**Execution Loop**

```
for each step:
   prepare context
   execute tool
   store output
```

---

## Tool Agents

---

### File Agent

**Capabilities**

* Locate files in project
* List directories
* Read file contents
* Write / append files

**Typical Tasks**

* Find dataset
* Show file content
* Create notes.txt

**Output Example**

```
src/data/sales.csv
```

---

### Database Agent (SQLite)

**Capabilities**

* Discover tables
* Inspect schema
* Execute SELECT queries
* Return structured rows

**Reasoning Flow**

```
list_tables → get_schema → run_query
```

**Output Example**

| id | product | revenue |
| -- | ------- | ------- |
| 1  | Laptop  | 5000    |
| 2  | Phone   | 3000    |

---

### Code Execution Agent

**Capabilities**

* Execute Python scripts
* Generate synthetic datasets
* Perform pandas analytics
* Create new CSV / TXT files
* Return execution logs

**Example Tasks**

* Create CSV with random numbers
* Analyze revenue trends
* Generate factorial script

**Output Example**

```
workspace/random_numbers.csv
```

---

## Multi-Step Orchestration Example

### User Query

> Analyze sales.csv and generate top 5 insights

### Execution Flow

```
Step 1 → File Agent → Locate dataset
Step 2 → Code Agent → Perform pandas analysis
Step 3 → Answer Agent → Present insights
```

### Sample Insights Generated

* Electronics category has highest revenue
* West region leads total sales
* Credit Card is most used payment method
* Amit Verma is top performing sales rep
* Electronics receives highest discount %

---

## Context Passing Mechanism

Context is maintained as:

```python
context = {
   "file_path": "src/data/sales.csv",
   "analysis": "Top insights..."
}
```

Each step can access previous outputs using `input_keys`.

---

## Answer Agent — Grounded Response Layer

**Responsibilities**

* Use only tool outputs
* Avoid hallucination
* Present structured user-friendly response

---

## Safety & Reliability Features

* Planner tool usage disabled
* SQL dangerous commands blocked
* Code execution sandboxed (workspace)
* Step failure handling
* JSON plan validation
* Retry logic for planner failures
* Relative file paths for portability

---

## System Validation Tests

### File Tool Test

```
Find sales.csv file
```

### Database Tool Test

```
Show first 2 rows from sales table
```

### Code Tool Test

```
Create csv with random numbers
```

### Multi-Tool Test

```
Analyze sales.csv and generate insights
```

---


## Final Status

- Planner Routing Working
- File Tool Working
- DB Tool Working
- Code Execution Working
- Multi-Step Orchestration Successful
- Grounded Answer Generation Enabled

---

## Project Outcome

A **functional multi-agent automation system** capable of:

* File discovery
* Database analytics
* Python execution
* Data pipeline automation
* Insight generation
* Autonomous task decomposition

---
