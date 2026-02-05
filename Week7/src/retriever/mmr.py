import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class MMRSelector:
    def __init__(self, model_name="BAAI/bge-small-en", lambda_param=0.7):
        self.model = SentenceTransformer(model_name)
        self.lambda_param = lambda_param

    def select(self, query, candidates, top_k=5):
        texts = [c["text"] for c in candidates]

        doc_embeddings = self.model.encode(
            texts, normalize_embeddings=True
        )
        query_embedding = self.model.encode(
            [query], normalize_embeddings=True
        )

        selected = []
        selected_indices = []

        sim_to_query = cosine_similarity(
            query_embedding, doc_embeddings
        )[0]

        for _ in range(top_k):
            mmr_scores = []

            for i in range(len(candidates)):
                if i in selected_indices:
                    mmr_scores.append(-1)
                    continue

                diversity = 0
                if selected_indices:
                    diversity = max(
                        cosine_similarity(
                            doc_embeddings[i].reshape(1, -1),
                            doc_embeddings[selected_indices]
                        )[0]
                    )

                score = (
                    self.lambda_param * sim_to_query[i]
                    - (1 - self.lambda_param) * diversity
                )
                mmr_scores.append(score)

            best_idx = int(np.argmax(mmr_scores))
            selected_indices.append(best_idx)
            selected.append(candidates[best_idx])

        return selected
