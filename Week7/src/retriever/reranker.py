# src/retriever/reranker.py

from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    """
    Cross-Encoder based reranker
    Input  : query + candidate chunks
    Output : reranked candidates (high precision)
    """

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, candidates, top_k=5):
        """
        candidates: list of dicts
        Each dict must contain: text, source, chunk_id
        """

        pairs = [[query, c["text"]] for c in candidates]

        scores = self.model.predict(pairs)

        for i, score in enumerate(scores):
            candidates[i]["rerank_score"] = float(score)

        candidates = sorted(
            candidates,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return candidates[:top_k]
