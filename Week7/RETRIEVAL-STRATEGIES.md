# Retrieval Strategies — Day 2
## Hybrid Retrieval, Reranking & MMR

This document describes the retrieval strategies implemented on Day-2
to build an enterprise-grade, low-hallucination Retrieval-Augmented
Generation (RAG) system.

The goal is to retrieve **high-precision, diverse, and fully traceable**
context chunks before passing them to an LLM.

---

## 1. Overview of Retrieval Pipeline

The final retrieval pipeline is as follows:

Semantic Retrieval (Vector Search - FAISS)
+ Keyword Retrieval (BM25)
→ Merge & Deduplication
→ Cross-Encoder Reranking
→ Max Marginal Relevance (MMR)
→ Final Context for LLM

This multi-stage approach balances:
- Recall (finding all relevant content)
- Precision (ranking the best content)
- Diversity (avoiding redundant chunks)
- Traceability (source + chunk references)

---

## 2. Semantic Retrieval (Vector Search)

### Technique
- Dense vector similarity search using FAISS
- Embeddings generated using Sentence Transformers

### Model Used
- **BAAI/bge-small-en**

### Why?
- Strong performance for semantic similarity
- Lightweight and CPU-friendly
- Industry-recommended for RAG pipelines

### Implementation
Semantic retrieval is implemented in: `src/retriever/query_engine.py`


The query is embedded and searched against the FAISS index.

### Command Used
```bash
python -m src.retriever.query_engine
```

---

## 3. Keyword Retrieval (BM25)
### Technique

Traditional lexical search using BM25

Acts as a fallback for exact matches (section numbers, names, codes)

### Library Used

- `rank_bm25`

### Why?

Semantic models may miss exact terms

BM25 ensures recall for precise keywords

### Implementation

Keyword retrieval is implemented in:
```bash
src/retriever/hybrid_retriever.py
```

(Class: `KeywordRetriever`)

### Command Used

Triggered automatically via:
```bash
python -m src.retriever.hybrid_retriever
```

---

## 4. Merge & Deduplication
### Problem Addressed

Same chunk can appear in both semantic and keyword results

### Solution

- Merge results from both retrievers

- Deduplicate using (source, chunk_id) as unique keys

### Implementation
```bash
src/retriever/merge_utils.py
```

### Outcome

- Prevents repeated context

- Ensures clean candidate set for reranking

---

## 5. Cross-Encoder Reranking
### Technique

Cross-Encoder reranking (query + chunk evaluated together)

### Model Used

`cross-encoder/ms-marco-MiniLM-L-6-v2`

### Why Cross-Encoder?

- Much higher precision than cosine similarity

- Reads query and chunk jointly

- Used in production search engines

### When Applied

- After merge & deduplication

- On a small candidate set (Top-10)

### Implementation
```bash
src/retriever/reranker.py
```

### Command Used
```bash
python -m src.retriever.hybrid_retriever
```

### Notes

- Rerank scores can be negative (expected behavior)

- Relative ranking matters, not absolute score

---

## 6. Max Marginal Relevance (MMR)
### Problem Addressed

Top results often come from the same section

Redundant context increases hallucination risk

### Technique

- Max Marginal Relevance (MMR)

- Balances relevance and diversity

### Formula (Conceptual)
```ini
MMR = λ · relevance − (1 − λ) · redundancy
```

### Parameters Used

`lambda = 0.7` (favor relevance with controlled diversity)

### Implementation
```bash
src/retriever/mmr.py
```

### Outcome

- Diverse but relevant chunks

- Better coverage across sections

- Optimized context window for LLMs

---

## 7. Traceable Context Sources

Each retrieved chunk carries metadata:

- Source document name

- Chunk identifier

- Original text

### Example:
```yaml
Source: EnterpriseRAG_2025_02_markdown_xxx.txt
Chunk ID: 706
```

### Why This Matters

- Enables auditability

- Reduces hallucinations

- Required in enterprise (banking, legal, insurance)

---

## 8. Final Retriever Execution
### Command Used
```bash
python -m src.retriever.hybrid_retriever
```
### Output Stages

- Merged & deduplicated results

- Cross-encoder reranked results

- Final MMR-selected chunks

- Text previews with source & chunk IDs

---

## Models and Techniques

| Component             | Technique            | Model / Tool                         |
|----------------------|----------------------|--------------------------------------|
| Semantic Retrieval   | Dense embeddings     | BAAI/bge-small-en                    |
| Keyword Retrieval    | BM25                 | rank_bm25                            |
| Vector Search        | Approx. NN Search    | FAISS                                |
| Reranking            | Cross-Encoder        | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| Diversity Selection  | Max Marginal Relevance (MMR) | Cosine similarity              |
| Traceability         | Metadata tagging     | source file + chunk_id               |
