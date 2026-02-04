from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="BAAI/bge-small-en"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
