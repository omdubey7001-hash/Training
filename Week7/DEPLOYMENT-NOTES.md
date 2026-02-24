# 🚀 Enterprise Multimodal RAG — Deployment Notes (Day 5 Capstone)

---

## 📌 Project Overview

This project implements an **Enterprise Knowledge Intelligence System**
based on **Advanced Retrieval-Augmented Generation (RAG)**.

The system supports:

✔ Text Document Question Answering  
✔ Image-based Retrieval (Multimodal RAG)  
✔ Natural Language → SQL Querying  
✔ Conversational Memory  
✔ Hallucination Detection & Confidence Scoring  
✔ Local LLM + Hybrid Retrieval  

The architecture follows an enterprise-grade GenAI pipeline.

---

## 🧠 System Architecture


User → Streamlit UI → FastAPI → Multimodal Router → Hybrid Retriever → Generator → Evaluation → Response


### Modules

- Hybrid Retriever (Semantic + Keyword + Rerank + MMR)
- Multimodal Router (Text/Image Input Detection)
- SQL Generator Pipeline
- Memory Store (last 5 interactions)
- Evaluation Engine (Faithfulness + Confidence)

---

## 📂 Folder Structure

```
src/
│
├── deployment/
│ ├── api.py
│ ├── app.py
│ ├── ui.py ← Streamlit UI
│
├── retriever/
│ ├── hybrid_retriever.py
│ ├── multimodal_router.py
│
├── generator/
│ ├── query_generator.py
│ ├── sql_generator.py
│
├── pipelines/
│ ├── sql_pipeline.py
│
├── memory/
│ ├── memory_store.py
│
├── evaluation/
│ ├── rag_eval.py
│
├── data/
│ ├── raw/
│ ├── chunks/
│ ├── embeddings/

```
---

## Models Used

**LLM**
- TinyLlama-1.1B-Chat (Local)

**Embeddings**
- BAAI/bge-small-en

**Vision**
- CLIP / BLIP pipelines

**Vector Database**
- FAISS

**Database**
- SQLite

---

## Hybrid Retrieval Pipeline

1. Semantic Search (FAISS)
2. Keyword Search (BM25)
3. Merge + Deduplication
4. Cross-Encoder Reranking
5. MMR Selection

This reduces hallucination and improves grounding.

---

## Memory System

Memory stores:

- Last 5 Q&A interactions
- Context enhancement
- Chat history injection into prompts

File:

`memory/memory_store.py`


---

## Evaluation System

Metrics implemented:

- Context Match Score
- Faithfulness Score
- Hallucination Detection
- Confidence Score

File:

`evaluation/rag_eval.py`


---

## 🌐 API Endpoints

### 1️⃣ TEXT RAG

POST `/ask`

```json
{
  "question": "Gender Diversity"
}
```

Response:
```
{
  "answer": "...",
  "confidence": 0.87,
  "hallucination": false,
  "image": "http://127.0.0.1:8000/data/..."
}
```
### 2️⃣ IMAGE RAG

POST `/ask-image`

Multipart Upload:

`file=<image>`

### 3️⃣ SQL QA

POST `/ask-sql`
```
{
  "question": "Show red products"
}
```
Flow:
```
NL Question → SQL Generator → SQLite Execution → Result Summary
```

## 🎨 Streamlit UI (deployment/ui.py)

The project uses a *Streamlit interface* for rapid prototyping and demonstration.

UI Features:
```
✔ Chat-like interface
✔ Mode Switching (Text / Image / SQL)
✔ Image Upload
✔ Retrieved Image Preview
✔ Confidence + Hallucination Display
```
Example UI Flow:
```
User Input → Streamlit → FastAPI API → Response Rendered
```
## ▶️ Running the Backend

Activate environment:
```bash
source .venv/bin/activate
```
Start FastAPI:
```bash
uvicorn src.deployment.api:app --reload
```
Server:
```code
http://127.0.0.1:8000
```
## 🖥️ Running Streamlit UI
```bash
streamlit run src/deployment/ui.py
```
Open:
```code
http://localhost:8501
```
## 📷 Static Image Serving

FastAPI mounts dataset images:
```python
app.mount("/data"StaticFiles(directory="src/data/raw/data_inside"))
```
Generator converts local image paths into public URLs:
```code
http://127.0.0.1:8000/data/<image_path>
```

## 🧠 Hallucination Prevention
Implemented techniques:

- Context-only answering prompts

- Hybrid retrieval

- Reranking

- Faithfulness scoring

## 🔐 Production Notes

Recommended improvements:

- API key authentication

- Rate limiting

- Structured logging

- Redis memory backend

- Streaming responses

## 🎯 Final Outcome

This system simulates a real enterprise GenAI platform capable of:

- Document Intelligence

- Visual Knowledge Retrieval

- Structured Data Querying

- Faithful Answer Generation

# It looks like this:-

![](/Week7/images/imageis.png)