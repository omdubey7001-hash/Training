import glob
from rank_bm25 import BM25Okapi

from src.retriever.query_engine import search as semantic_search
from src.retriever.merge_utils import merge_and_dedup
from src.retriever.reranker import CrossEncoderReranker
from src.retriever.mmr import MMRSelector



class KeywordRetriever:
    def __init__(self, chunks_path="src/data/chunks"):
        self.chunk_files = glob.glob(f"{chunks_path}/*.txt")
        self.texts = []
        self.file_map = []

        for f in self.chunk_files:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                txt = fp.read()
                self.texts.append(txt)
                self.file_map.append(f)

        tokenized = [t.lower().split() for t in self.texts]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, top_k=5):
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []
        for idx, score in ranked:
            results.append({
                "source": self.file_map[idx],
                "text": self.texts[idx],
                "chunk_id": idx,
                "score": float(score),
                "type": "keyword"
            })

        return results


class HybridRetriever:
    def __init__(self):
        self.keyword = KeywordRetriever()
        self.reranker = CrossEncoderReranker()
        self.mmr = MMRSelector(lambda_param=0.7)

    def search(self, query, top_k_semantic=5, top_k_keyword=5, final_k=5):

        # 1️⃣ Semantic Retrieval (FAISS)
        semantic_results = semantic_search(query, top_k=top_k_semantic)
        for r in semantic_results:
            r["type"] = "semantic"

        # 2️⃣ Keyword Retrieval (BM25)
        keyword_results = self.keyword.search(query, top_k=top_k_keyword)

        # 3️⃣ Merge + Dedup
        merged = merge_and_dedup(semantic_results, keyword_results)

        print("\n--- Merged & Deduplicated Results ---\n")
        for i, r in enumerate(merged, 1):
            print(
                f"{i}. [{r['type']}] {r['source']} | "
                f"chunk {r.get('chunk_id', 'N/A')} | score {r['score']:.4f}"
            )

        # 4️⃣ Cross-Encoder Reranking
        # (yahan thode zyada candidates rakho for MMR)
        reranked = self.reranker.rerank(
            query=query,
            candidates=merged,
            top_k=10
        )

        print("\n--- Cross-Encoder Reranked ---\n")
        for i, r in enumerate(reranked, 1):
            print(
                f"{i}. {r['source']} | chunk {r.get('chunk_id', 'N/A')} "
                f"| rerank_score {r['rerank_score']:.4f}"
            )

        # 5️⃣ MMR (Final selection for LLM context)
        final_results = self.mmr.select(
            query=query,
            candidates=reranked,
            top_k=final_k
        )

        print("\n--- Final Results after MMR ---\n")
        for i, r in enumerate(final_results, 1):
            print(
                f"{i}. {r['source']} | chunk {r.get('chunk_id', 'N/A')}"
            )

        return final_results



if __name__ == "__main__":
    hr = HybridRetriever()
    q = input("Enter query: ")

    results = hr.search(q)

    print("\n--- Reranked Final Results ---\n")
    for i, r in enumerate(results, 1):
        print(
            f"{i}. {r['source']} \n | chunk {r['chunk_id']}\n "
            f"| rerank_score {r['rerank_score']:.4f}\n"
            f"| TEXT: {r['text'][:300]}...\n"
        )

