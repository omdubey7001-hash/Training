import json
import numpy as np
import faiss
from pathlib import Path

EMB_DIR = Path("src/data/embeddings")
OUT_DIR = Path("src/vectorstore")

OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    embeddings = np.load(EMB_DIR / "embeddings.npy")
    metadata = json.loads((EMB_DIR / "index_to_chunk.json").read_text())

    print(f"Loaded embeddings: {embeddings.shape}")

    dim = embeddings.shape[1]

    # Flat index (accurate, simple – best for Day 1)
    index = faiss.IndexFlatIP(dim)

    # embeddings already normalized → inner product = cosine similarity
    index.add(embeddings)

    faiss.write_index(index, str(OUT_DIR / "index.faiss"))
    json.dump(metadata, open(OUT_DIR / "index_metadata.json", "w"), indent=2)

    print("FAISS index built successfully")

if __name__ == "__main__":
    main()
