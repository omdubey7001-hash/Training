from src.vectorstore.image_captioner import ImageCaptioner
from src.retriever.query_engine import search as text_search


class ImageToTextRAG:
    def __init__(self, top_k=5):
        self.captioner = ImageCaptioner()
        self.top_k = top_k

    def search(self, image_path: str):
        print("\n🖼 Image:", image_path)

        # 1️⃣ Image → Caption
        caption = self.captioner.caption(image_path)
        print("\n📝 Generated Caption:")
        print(caption)

        # 2️⃣ Caption → Text FAISS
        results = text_search(caption, top_k=self.top_k)

        return caption, results


if __name__ == "__main__":
    retriever = ImageToTextRAG(top_k=5)

    img = input("Enter image path: ").strip()
    caption, results = retriever.search(img)

    print("\n--- Image → Text RAG Results ---\n")
    for i, r in enumerate(results, 1):
        print(
            f"{i}. Source: {r['source']} | chunk {r['chunk_id']} | score {r['score']:.4f}\n"
            f"TEXT: {r['text'][:300]}...\n"
        )
