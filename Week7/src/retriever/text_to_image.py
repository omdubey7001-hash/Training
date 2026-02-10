import faiss
import json
import numpy as np
from pathlib import Path
import subprocess

from src.embeddings.clip_embedder import CLIPEmbedder

# ---------------- PATHS ----------------
INDEX_PATH = Path("src/vectorstore/image.index")
META_PATH = Path("src/data/embeddings/images/image_metadata.json")


# ---------------- RETRIEVER ----------------
class TextToImageRetriever:
    def __init__(self, top_k=5, show_image=True):
        self.index = faiss.read_index(str(INDEX_PATH))
        self.metadata = json.loads(META_PATH.read_text())

        self.embedder = CLIPEmbedder()
        self.top_k = top_k
        self.show_image = show_image

    def _text_match_score(self, query: str, caption: str, ocr: str):
        """
        Simple lexical matching score (lightweight but effective)
        """
        query = query.lower()
        score = 0.0

        if caption:
            score += sum(1 for w in query.split() if w in caption.lower())

        if ocr:
            score += sum(1 for w in query.split() if w in ocr.lower())

        return score

    def search(self, query: str):
        # 1️⃣ Text → CLIP embedding
        query_vec = self.embedder.embed_text(query).astype("float32")
        scores, indices = self.index.search(query_vec, self.top_k * 3)

        results = []

        # 2️⃣ Combine CLIP + Caption + OCR
        for idx, clip_score in zip(indices[0], scores[0]):
            meta = self.metadata[idx]

            caption = meta.get("caption", "")
            ocr_text = meta.get("ocr_text", "")

            text_score = self._text_match_score(query, caption, ocr_text)

            final_score = (0.7 * clip_score) + (0.3 * text_score)

            results.append({
                "final_score": float(final_score),
                "clip_score": float(clip_score),
                "pdf": meta["pdf"],
                "image_path": meta["image_path"],
                "caption": caption,
                "ocr_text": ocr_text
            })

        # 3️⃣ Sort + take top_k
        results = sorted(results, key=lambda x: x["final_score"], reverse=True)
        return results[:self.top_k]


# ---------------- CLI ----------------
if __name__ == "__main__":
    retriever = TextToImageRetriever(top_k=5, show_image=True)
    query = input("Enter text query: ")

    results = retriever.search(query)

    print("\n--- Text → Image Results (CLIP + Caption + OCR) ---\n")

    for i, r in enumerate(results, 1):
        print(
            f"Rank {i}\n"
            f"Final Score : {r['final_score']:.4f}\n"
            f"CLIP Score  : {r['clip_score']:.4f}\n"
            f"PDF         : {r['pdf']}\n"
            f"Image       : {r['image_path']}\n"
            f"Caption     : {r['caption']}\n"
            f"OCR Text    : {r['ocr_text'][:200]}\n"
        )

        # Optional: render image in terminal
        try:
            subprocess.run(["timg", r["image_path"]])
        except Exception:
            pass

        print("=" * 60)
