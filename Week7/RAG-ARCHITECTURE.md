# Enterprise RAG System — Architecture Overview

This document describes the architecture of an enterprise-grade Retrieval Augmented Generation (RAG) system built to answer questions from large, unstructured internal documents.

The system supports:
- Ingestion of enterprise documents (Markdown, PDFs, TXT)
- Semantic search using vector embeddings
- Traceable and non-hallucinated retrieval
- Extensibility to local or hosted LLMs


## High-Level Architecture

The RAG system follows a standard Retriever → Generator architecture.

Data flows through the system in the following stages:

1. Document Ingestion
2. Text Chunking
3. Metadata Attachment
4. Embedding Generation
5. Vector Indexing (FAISS)
6. Query-Time Retrieval
7. (Future) LLM-based Answer Generation

### Architecture Flow
```
Raw Enterprise Documents
            ↓
Text Cleaning & Normalization
            ↓
Chunking (500–800 tokens, overlap)
            ↓
Chunks + Metadata
            ↓
Embedding Model (BAAI/bge-small-en)
            ↓
Vector Database (FAISS)
            ↓
Retriever (Top-K Semantic Search)
```

## Document Ingestion

The ingestion layer loads raw enterprise documents stored in nested directory structures.
These documents may include financial reports, policy manuals, and structured markdown files.

Responsibilities:
- Traverse nested folders
- Read supported formats (Markdown, TXT, CSV)
- Normalize text for downstream processing

Command: `python -m src.pipelines.ingest`

Output:
- Cleaned plain-text documents
```
Found 100 markdown files
Saved → src/data/cleaned/EnterpriseRAG_2025_02_markdown_xxx.txt
```

## Chunking Strategy

Large documents are split into smaller overlapping chunks to fit within LLM token limits
and improve semantic retrieval accuracy.

Configuration:
- Chunk size: 500–800 tokens
- Overlap: 100 tokens

Rationale:
- Prevents loss of context at chunk boundaries
- Improves recall during retrieval

## Metadata Management

Each chunk is enriched with lightweight metadata to ensure traceability and auditability.

Metadata fields include:
- Source document name
- Chunk ID

This allows the system to trace every retrieved chunk back to its original document,
which is essential for enterprise compliance and debugging.

Command: `python -m src.pipelines.generate_metadata`

## Embedding Generation

Text chunks are converted into dense vector representations using a sentence-transformer
embedding model.

Model characteristics:
- Lightweight embedding model suitable for CPU execution
- Normalized embeddings for cosine similarity search

Embeddings capture the semantic meaning of each chunk and enable efficient similarity search.

Command: `python -m src.pipelines.build_embeddings`

## Vector Store (FAISS)

All embeddings are stored in a FAISS vector index for fast semantic search.

Index type:
- Flat Inner Product (cosine similarity)

Reasons for choosing FAISS:
- High performance on large vector collections
- Fully local and offline
- Widely used in production RAG systems

Command: `python -m src.pipelines.build_faiss`

## Retriever (Query Engine)

At query time, the system performs the following steps:

1. Convert user query into an embedding
2. Perform Top-K similarity search against the FAISS index
3. Retrieve the most relevant chunks along with metadata

The retriever returns raw knowledge chunks, not final answers.
This separation ensures modularity and prevents hallucinations.

Command:`python -m src.retriever.query_engine`

## Hallucination Control and Reliability

The system minimizes hallucinations by design:

- Only retrieved document chunks are used as context
- Every result is traceable to a source document
- The retriever and generator responsibilities are strictly separated

This design aligns with enterprise requirements for accuracy and explainability.

## Extensibility and Deployment Modes

The architecture supports multiple deployment modes:

- Fully local execution using open-source models
- Hosted LLM APIs (OpenAI, Claude, Gemini)

The retriever, chunking, and vector store remain unchanged.
Only the generator component is swapped via configuration.

This ensures vendor independence and enterprise control.

## Current Status (Day 1)

Implemented:
- Document ingestion
- Chunking and metadata
- Embedding generation
- FAISS vector indexing
- Semantic retriever

