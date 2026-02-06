import faiss
import json
import numpy as np
from pathlib import Path
from src.embeddings.clip_embedder import CLIPEmbedder
import subprocess

INDEX_PATH = Path("src/vectorstore/image.index")
META_PATH = Path("src/vectorstore/image_index_metadata.json")


class ImageToImageRetriever:
    def __init__(self, top_k=5):
        self.index = faiss.read_index(str(INDEX_PATH))
        self.metadata = json.loads(META_PATH.read_text())
        self.embedder = CLIPEmbedder()
        self.top_k = top_k

    def search(self, image_path: str):
        # 1️⃣ Embed query image
        query_vec = self.embedder.embed_image(image_path).astype("float32")
        query_vec = query_vec.reshape(1, -1)

        # 2️⃣ FAISS search
        scores, indices = self.index.search(query_vec, self.top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            meta = self.metadata[idx]
            results.append({
                "rank": rank + 1,
                "score": float(scores[0][rank]),
                "pdf": meta["pdf"],
                "image_path": meta["image_path"]
            })

        return results


if __name__ == "__main__":
    retriever = ImageToImageRetriever(top_k=5)

    query_image = input("Enter query image path: ").strip()
    results = retriever.search(query_image)

    print("\n--- Image → Image Results ---\n")
    for r in results:
        print(
            f"Rank {r['rank']} | Score {r['score']:.4f}\n"
            f"PDF: {r['pdf']}\n"
            f"Image: {r['image_path']}\n"
            
        )
        subprocess.run(["timg", r["image_path"]])
