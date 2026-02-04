import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
VECTOR_DIR = Path("src/vectorstore")
EMB_DIR = Path("src/data/embeddings")
CHUNK_DIR = Path("src/data/chunks")

INDEX_PATH = VECTOR_DIR / "index.faiss"
META_PATH = VECTOR_DIR / "index_metadata.json"

# Load everything once
index = faiss.read_index(str(INDEX_PATH))
metadata = json.loads(META_PATH.read_text())

# Same embedding model used earlier
model = SentenceTransformer("BAAI/bge-small-en")

def search(query: str, top_k: int = 5):
    # Embed query
    query_vec = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    # Search FAISS
    scores, indices = index.search(query_vec, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        meta = metadata[idx]
        chunk_file = CHUNK_DIR / meta["chunk_file"]
        text = chunk_file.read_text(encoding="utf-8", errors="ignore")

        results.append({
            "rank": rank + 1,
            "score": float(scores[0][rank]),
            "source": meta["source_file"],
            "chunk_id": meta["chunk_id"],
            "text": text[:800]  # preview
        })

    return results


if __name__ == "__main__":
    query = input("Enter your question: ")
    results = search(query)

    print("\n--- Top Results ---\n")
    for r in results:
        print(f"Rank {r['rank']} | Score: {r['score']:.4f}")
        print(f"Source: {r['source']} | Chunk: {r['chunk_id']}")
        print(r["text"])
        print("-" * 80)
