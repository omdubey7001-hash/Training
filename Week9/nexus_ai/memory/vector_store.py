import faiss
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(__file__)

INDEX_FILE = os.path.join(BASE_DIR, "vector.index")
META_FILE = os.path.join(BASE_DIR, "vector_meta.json")


class VectorStore:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384

        if os.path.exists(INDEX_FILE):
            self.index = faiss.read_index(INDEX_FILE)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)

        if os.path.exists(META_FILE):
            with open(META_FILE, "r") as f:
                data = json.load(f)
                self.id_map = data.get("ids", [])
                self.text_map = data.get("texts", {})
        else:
            self.id_map = []
            self.text_map = {}

    def _embed(self, text):

        vec = self.model.encode(text)

        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec.astype("float32")

        vec = vec / norm

        return vec.astype("float32")

    def _save(self):

        faiss.write_index(self.index, INDEX_FILE)

        with open(META_FILE, "w") as f:
            json.dump(
                {
                    "ids": self.id_map,
                    "texts": self.text_map
                },
                f
            )

    def add_text(self, mem_id, text):

        vec = self._embed(text)

        self.index.add(np.array([vec]))

        self.id_map.append(mem_id)
        self.text_map[str(mem_id)] = text

        self._save()

    def search(self, query, k=3):

        if self.index.ntotal == 0:
            return []

        k = min(k, self.index.ntotal)

        vec = self._embed(query)

        scores, ids = self.index.search(np.array([vec]), k)

        results = []

        for score, idx in zip(scores[0], ids[0]):

            if idx == -1:
                continue

            mem_id = self.id_map[idx]

            results.append((mem_id, float(score)))

        return results

    def delete(self, mem_id):

        mem_id = str(mem_id)

        if mem_id not in self.text_map:
            return

        # remove
        self.text_map.pop(mem_id)
        self.id_map = [i for i in self.id_map if str(i) != mem_id]

        # rebuild index
        self.index = faiss.IndexFlatIP(self.dimension)

        if self.id_map:

            texts = [self.text_map[str(i)] for i in self.id_map]

            vectors = self.model.encode(texts)

            vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

            self.index.add(vectors.astype("float32"))

        self._save()