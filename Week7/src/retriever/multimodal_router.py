from pathlib import Path

from src.retriever.query_engine import search as text_search
from src.retriever.text_to_image import TextToImageRetriever
from src.retriever.image_to_image import ImageToImageRetriever
from src.retriever.image_to_text import ImageToTextRAG
import subprocess

class MultimodalRouter:
    def __init__(self, top_k=5):
        self.top_k = top_k

        self.text_to_image = TextToImageRetriever(top_k=top_k)
        self.image_to_image = ImageToImageRetriever(top_k=top_k)
        self.image_to_text = ImageToTextRAG(top_k=top_k)

    def is_image(self, user_input: str) -> bool:
        return Path(user_input).suffix.lower() in [
            ".jpg", ".jpeg", ".png", ".webp"
        ]

    def run(self, user_input: str):
        if self.is_image(user_input):
            return self._handle_image(user_input)
        else:
            return self._handle_text(user_input)

    # ---------------- TEXT INPUT ----------------
    def _handle_text(self, query: str):
        print("\n📄 Input detected: TEXT")

        text_results = text_search(query, top_k=self.top_k)
        image_results = self.text_to_image.search(query)

        return {
            "mode": "text",
            "query": query,
            "text_results": text_results,
            "image_results": image_results
        }

    # ---------------- IMAGE INPUT ----------------
    def _handle_image(self, image_path: str):
        print("\n🖼 Input detected: IMAGE")

        image_results = self.image_to_image.search(image_path)
        caption, text_results = self.image_to_text.search(image_path)

        return {
            "mode": "image",
            "image": image_path,
            "caption": caption,
            "text_results": text_results,
            "image_results": image_results
        }


# ---------------- CLI ----------------
if __name__ == "__main__":
    router = MultimodalRouter(top_k=5)

    user_input = input("Enter text or image path: ").strip()
    output = router.run(user_input)

    print("\n=========== FINAL OUTPUT ===========\n")

    if output["mode"] == "image":
        print("📝 Image Caption:")
        print(output["caption"], "\n")

    print("📄 TEXT RESULTS:\n")
    for i, r in enumerate(output["text_results"], 1):
        print(
            f"{i}. {r['source']} | chunk {r['chunk_id']} | score {r['score']:.4f}\n"
            f"{r['text'][:200]}...\n"
        )

    print("\n🖼 IMAGE RESULTS:\n")
    for i, r in enumerate(output["image_results"], 1):
        print(
            f"{i}. PDF: {r['pdf']} | score {r['score']:.4f}\n"
            f"Image: {r['image_path']}\n"
            
        )
        subprocess.run(["timg", r["image_path"]])
