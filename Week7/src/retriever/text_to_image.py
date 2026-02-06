import faiss
import json
import numpy as np
from pathlib import Path
from src.embeddings.clip_embedder import CLIPEmbedder
import subprocess


INDEX_PATH = Path("src/vectorstore/image.index")
META_PATH = Path("src/vectorstore/image_index_metadata.json")


class TextToImageRetriever:
    def __init__(self, top_k=5):
        self.index = faiss.read_index(str(INDEX_PATH))
        self.metadata = json.loads(META_PATH.read_text())
        self.embedder = CLIPEmbedder()
        self.top_k = top_k

    def search(self, query: str):
        # 1️⃣ Text embedding
        query_vec = self.embedder.embed_text(query).astype("float32")

        # 2️⃣ FAISS search (extra results for dedup)
        scores, indices = self.index.search(query_vec, self.top_k * 3)

        seen = set()
        results = []
        rank = 1

        for score, idx in zip(scores[0], indices[0]):
            meta = self.metadata[idx]
            image_path = meta["image_path"]

            # 🔥 DEDUPLICATION
            if image_path in seen:
                continue

            seen.add(image_path)

            results.append({
                "rank": rank,
                "score": float(score),
                "pdf": meta["pdf"],
                "image_file": meta["image_file"],
                "image_path": image_path,
                
            })

            rank += 1
            if rank > self.top_k:
                break

        return results




if __name__ == "__main__":
    retriever = TextToImageRetriever(top_k=5)
    q = input("Enter text query: ")

    results = retriever.search(q)

    print("\n--- Text → Image Results ---\n")
    for r in results:
        print(
            f"Rank {r['rank']} | Score {r['score']:.4f}\n"
            f"PDF: {r['pdf']}\n"
            f"Image: {r['image_path']}\n"
            
            "-"
        )
        subprocess.run(["timg", r["image_path"]])
