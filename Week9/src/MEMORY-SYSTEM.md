# AI Memory System Documentation

## Overview

This project implements a **multi-layer cognitive memory system** for conversational AI agents.

The system enables the agent to:

* Remember user facts across sessions
* Perform semantic recall
* Update / merge / delete memories intelligently
* Maintain short-term conversational context
* Persist structured knowledge in a database

The architecture follows a **hybrid memory design** inspired by real agent frameworks (AutoGen, LangGraph, CrewAI).

---

# Memory Architecture

```
User Query
   │
   ▼
Session Memory (Short Term)
   │
   ▼
Vector Semantic Search (FAISS)
   │
   ▼
Long Term Memory Fetch (SQLite)
   │
   ▼
Context Injection → LLM Response
   │
   ▼
Fact Extraction → Memory Update
```

---

# Memory Layers

## 1. Session Memory (Short-Term Memory)

File: `session_memory.py`

### Purpose

* Stores recent conversation messages
* Maintains conversational continuity
* Helps LLM understand dialogue flow

### Implementation

* Uses `collections.deque`
* Sliding window buffer (default size: 20 messages)
* In-memory only (not persistent)

### Example

```
User: Hi
Agent: Hello!

User: I am Om Ji Dubey
Agent: Nice to meet you
```

---

## 2. Vector Store (Semantic Memory)

File: `vector_store.py`

### Purpose

* Enables semantic similarity search
* Retrieves relevant memories even when wording differs

### Technology

* FAISS IndexFlatIP
* SentenceTransformers model: `all-MiniLM-L6-v2`
* Cosine similarity via normalized embeddings

### Storage Files

```
vector.index        → FAISS index
vector_meta.json    → ID + text mapping
```

### Flow

```
Fact Text
   ↓
Embedding
   ↓
Stored in FAISS
   ↓
Similarity Search during retrieval
```

### Features

* Persistent semantic index
* Safe rebuild on delete
* Backward-compatible metadata loading
* String UUID memory IDs
* Normalized vector scoring

---

## 3. Long-Term Memory (Persistent Knowledge Store)

File: `long_term_store.py`

Backend: `sqlite_lookup.py`

### Purpose

* Stores structured user facts permanently
* Supports identity memory and importance ranking

### Database

SQLite database file:

```
memory.db
```

### Table Schema

```
memories
----------------------------
id TEXT PRIMARY KEY
fact TEXT
category TEXT
importance REAL
```

### Indexed Columns

* category
* importance

### Example Stored Facts

```
User name is Om Ji Dubey
User prefers Java programming
User is a BTech CSE student
```

---

# Fact Extraction Pipeline

Facts are extracted using an LLM summarization step.

### Flow

```
Conversation Turn
   ↓
LLM Prompt
   ↓
Structured JSON Fact Output
```

### Example Output

```
[
  {
    "fact": "User name is Om Ji Dubey",
    "category": "identity",
    "importance": 1.0
  }
]
```

Only facts with **importance ≥ threshold** are stored.

---

# Memory Reconciliation Engine

File: `memory_manager.py`

When new facts are detected, the system compares them with existing semantic memories.

### Possible Relations

```
DUPLICATE     → ignore
CONTRADICTS   → replace old fact
UPDATES       → replace old fact
MERGEABLE     → combine facts
UNRELATED     → store as new memory
```

### Example

```
Old Fact: User lives in Delhi
New Fact: User lives in Noida
```

Result:

```
Old memory deleted
New memory stored
```

---

# Memory Retrieval Pipeline

When the user asks a question:

```
User Query
   ↓
Embedding
   ↓
FAISS similarity search
   ↓
Memory IDs retrieved
   ↓
SQLite fact lookup
   ↓
Context injection into LLM
```

### Example

User:

```
Who am I?
```

Retrieved memory:

```
User name is Om Ji Dubey
```

Agent Response:

```
You are Om Ji Dubey.
```

---

# Data Storage Flow

```
User Message
      │
      ▼
Session Memory (RAM)
      │
      ▼
Fact Extraction (LLM reasoning)
      │
      ▼
Vector Store (semantic index)
      │
      ▼
SQLite Persistent Store
```

---

# Memory ID Strategy

* Uses **UUID string identifiers**
* Prevents SQLite integer overflow
* Compatible with FAISS metadata mapping
* Ensures safe distributed scaling

---

# Key System Features

* Persistent long-term memory across sessions
* Semantic recall using embeddings
* Intelligent memory reconciliation
* Importance-based memory filtering
* Identity memory fallback retrieval
* Safe schema handling and migration awareness
* Context-aware conversational responses
* Hybrid short-term + long-term cognition

---

# Project Structure

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

# Future Enhancements (Planned)

* Hybrid retrieval scoring (similarity + importance + recency)
* Memory decay / forgetting mechanism
* Episodic vs semantic memory separation
* Background summarization worker
* Context compression before LLM call
* Multi-user namespace support
* Conflict audit logs
* Batch embedding pipeline

---

# Conclusion

This AI memory system provides a **scalable cognitive architecture** for conversational agents.

By combining:

* Short-term session memory
* Semantic vector memory
* Persistent structured storage

the agent achieves **human-like memory behaviour**, enabling intelligent, evolving, and context-aware interactions.
