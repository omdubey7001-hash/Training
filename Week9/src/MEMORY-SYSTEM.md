# AI Memory System Documentation

## Overview

This project implements a multi-layer AI memory system designed for conversational agents.
The system stores, retrieves, and updates user-related knowledge across sessions using a hybrid architecture.

The memory system consists of three major components:

1. **Session Memory**
2. **Vector Memory (Semantic Memory)**
3. **Long-Term Memory (Persistent Database)**

---

# Memory Architecture

```
User Query
   │
   ▼
Session Memory
   │
   ▼
Vector Search (FAISS)
   │
   ▼
Long-Term Memory (SQLite)
   │
   ▼
Context Injection into LLM
```

---

# Components

## 1. Session Memory

File: `session_memory.py`

Purpose:

* Stores the most recent conversation messages
* Helps maintain short-term conversational context

Implementation:

* Uses a deque buffer
* Default size: 20 messages

Example:

```
User: Hi
Agent: Hello!

User: My name is Om
Agent: Nice to meet you
```

Session memory ensures the agent remembers the current conversation flow.

---

## 2. Vector Store (Semantic Memory)

File: `vector_store.py`

Purpose:

* Enables semantic search across stored memories.
* Uses embeddings to retrieve relevant facts.

Technology:

* FAISS
* Sentence Transformers (`all-MiniLM-L6-v2`)

Process:

```
Fact
   ↓
Embedding
   ↓
FAISS Index
   ↓
Similarity Search
```

Stored files:

```
vector.index
vector_meta.json
```

These files allow persistent semantic memory between sessions.

---

## 3. Long-Term Memory

File: `long_term_store.py`

Purpose:

* Stores extracted user facts permanently.

Database:

* SQLite

Database file:

```
memory.db
```

Table schema:

```
memories
----------------------------
id
fact
category
importance
```

Example stored facts:

```
User's name is Om Ji Dubey
User prefers Java programming
User is a BTech CSE student
```

---

# Fact Extraction

Facts are extracted using the LLM.

Process:

```
Conversation
   ↓
LLM summarization
   ↓
Structured JSON facts
```

Example output:

```
[
  {
    "fact": "User's name is Om Ji Dubey",
    "category": "identity",
    "importance": 1.0
  }
]
```

---

# Memory Reconciliation

File: `memory_manager.py`

When a new fact appears, the system compares it with existing facts.

Possible relations:

```
DUPLICATE
CONTRADICTS
UPDATES
MERGEABLE
UNRELATED
```

Example:

```
Old Fact: User lives in Delhi
New Fact: User lives in Noida
```

Relation: **UPDATES**

Result:

```
User lives in Noida
```

---

# Memory Retrieval

When the user asks a question:

```
User Query
   ↓
Vector Search
   ↓
Fetch memory IDs
   ↓
Retrieve facts from SQLite
   ↓
Inject into prompt
```

Example:

User query:

```
What is my name?
```

Retrieved memory:

```
User's name is Om Ji Dubey
```

---

# Data Flow

```
User Message
      │
      ▼
Session Memory
      │
      ▼
Fact Extraction (LLM)
      │
      ▼
Vector Store
      │
      ▼
Long-Term SQLite Store
```

---

# Files in Memory System

```
memory/
│
├── memory_manager.py
├── vector_store.py
├── long_term_store.py
├── session_memory.py
├── sqlite_lookup.py
│
├── memory.db
├── vector.index
└── vector_meta.json
```

---

# Key Features

* Persistent memory across sessions
* Semantic memory retrieval
* Duplicate fact detection
* Memory reconciliation
* Context-aware responses

---

# Conclusion

This memory system provides a scalable architecture for AI agents to remember user information across conversations.

By combining:

* Session memory
* Vector semantic memory
* Persistent long-term storage

the system enables intelligent, context-aware interactions.
