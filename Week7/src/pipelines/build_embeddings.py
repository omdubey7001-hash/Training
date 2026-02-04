import json
import numpy as np
from pathlib import Path
from src.embeddings.embedder import Embedder

CHUNK_DIR = Path("src/data/chunks")
META_FILE = Path("src/data/chunks_metadata.json")
OUT_DIR = Path("src/data/embeddings")

OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    metadata = json.loads(META_FILE.read_text())
    embedder = Embedder()

    texts = []
    index_to_chunk = []

    for i, item in enumerate(metadata):
        chunk_path = CHUNK_DIR / item["chunk_file"]
        text = chunk_path.read_text(encoding="utf-8", errors="ignore")

        if not text.strip():
            continue

        texts.append(text)
        index_to_chunk.append(item)

    print(f"Generating embeddings for {len(texts)} chunks")

    embeddings = embedder.embed(texts)

    np.save(OUT_DIR / "embeddings.npy", embeddings)
    json.dump(index_to_chunk, open(OUT_DIR / "index_to_chunk.json", "w"), indent=2)

    print("Embeddings saved successfully")

if __name__ == "__main__":
    main()
