# AGENT-FUNDAMENTALS.md

## Overview

This project demonstrates a basic **Agentic AI pipeline** using Microsoft AutoGen.
The system consists of three specialized agents working together through structured message passing.

**Architecture Flow**

User → ResearchAgent → SummarizerAgent → AnswerAgent

Each agent has a clearly defined role and operates under strict separation of responsibilities.

---

## Core Concepts

### Agentic Loop

All agents follow the same internal cycle:

Perception → Reasoning → Action

* **Perception** — Reads incoming messages and context
* **Reasoning** — Applies system prompt and role rules
* **Action** — Generates response using the model

---

## Role-Based Design

Agents are built with strict job boundaries to maintain clarity and scalability.

### ResearchAgent

**Purpose**

* Collect factual research notes

**Rules**

* No summarization
* No final answers
* Provide structured research information
* Mention uncertainty if needed

---

### SummarizerAgent

**Purpose**

* Compress research into a structured summary

**Rules**

* Highlight key points
* Reduce verbosity
* Maintain factual accuracy

---

### AnswerAgent

**Purpose**

* Produce final user-ready explanation

**Rules**

* Use only summarized input
* Do not introduce new research
* Provide clear and simple explanation

---

## Model Architecture

The system uses a layered design:

AssistantAgent (Agent Logic)
↓
LlamaCppChatCompletionClient (Model Interface)
↓
Local GGUF Model (Qwen)

**Key Characteristics**

* Local inference (no cloud API)
* Token-based processing
* Shared model instance across agents

---

## Memory Design

Memory is indirectly controlled through model configuration:

* `n_ctx = 2048`
* `max_tokens = 256`

This creates an effective **memory window** that limits how much past conversation each agent perceives.

**Why memory control matters**

* Prevents context overflow
* Maintains stable reasoning loops
* Improves performance in multi-agent pipelines

---

## Message Passing

Agents communicate using AutoGen’s internal message system.

Instead of manually passing text between agents:

RoundRobinGroupChat manages conversation flow automatically.

**Benefits**

* Shared context
* Cleaner orchestration
* Easier scalability

---

## Termination Logic

Execution stops after a fixed number of messages:

MaxMessageTermination(4)

Execution Order:

1. User input
2. ResearchAgent
3. SummarizerAgent
4. AnswerAgent

---

## To run it

python "src/main(day1).py"