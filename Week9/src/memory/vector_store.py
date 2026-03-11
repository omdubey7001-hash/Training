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

        # Load index
        if os.path.exists(INDEX_FILE):
            self.index = faiss.read_index(INDEX_FILE)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)

        # Load metadata
        if os.path.exists(META_FILE):
            with open(META_FILE, "r") as f:
                self.id_map = json.load(f)
        else:
            self.id_map = []


    def _embed(self, text):

        vec = self.model.encode([text])[0]
        vec = vec / np.linalg.norm(vec)

        return vec.astype("float32")


    def add_text(self, mem_id, text):

        vec = self._embed(text)

        self.index.add(np.array([vec]))

        self.id_map.append(mem_id)

        # Save index
        faiss.write_index(self.index, INDEX_FILE)

        # Save metadata
        with open(META_FILE, "w") as f:
            json.dump(self.id_map, f)


    def search(self, query, k=3):

        if self.index.ntotal == 0:
            return []

        vec = self._embed(query)

        scores, ids = self.index.search(np.array([vec]), k)

        results = []

        for score, idx in zip(scores[0], ids[0]):

            if idx == -1 or idx >= len(self.id_map):
                continue

            mem_id = self.id_map[idx]

            results.append((mem_id, float(score)))

        return results


    def delete(self, mem_id):

        if mem_id not in self.id_map:
            return

        idx = self.id_map.index(mem_id)

        self.id_map.pop(idx)

        # rebuild index
        vectors = []

        for mid in self.id_map:
            vectors.append(self._embed(mid))

        self.index = faiss.IndexFlatIP(self.dimension)

        if vectors:
            self.index.add(np.array(vectors))

        faiss.write_index(self.index, INDEX_FILE)

        with open(META_FILE, "w") as f:
            json.dump(self.id_map, f)