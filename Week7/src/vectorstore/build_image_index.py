import json
import faiss
import numpy as np
from pathlib import Path

EMB_DIR = Path("src/data/embeddings/images")
VECTOR_DIR = Path("src/vectorstore")

VECTOR_DIR.mkdir(exist_ok=True)

EMB_PATH = EMB_DIR / "image_embeddings.npy"
META_PATH = EMB_DIR / "image_metadata.json"

INDEX_PATH = VECTOR_DIR / "image.index"
INDEX_META_PATH = VECTOR_DIR / "image_index_metadata.json"


def main():
    embeddings = np.load(EMB_PATH).astype("float32")

    with open(META_PATH, "r") as f:
        metadata = json.load(f)

    dim = embeddings.shape[1]

    # Cosine similarity via inner product
    index = faiss.IndexFlatIP(dim)

    # Normalize embeddings
    faiss.normalize_L2(embeddings)

    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with open(INDEX_META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Image FAISS index created")
    print(f"Vectors: {index.ntotal}")
    print(f"Saved at: {INDEX_PATH}")


if __name__ == "__main__":
    main()
