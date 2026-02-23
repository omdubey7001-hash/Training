from src.vectorstore.image_captioner import ImageCaptioner
from src.utils.ocr import extract_text
from src.retriever.query_engine import search as text_search


class ImageToTextRetriever:
    def __init__(self, top_k=5):
        self.captioner = ImageCaptioner()
        self.top_k = top_k

    def search(self, image_path):
        caption = self.captioner.caption(image_path)

        ocr_text = extract_text(image_path)

        combined_query = caption
        if ocr_text.strip():
            combined_query = ocr_text + "\n" + caption


        # print("\n📝 Generated Caption:")
        # print(caption)

        # if ocr_text.strip():
        #     print("\n🔍 OCR Text:")
        #     print(ocr_text[:300])

        # print("\n🧠 Combined Query Used for RAG:")
        # print(combined_query)

        results = text_search(combined_query, top_k=self.top_k)

        return combined_query, results 



if __name__ == "__main__":
    retriever = ImageToTextRetriever(top_k=5)

    img = input("Enter image path: ").strip()

    caption, results = retriever.search(img)

    print("\n--- Image → Text RAG Results ---\n")
    for i, r in enumerate(results, 1):
        print(
            f"{i}. Source: {r['source']} | chunk {r['chunk_id']} | score {r['score']:.4f}\n"
            f"TEXT: {r['text'][:300]}...\n"
        )

