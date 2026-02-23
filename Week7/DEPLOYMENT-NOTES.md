# Enterprise Multimodal RAG — Deployment Notes (Day 5 Capstone)

## Project Overview

This project implements an **Enterprise Knowledge Intelligence System**
based on Advanced Retrieval-Augmented Generation (RAG).

The system supports:

✔ Text Document Question Answering  
✔ Image-based Retrieval (Multimodal RAG)  
✔ Natural Language → SQL Querying  
✔ Conversational Memory  
✔ Hallucination Detection & Confidence Scoring  
✔ Local LLM + Hybrid Retrieval  

The architecture follows an enterprise-grade GenAI pipeline.

------------------------------------------------------------

## System Architecture

User → API → Multimodal Router → Retriever → Generator → Evaluator → Response

Modules:

- Hybrid Retriever (Semantic + Keyword + Rerank + MMR)
- Multimodal Router (Text/Image Input Detection)
- SQL Generator Pipeline
- Memory Store (last 5 interactions)
- Evaluation Engine (Faithfulness + Confidence)

------------------------------------------------------------

## Folder Structure
```
src/
│
├── deployment/
│   ├── api.py
│   ├── app.py
│
├── retriever/
│   ├── hybrid_retriever.py
│   ├── multimodal_router.py
│
├── generator/
│   ├── query_generator.py
│   ├── sql_generator.py
│
├── pipelines/
│   ├── sql_pipeline.py
│
├── memory/
│   ├── memory_store.py
│
├── evaluation/
│   ├── rag_eval.py
│
├── data/
│   ├── raw/
│   ├── chunks/
│   ├── embeddings/
│   ├── vectorstore/
```
------------------------------------------------------------

## Models Used

LLM:
- `TinyLlama-1.1B-Chat (Local)`

Embeddings:
- `BAAI/bge-small-en`

Vision:
- `CLIP / BLIP pipelines`

Vector Database:
- `FAISS`

Database:
- `SQLite`

------------------------------------------------------------

## Hybrid Retrieval Pipeline

Steps:

1. Semantic Search (FAISS)
2. Keyword Search (BM25)
3. Merge + Deduplication
4. Cross-Encoder Reranking
5. MMR Selection

This reduces hallucination and improves grounding.

------------------------------------------------------------

## Memory System

Memory stores:

- Last 5 Q&A interactions
- Context enhancement
- Chat history injection into prompts

File:
`memory/memory_store.py`

------------------------------------------------------------

## Evaluation System

Metrics implemented:

- Context Match Score
- Faithfulness Score
- Hallucination Detection
- Confidence Score

File:
`evaluation/rag_eval.py`

------------------------------------------------------------

## API Endpoints

### 1 TEXT RAG

POST /ask

Request:
```
{
  "question": "Gender Diversity"
}
```
```
Response:
{
  "answer": "...",
  "confidence": 0.87,
  "hallucination": false,
  "image": "<optional image url>"
}
```
------------------------------------------------------------

### 2 IMAGE RAG

POST /ask-image

Multipart Upload:
file=<image>

Response:
{
  "answer": "...",
  "image": "<retrieved image>"
}

------------------------------------------------------------

### 3 SQL QA

POST /ask-sql

Request:
{
  "question": "Show red products"
}

System Flow:

NL Question → SQL Generator → SQLite Execution → Result Summary

------------------------------------------------------------

## Frontend (React + Vite)

UI Features:
```
✔ Chat Interface
✔ Mode Switching (Ask / Image / SQL)
✔ Image Upload
✔ Confidence Display
✔ Hallucination Flag
```
Image Rendering:

<img src=![](SS/image.png) />

------------------------------------------------------------

## Running the Backend

Activate environment:

`source .venv/bin/activate`

Start API:

`uvicorn src.deployment.api:app --reload`

Server:
`http://127.0.0.1:8000`

------------------------------------------------------------

## Running Frontend

cd rag-ui
npm install
npm run dev

Frontend:
http://localhost:5173

------------------------------------------------------------

## Static Image Serving

FastAPI mounts image directory:

`app.mount("/data", StaticFiles(directory="src/data/raw/data_inside"))`

Generator returns public URL:

http://127.0.0.1:8000/data/<image_path>

------------------------------------------------------------

## Hallucination Prevention

Implemented:

- Context-only answering prompt
- Hybrid retrieval
- Reranking
- Faithfulness scoring

------------------------------------------------------------

## Production Notes

Recommended:

- Add API key auth
- Rate limiting
- Structured logging
- Redis memory backend
- Async streaming responses

------------------------------------------------------------

## Completion Checklist (Day 5)

✔ Multimodal RAG Working  
✔ Hybrid Retriever Implemented  
✔ SQL QA Pipeline Running  
✔ Memory Integration  
✔ Evaluation Metrics  
✔ FastAPI Deployment  
✔ React UI Connected  

------------------------------------------------------------

## Final Outcome

![](SS/image.png)

This system simulates a real enterprise GenAI platform capable of:

- Document Intelligence
- Visual Knowledge Retrieval
- Structured Data Querying
- Faithful Answer Generation
