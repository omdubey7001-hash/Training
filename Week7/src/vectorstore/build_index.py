import faiss
import os
import json
from pathlib import Path
from src.embeddings.embedder import Embedder
from src.utils.chunker import chunk_text

CLEAN_DIR = "src/data/cleaned"
INDEX_PATH = "src/vectorstore/index.faiss"
META_PATH = "src/vectorstore/metadata.json"

def main():
    embedder = Embedder()
    texts, metadata = [], []

    for file in Path(CLEAN_DIR).iterdir():
        content = file.read_text()
        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            metadata.append({
                "source": file.name,
                "chunk_id": i
            })

    vectors = embedder.embed(texts)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    json.dump(metadata, open(META_PATH, "w"))

    print("Vector DB built successfully")

if __name__ == "__main__":
    main()
