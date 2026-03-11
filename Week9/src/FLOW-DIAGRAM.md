# FLOW-DIAGRAM.md

**Week 9 — Day 2: Multi-Agent Orchestration Architecture**

---

## Overview

This system implements a **multi-agent architecture** where a **Planner (Orchestrator)** creates a task plan and distributes work to specialized agents.

The architecture follows:

```
Planner → Worker Agents → Reflection Agent → Validator Agent → Final Answer
```

The planner converts the user request into a **Directed Acyclic Graph (DAG)** and executes tasks according to dependencies.

---

# System Architecture

```
User Query
     │
     ▼
┌───────────────┐
│   Planner     │
│ (Orchestrator)│
└───────┬───────┘
        │
        ▼
   Task Graph (DAG)
        │
        ▼
┌─────────────────────────────┐
│      Worker Agents           │
│  (Parallel Execution)        │
│                              │
│  worker_1  worker_2  worker_3│
└──────────────┬───────────────┘
               │
               ▼
        Combined Outputs
               │
               ▼
┌─────────────────────────────┐
│      Reflection Agent        │
│  Improves / Refines Output   │
└──────────────┬───────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Validator Agent         │
│ Checks correctness & errors  │
└──────────────┬───────────────┘
               │
               ▼
           Final Answer
```

---

# Execution Flow

### 1. User Query

The system receives a natural language query from the user.

Example:

```
Explain Artificial Intelligence including history,
algorithms, applications, and future trends.
```

---

### 2. Planner (Orchestrator)

The planner agent:

* analyzes the query
* breaks the task into multiple steps
* constructs a **DAG execution plan**

Example DAG:

```
worker_1 → research AI history
worker_2 → analyze AI algorithms
worker_3 → identify AI applications
worker_4 → explore future trends
reflector → combine all results
validator → verify correctness
```

---

### 3. Task Graph Generation

Example JSON produced by the planner:

```json
{
  "nodes": [
    {"id": "worker_1", "role": "worker", "task": "AI history", "deps": []},
    {"id": "worker_2", "role": "worker", "task": "AI algorithms", "deps": []},
    {"id": "worker_3", "role": "worker", "task": "AI applications", "deps": []},
    {"id": "worker_4", "role": "worker", "task": "AI future trends", "deps": []},
    {"id": "reflector", "role": "reflector", "task": "combine results", "deps": ["worker_1","worker_2","worker_3","worker_4"]},
    {"id": "validator", "role": "validator", "task": "validate answer", "deps": ["reflector"]}
  ]
}
```

This structure represents a **Directed Acyclic Graph (DAG)**.

---

# DAG Execution Model

```
        worker_1
           │
           ├──────────┐
           │          │
        worker_2   worker_3
           │          │
           └────┬─────┘
                │
            worker_4
                │
                ▼
            reflector
                │
                ▼
            validator
                │
                ▼
           Final Answer
```

Workers with **no dependencies run in parallel**.

---

# Parallel Worker Execution

Workers execute concurrently using:

```
asyncio.gather()
```

Benefits:

* faster task completion
* independent sub-task execution
* scalable architecture

Example:

```
worker_1 → AI history
worker_2 → AI algorithms
worker_3 → AI applications
worker_4 → AI future trends
```

All four workers run simultaneously.

---

# Reflection Agent

Purpose:

* combine worker outputs
* remove redundancies
* improve explanation quality
* ensure coherence

Input:

```
worker outputs
```

Output:

```
refined combined answer
```

---

# Validator Agent

Purpose:

* verify factual correctness
* check logical consistency
* detect missing information
* validate completeness

Example checks:

```
✔ facts correct
✔ reasoning valid
✔ explanation complete
```

---

# Agent Responsibilities

| Agent     | Role                       |
| --------- | -------------------------- |
| Planner   | Creates task DAG           |
| Worker    | Executes sub-tasks         |
| Reflector | Improves combined output   |
| Validator | Ensures answer correctness |

---

# Agent Registry Pattern

Agents are registered in a dictionary:

```
agent_registry = {
    "worker": worker_agent,
    "reflector": reflection_agent,
    "validator": validator_agent
}
```

Benefits:

* dynamic agent selection
* modular architecture
* easy agent replacement

---

# Planner–Executor Architecture

```
Planner
   │
   ▼
Task Graph
   │
   ▼
Execution Engine
   │
   ├─ Worker Agents
   ├─ Reflection Agent
   └─ Validator Agent
```

Planner handles **planning**
Agents handle **execution**

---

# Execution Tree (Example)

```
worker_1
   depends on: None

worker_2
   depends on: None

worker_3
   depends on: None

worker_4
   depends on: None

reflector
   depends on: worker_1, worker_2, worker_3, worker_4

validator
   depends on: reflector
```

---

# Key Design Principles

### Separation of Responsibilities

Each agent performs a specific role.

### Parallel Execution

Independent tasks run simultaneously.

### DAG Planning

Ensures correct execution order.

### Modular Architecture

Agents can be added or replaced easily.

---

# Technologies Used

* Python
* AsyncIO
* AutoGen AgentChat
* Local LLM (Qwen2.5 GGUF)
* Planner-Executor Architecture
* Directed Acyclic Graph Execution

---

# Conclusion

This architecture enables **scalable multi-agent systems** where tasks are planned, executed, refined, and validated automatically.

The system demonstrates:

* Planner-Executor architecture
* DAG-based execution
* Parallel worker agents
* Reflection-based improvement
* Validation-based correctness checking

This forms the foundation for **autonomous AI agent systems**.

## To run

python src/day2_main.py
