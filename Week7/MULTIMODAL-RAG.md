# Multimodal-Rag

## 1. Overview

This document describes the implementation of a **Multimodal Retrieval-Augmented Generation (RAG)** system that supports:

- 📄 Text → Text Retrieval

- 📄 Text → Image Retrieval

- 🖼 Image → Image Retrieval

- 🖼 Image → Text Retrieval (via Captioning)

The system dynamically routes user input based on modality (text or image) and ensures traceable, low-hallucination retrieval.

## 2. High-Level Architecture
```css
User Input
   |
   ├── Text Input
   |     ├── Text → Text (FAISS + BGE)
   |     └── Text → Image (CLIP)
   |
   └── Image Input
         ├── Image → Image (CLIP)
         └── Image → Caption → Text (BLIP → BGE → FAISS)
```

## 3. Folder Structure (Relevant)
```css
src/
├── embeddings/
│   ├── embedder.py              # Text embeddings (BGE)
│   └── clip_embedder.py         # Image & text embeddings (CLIP)
│
├── pipelines/
│   └── image_ingest.py          # Image embedding pipeline
│
├── retriever/
│   ├── query_engine.py          # Text → Text retrieval
│   ├── text_to_image.py         # Text → Image retrieval
│   ├── image_to_image.py        # Image → Image retrieval
│   ├── image_to_text_rag.py     # Image → Caption → Text
│   └── multimodal_router.py     # Final multimodal router
│
├── vectorstore/
│   ├── index.faiss              # Text FAISS index
│   ├── image.index              # Image FAISS index
│   ├── index_metadata.json
│   └── image_index_metadata.json
```

## 4. Step-1: Image Embedding Pipeline (Day-3 Start)
### Goal

Convert all images into vector embeddings using CLIP and store them in FAISS.

### Model Used

- `openai/clip-vit-base-patch32`

### Command
```bash
python -m src.pipelines.image_ingest
```

### Output

- `src/data/embeddings/images/image_embeddings.npy`

- `src/vectorstore/image.index`

- `src/vectorstore/image_index_metadata.json`

## 5. Step-2: Text → Image Retrieval
### Goal

Given a text query, retrieve the most relevant images.

### Technique

- CLIP text embedding

- FAISS similarity search

### Command
```bash
python -m src.retriever.text_to_image
```

### Example Query
```nginx
financial performance chart
```

### Output (Terminal)
```makefile
Rank 1 | Score 0.2421
PDF: <pdf_id>
Image: <image_path>
Run: timg <image_path>
```
## 6. Step-3: Image → Image Retrieval
### Goal

Find visually similar images given an input image.

### Technique

- CLIP image embeddings

- FAISS cosine similarity

### Command
```bash
python -m src.retriever.image_to_image
```

### Input
```swift
src/data/raw/.../Figure_3.jpeg
```

## 7. Step-4: Image → Text Retrieval (Image RAG)
### Goal

Retrieve text context relevant to an image.

### Pipeline
```css
Image
 ↓
Image Captioning (BLIP)
 ↓
Generated Caption
 ↓
BGE Text Embedding
 ↓
Text FAISS Search
```

### Models Used

- `Salesforce/blip-image-captioning-base`

- `BAAI/bge-small-en`

### Command
```bash
python -m src.retriever.image_to_text_rag
```

### Output

- Generated image caption

- Top-k text chunks related to caption

## 8. Step-5: Multimodal Routing Logic (FINAL)
### Goal

Automatically detect input type and route accordingly.

### Logic

| Input Type | Actions |
|-----------|---------|
| **Text**  | Text → Text Retrieval + Text → Image Retrieval |
| **Image** | Image → Image Retrieval + Image → Caption → Text Retrieval |

## 9. Multimodal Router Implementation
### File
```bash
src/retriever/multimodal_router.py
```

### Command
```bash
python -m src.retriever.multimodal_router
```

### Example Inputs
#### Text Input
```nginx
Explain financial performance risks
```

#### Image Input
```swift
src/data/raw/.../Figure_6.jpeg
```

## 10. Traceability & Hallucination Control

Each retrieved result includes:

- `source_file / pdf_id`

- `chunk_id`

- `image_path`

- similarity score

This ensures:

- ✔ Fully traceable context

- ✔ No fabricated answers

- ✔ Enterprise-grade retrieval

## 11. Models & Techniques Summary

| Component            | Technique            | Model / Tool                              |
|---------------------|----------------------|-------------------------------------------|
| Text Embeddings     | Dense embeddings     | BAAI/bge-small-en                         |
| Image Embeddings    | Vision-language      | openai/clip-vit-base-patch32              |
| Image Captioning    | Vision → Text        | Salesforce/blip-image-captioning-base     |
| Vector Search       | ANN                  | FAISS                                     |
| Multimodal Routing  | Rule-based           | Python Router                             |
| Traceability        | Metadata             | source + chunk_id                         |

## 12. Final Outcome

The system successfully supports:

- Multimodal queries

- Unified vectorstore

- Cross-modal retrieval

- Low hallucination

- Production-ready RAG design